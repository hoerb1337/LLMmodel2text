##### README for
Electronic attachment on USB flash drive for master's thesis
##### "An explorative study on using LLMs to explain process models"
by Eduard Kaucher/s0641340@stud.uni-frankfurt.de

submitted to Department of Informatics/Goethe-University Frankfurt

04th December 2023



####### Contents on electronic attachment #######

- Master's thesis document as PDF

- Folder "Analysis":

    -- Mainly Overview_Results_Analysis.xlsx, it includes:

        ---> Overview on model characteristics and descriptive statistics

        ---> Raw results from each experiment

        ---> Aggregated results from each experiment

    -- All Python scripts used to create box plots and scatter plots

    -- All constructed .csv-files for the analysis



- Folder "Code":

    -- All developed Python scripts for the LLM-based and RALLM-based model-to-text approach


- Folder "Data_set":
  
    -- All collected 37 BPMN models (mainly from Fabian (2010)) in .bpmn format

    -- Case base with in-context examples for One-Shot/Few-Shot (.txt-files)

    -- New cases for RALLM-based model-to-text approach that were integrated into data pool (.txt-files)

- Folder "Experimental_output":
  
    -- All generated textual process descriptions differentiated by all experiments (.txt-files)

- Folder "Prompt Templates":
  
    -- All developed and used prompt templates differentiated by all experiments (.txt-files)


####### How-to: LLM-based model-to-text approach #######

- Only tested with Python 3.10.9
- The Python script "LLM-based_model2text.py" requires the module "LLM_prompt_engineering.py"
- LLM_prompt_engineering.py includes all prompt templates, 
  in-context examples and the function to count tokens from prompts (tiktoken)
- OpenAI API Key is required
- Dependencies:
-- openai library: see this URL for information on how to install this library: 
   https://platform.openai.com/docs/api-reference/introduction?lang=python
-- tiktoken library: see this URL for information on how to install this library: https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
- Comments should enable you to understand its underlying logic


####### How-to: RALLM-based model-to-text approach: Zero-Shot #######

- Only tested with Python 3.10.9
- Python script "retrieval_augmented_model2text_zero_shot"
- OpenAI API Key is required
- Dependencies:
-- openai library: see this URL for information on how to install this library: 
   https://platform.openai.com/docs/api-reference/introduction?lang=python
-- llama_index library: see this URL for information on how to install this library: https://docs.llamaindex.ai/en/latest/getting_started/installation.html#
- The path to the new cases needs to be adapted
- The path to the export needs to be adapted
- Comments + description in thesis PDF should enable you to understand its underlying logic

####### How-to: RALLM-based model-to-text approach: Few-Shot #######

- Only tested with Python 3.10.9
- Python script "retrieval_augmented_model2text_few_shot"
- OpenAI API Key is required
- Dependencies:
-- openai library: see this URL for information on how to install this library: 
   https://platform.openai.com/docs/api-reference/introduction?lang=python
-- llama_index library: see this URL for information on how to install this library: https://docs.llamaindex.ai/en/latest/getting_started/installation.html#
- The path to the case base needs to be adapted
- The path to the export needs to be adapted
- Comments + description in thesis PDF should enable you to understand its underlying logic
