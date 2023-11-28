import LLM_prompt_engineering
import openai
from nltk.tokenize import sent_tokenize, word_tokenize
from datetime import datetime

# Define OpenAI API key 
openai.api_key = ""

### Experimental Setup ###

# Model to be explained
explain_BPMN_model_id = ""
bpmn_model_name = ""
model_nr = ""
# Choosing prompt templates:
round = ""
# XML definition of the model:
bpmn_model =  """"""

# Choose example model for in-context learning
in_context_learning = True # True or False (Zero Shot)
example_BPMN_model_id = "" # ID of model in case base
# Retrieve in-context example from case base
example_bpmn_xml, example_bpmn_text = LLM_prompt_engineering.prompt_demonstrations(example_BPMN_model_id=example_BPMN_model_id)


### Prompt engineering: Retrieve prompt template filled with 
### model to be explained and in case of in-context learning the in-context example ###
prompt = LLM_prompt_engineering.prompt_engineering(in_context_learning = in_context_learning,
                                                   round=round,
                                                   bpmn_model_name=bpmn_model_name,
                                                   bpmn_model=bpmn_model,
                                                   example_bpmn_xml=example_bpmn_xml,
                                                   example_bpmn_text = example_bpmn_text)

# LLM setup
max_tokens=2000
n=1
temperature=0.0
model="gpt-4"
context_window = 8192

# Token number fit context window?
print("Counting the prompt's number of token...")
num_tokens = LLM_prompt_engineering.num_tokens_from_messages(prompt, model)
print("prompt's number of token: ", num_tokens)

# Prompt fits into context window
if num_tokens <= context_window:

  # Send request with defined model settings and prompt to the LLM
  chat_completion = openai.ChatCompletion.create(model=model,
                                                 messages=prompt, 
                                                 max_tokens=max_tokens,
                                                 n=n, 
                                                 temperature=temperature)

  # chat completion results
  gen_text_description = chat_completion.choices[0].message.content
  usage_prompt_tokens = chat_completion.usage.prompt_tokens
  usage_completion_tokens = chat_completion.usage.completion_tokens
  usage_total_tokens  = chat_completion.usage.total_tokens
  
  num_sentences = len(sent_tokenize(str(gen_text_description)))
  num_words = len(word_tokenize(str(gen_text_description)))

  print("Generated textual process description: ", gen_text_description, "\n",
        "usage_prompt_tokens: ", usage_prompt_tokens, "\n",
        "usage_completion_tokens: ", usage_completion_tokens, "\n",
        "usage_total_tokens: ", usage_total_tokens,"\n",
        "num_sentences: ", num_sentences, "\n",
        "num_words: ", num_words)

  # Prompt documentation
  date_experiment = datetime.today()
  prompt_documentation = ["######### Experiment Setup #########\n",
                          "Date Experiment: " + str(date_experiment), 
                          "Demonstration BPMN model: " + example_BPMN_model_id,
                          "BPMN model to explain: " + explain_BPMN_model_id,
                          "Round of prompt engineering for this model: " + round, 
                          "max_tokens: " + str(max_tokens),
                          "n: " + str(n),
                          "temperature: " + str(temperature) + "\n",
                          "######### Query used #########\n",
                          str(prompt) + "\n",
                          "######### Generated Textual Process Description #########\n",
                          str(gen_text_description) + "\n",
                          "######### Token data #########\n",
                          "usage_prompt_tokens: " + str(usage_prompt_tokens),
                          "usage_completion_tokens: " + str(usage_completion_tokens),
                          "usage_total_tokens: " + str(usage_total_tokens),
                          "num_sentences: " + str(num_sentences),
                          "num_words: " + str(num_words)
                          ]

# Prompt does not fit into context window
else:
  gen_text_description = "The prompt (number of tokens: " + str(num_tokens) + ") does not fit into the context window. Allowed are 8,192 token."

  print(gen_text_description)

  # Prompt documentation
  date_experiment = datetime.today()
  prompt_documentation = ["######### Experiment Setup #########\n",
                          "Date Experiment: " + str(date_experiment), 
                          "Demonstration BPMN model: " + example_BPMN_model_id,
                          "BPMN model to explain: " + explain_BPMN_model_id,
                          "Round of prompt engineering for this model: " + round,
                          "max_tokens: " + str(max_tokens),
                          "n: " + str(n),
                          "temperature: " + str(temperature) + "\n",
                          "######### Query used #########\n",
                          str(prompt) + "\n",
                          "######### Generated Textual Process Description #########\n",
                          str(gen_text_description) + "\n",
                          "######### Token data #########\n",
                          "usage_prompt_tokens: " + str(num_tokens)
                          ]

# Export documentation
# 0shot export address: /.../Experimental output/1_0shot/
# 1shot export address: /.../Experimental output/1_1shot/

# define your path for export
with open('/.../Experimental output/1_0shot/'+ model_nr + '_output_model_'+ explain_BPMN_model_id +'_round_'+ round +'.txt', 'w') as output:
    output.writelines('\n'.join(prompt_documentation))


