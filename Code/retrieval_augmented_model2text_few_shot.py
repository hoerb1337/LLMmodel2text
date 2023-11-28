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


# Case base
filename_fn = lambda filename: {'file_name': filename}
# define cd and files for case base
documents = SimpleDirectoryReader('.../03_case_base/./',
                                    ['.../03_case_base/case_3-7.txt',
                                     '.../03_case_base/case_3-8.txt',
                                     '.../03_case_base/case_5-1.txt',
                                     '.../03_case_base/case_5-2.txt',
                                     '.../03_case_base/case_6-2.txt',
                                     '.../03_case_base/case_8-2.txt',
                                     ],
                                     file_metadata=filename_fn).load_data()

# Case definition
bpmn_model = "" # name of model or similar, will be used for documentation

# Promp Helper
context_window=8192
num_output=2000
chunk_overlap_ratio=0.2
chunk_size_limit=None
prompt_helper = PromptHelper(context_window=context_window,
                             num_output=num_output,
                             chunk_overlap_ratio=chunk_overlap_ratio,
                             chunk_size_limit=chunk_size_limit)

# Embedding model
embed_batch_size=10
embed_model = OpenAIEmbedding(mode="similarity",
                              embed_batch_size=embed_batch_size)


# Nodeparsers
chunk_size=700
chunk_overlap=100
text_splitter = TokenTextSplitter(chunk_size=chunk_size,
                                  chunk_overlap=chunk_overlap)

node_parser = SimpleNodeParser.from_defaults(text_splitter=text_splitter,
                                             include_metadata=True,
                                             include_prev_next_rel=True)

# Service context
model="gpt-4"
temperature=0.0
llm=OpenAI(model=model, temperature=temperature)
service_context = ServiceContext.from_defaults(llm=llm,
                                               prompt_helper=prompt_helper,
                                               embed_model=embed_model,
                                               node_parser=node_parser)

# Vector Index
index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context)

# Retriever
similarity_top_k = 3 #nr. maximum retrieved cases(nodes)

# Define retriever with underlying index
vector_retriever = VectorIndexRetriever(index=index,
                                        similarity_top_k=similarity_top_k,
                                        vector_store_query_mode="default")

### Query Engine ###
# Text QA Prompt
chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="""You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Consider the standard BPMN 2.0.2 specification. Assume you have created a BPMN model. Now you want to explain the complete control flow with all interactions between participants and lanes represented by the BPMN notations used in your created BPMN model to users without knowledge on BPMN notation."""
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            """Please create a textual process description for the given BPMN model serialised in XML. Add to each type of BPMN element used in the BPMN model a short explanation of this element type's semantics.

            Exemplary textual process description for BPMN model "Example": {context_str}
            BPMN model "Explain" serialised in XML: {query_str}"""
        ),
    ),
]
text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

# Refine Prompt
chat_refine_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="""You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. You will get presented an exemplary textual process description for BPMN model "Example", which you should use as an example for the generation of textual process descriptions for given BPMN model "Explain" serialised in XML. Additionally, you will get presented your initially generated textual process description for the BPMN model "Explain". You therefore strictly operate in two modes when refining existing answers:\n1. **Add** new information to the original answer, using the exemplary textual process description.\n2. **Repeat** the original answer, if the exemplary textual process description is not useful.\nNever reference the original answer or the exemplary textual process description directly in your answer. When in doubt, just add to the original answer."""
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            """Please create a textual process description for the given BPMN model serialised in XML. Add to each type of BPMN element used in the BPMN model a short explanation of this element type's semantics.

            Exemplary textual process description for BPMN model "Example": {context_msg}
            BPMN model "Explain" serialised in XML: {query_str}
            Initial textual process description for BPMN model "Explain": {existing_answer}
            Adapted textual process description for BPMN model "Explain": """
        ),
    ),
]
refine_template = ChatPromptTemplate(chat_refine_msgs)


# Define Response Synthesizer with corresponding prompt templates
response_mode = "refine"
response_synthesizer = get_response_synthesizer(response_mode=response_mode,
                                                service_context=service_context,
                                                text_qa_template=text_qa_template,
                                                refine_template=refine_template,)

# Define Retriever Query Engine with retriever and response synthesizer
query_engine = RetrieverQueryEngine.from_args(retriever=vector_retriever,
                                              response_synthesizer=response_synthesizer,
                                              )

# User Query: Insert the BPMN model that should be explained as XML 
query = """<XML model definition>
  
Corresponding textual process description for BPMN model "Explain": """

# Send request to Retriever Query Engine and receive response
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
                        "similarity_top_k: " + str(similarity_top_k),
                        "model: " + str(model),
                        "temperature: " + str(temperature),
                        "chat_text_qa_msgs: " + str(chat_text_qa_msgs),
                        "chat_refine_msgs: " + str(chat_refine_msgs),
                        "response_mode: " + str(response_mode),
                        "Query:\n" + str(query) + "\n",
                        "response.source_nodes: " + str(response.source_nodes) + "\n",
                        "retrieved nodes: " + str(vector_retriever.retrieve(query)) + "\n",
                        "GPT response:\n" + str(response) + "\n",
                        "metadata:\n" + str(response.metadata) + "\n",
                        ]

# Export on your defined path
with open(".../Experimental output/2_1shot/" + bpmn_model + ".txt", "w") as output:
    output.writelines('\n'.join(prompt_documentation))