from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, PromptHelper, OpenAIEmbedding
import os
from llama_index.llms import OpenAI, ChatMessage, MessageRole
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index.response_synthesizers import get_response_synthesizer
from llama_index.prompts import ChatPromptTemplate
import openai
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.vector_store.retrievers.retriever import VectorIndexRetriever
from datetime import datetime


# OpenAI API Key 
openai.api_key = ''
os.environ['OPENAI_API_KEY'] = ''


def set_chunk_parameters(settings):
    """Setting the chunk parameters.
    
    Input:
      settings=1: Small context
      settings=2: Large context

    Output:
      chunk_overlap_ratio, chunk_size, chunk_overlap (int)
    """
    
    if settings == 1:
      chunk_overlap_ratio = 0.4
      chunk_size = 2048
      chunk_overlap = 400
      
    # Second two rounds
    elif settings == 2:
      chunk_overlap_ratio = 0.4
      chunk_size = 4096
      chunk_overlap = 800

    return chunk_overlap_ratio, chunk_size, chunk_overlap


# Case base

# document the file paths into retrieved nodes
filename_fn = lambda filename: {'file_name': filename} 

# define cd and files for case base
# these cases reflect the BPMN models that should be explained
documents = SimpleDirectoryReader('.../03_case_base/0shot',
                                    ['.../03_case_base/0shot/Case 10-2.txt'
                                     #'.../03_case_base/0shot/Case 8-5.txt'
                                     #'.../03_case_base/0shot/Case 8-4.txt'
                                     #'.../03_case_base/0shot/Case 2-2.txt'
                                     #'.../03_case_base/0shot/Case 2-1.txt'
                                     ],
                                     file_metadata=filename_fn).load_data()

# New case definition
bpmn_model = "" # name of model or similar, will be used for documentation

# setup response mode parameter for Response Synthesizer
response_mode = "refine"

# define wished parameter setups on chunks
settings = 2
chunk_overlap_ratio, chunk_size, chunk_overlap = set_chunk_parameters(settings)

# Promp Helper
context_window=8192
num_output=1500
chunk_size_limit=None
prompt_helper = PromptHelper(context_window=context_window,
                             num_output=num_output,
                             chunk_overlap_ratio=chunk_overlap_ratio,
                             chunk_size_limit=chunk_size_limit)

# Define Embedding model
embed_batch_size=10
embed_model = OpenAIEmbedding(mode="similarity",
                              embed_batch_size=embed_batch_size)


# Define Nodeparser
node_parser = SimpleNodeParser.from_defaults(text_splitter=TokenTextSplitter(chunk_size=chunk_size,
                                                                             chunk_overlap=chunk_overlap),
                                             include_metadata=True,
                                             include_prev_next_rel=True)


# Define LLM model and corresponding parameters
model="gpt-4"
temperature=0.0
llm=OpenAI(model=model, temperature=temperature)

# Service context as overarching setup that can be used 
# in multiple modules
service_context = ServiceContext.from_defaults(llm=llm,
                                               prompt_helper=prompt_helper,
                                               embed_model=embed_model,
                                               node_parser=node_parser)

# Vector Index
index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context)

# Define the Retriever with underlying index
vector_retriever = VectorIndexRetriever(index=index,
                                        similarity_top_k=99,
                                        vector_store_query_mode="default")

### Query Engine ###
# Text QA Prompt
chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="""You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. You will get presented a part of a BPMN model serialised in XML because of your limited context window. Always answer the query using the provided part of the BPMN model serialised in XML."""
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "Query: {query_str}\n"
            "Part of the BPMN model serialised in XML:\n"
            "{context_str}\n"
            "Given the part of the BPMN model serialised in XML, "
            "answer the query.\n"
            "Answer: "
        ),
    ),
]
text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

# Refine Prompt
chat_refine_msgs = [
    ChatMessage(
        role=MessageRole.USER,
        content=(
            """You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. You will get presented a part of a BPMN model serialised in XML because of your limited context window. Each part includes overlapping BPMN model elements to provide you orientation regarding the correct order of the control flow. At the end you will have seen all parts of the BPMN model serialised in XML, enabling you to create a coherent textual process description for the complete BPMN model. You therefore strictly operate in three modes when refining existing answers:
            1. **Add** new information to the original answer, using the new part of BPMN model serialised in XML.
            2. **Repeat** the original answer, if the new part of BPMN model serialised in XML isn't useful.
            3. **Adapt** existing sentences and/or the position of the sentence, if appropriate according to the new part of BPMN model serialised in XML.
            Never reference the original answer or the new given part of the BPMN model serialised in XML directly in your answer. When in doubt, just add to the original answer without deleting existing sentences. 
            
            Query: {query_str}

            Original Answer: {existing_answer}

            New part of BPMN model serialised in XML: {context_msg}

            New Answer: """
        ),
    ),
]
refine_template = ChatPromptTemplate(chat_refine_msgs)

# Define Response Synthesizer with corresponding prompt templates
response_synthesizer = get_response_synthesizer(response_mode=response_mode,
                                                service_context=service_context,
                                                text_qa_template=text_qa_template,
                                                refine_template=refine_template,)

# Define Retriever Query Engine with retriever and response synthesizer
query_engine = RetrieverQueryEngine.from_args(retriever=vector_retriever,
                                              response_synthesizer=response_synthesizer,
                                              )

# User Query: define reference to model that should be explained in case base
query = """Consider the standard BPMN 2.0.2 specification. Assume you have created a BPMN model. Now you want to explain the complete control flow with all interactions between participants and lanes represented by the BPMN notations used in your created BPMN model to users without knowledge on BPMN notation. Please create a coherent textual process description for the BPMN model "<Case ID: Name of case>" serialised in XML, considering each model element in the given BPMN model. Do not add any information that is not described in the given BPMN model. Your final generated textual process description should enable users to easily follow the control flow with all interactions between all participants in the given BPMN model."""

#  Send request to Retriever Query Engine and receive response
response = query_engine.query(query)
print(response)

# Prompt documentation
date_experiment = datetime.today()
prompt_documentation = ["Date Experiment: " + str(date_experiment),
                        "BPMN model: " + bpmn_model,
                        "context_window: " + str(context_window),
                        "num_output: " + str(num_output),
                        "chunk_overlap_ratio: " + str(chunk_overlap_ratio),
                        "chunk_size_limit: " + str(chunk_size_limit),
                        "Embedding batch size: " + str(embed_batch_size),
                        "chunk_size: " + str(chunk_size),
                        "chunk_overlap: " + str(chunk_overlap),
                        "model: " + str(model),
                        "temperature: " + str(temperature),
                        "chat_text_qa_msgs: " + str(chat_text_qa_msgs),
                        "chat_refine_msgs: " + str(chat_refine_msgs),
                        "response_mode: " + str(response_mode),
                        "Query: " + str(query) + "\n",
                        "GPT response: " + str(response) + "\n",
                        "Nodes: " + str(response.source_nodes) + "\n",
                        "metadata: " + str(response.metadata) + "\n",
                        "retrieved nodes: " + str(vector_retriever.retrieve(query))
                        ]

# Export on your defined path
with open(".../Experimental output/2_0shot/" + bpmn_model + ".txt", "w") as output:
    output.writelines('\n'.join(prompt_documentation))