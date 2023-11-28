import tiktoken

def prompt_engineering(in_context_learning,
                       round,
                       bpmn_model_name,
                       bpmn_model,
                       example_bpmn_xml="None",
                       example_bpmn_text="None"):
    """Return a ready-to-use prompt.
    
    Input:
        in_context_learning: True/False (Bolean)
        round: #round of experiment for current model (str)
        bpmn_model_name: name of current model (str)
        bpmn_model: XML code for current BPMN model (str)
        example_bpmn_xml: XML code for example model (str)
        example_bpmn_text: textual description for example model (str)
    
    Return:
        prompt: prompt object
    """

    if in_context_learning == False:
        if round == "1":
            # Initial prompt
            prompt = [
                        {"role": "user",
                        "content":
                        f"""Consider the standard BPMN 2.0.2 specification. Please create a textual process description for following BPMN model "{bpmn_model_name}" serialised in XML.
                        
                        BPMN model "{bpmn_model_name}" serialised in XML:
                        {bpmn_model}"""
                        }
                    ]

        elif round == "2":
            # Initial prompt + System context
            prompt = [  {"role": "system",
                        "content":
                        "You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Assume you have created a BPMN model. Now you want to explain your BPMN model to users without knowledge on BPMN notation. Consider the standard BPMN 2.0.2 specification."
                        },
                        {"role": "user",
                        "content":
                        f"""Please create a textual process description for following BPMN model "{bpmn_model_name}" serialised in XML.
                        
                        BPMN model "{bpmn_model_name}" serialised in XML:
                        {bpmn_model}"""
                        }
                    ]

        elif round == "3":
            # Initial prompt + System context + Placeholder for output
            prompt = [  {"role": "system",
                        "content":
                        "You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Assume you have created a BPMN model. Now you want to explain your BPMN model to users without knowledge on BPMN notation. Consider the standard BPMN 2.0.2 specification."
                        },
                        {"role": "user",
                        "content":
                        f"""Please create a textual process description for following BPMN model "{bpmn_model_name}" serialised in XML.

                        BPMN model "{bpmn_model_name}" serialised in XML:
                        {bpmn_model}
                        
                        Textual process description for the given BPMN model serialised in XML above:"""
                        }
                    ]

        elif round == "4":
            # Initial prompt + System context + Placeholder for output + Output instructions (style of text)
            prompt = [  {"role": "system",
                        "content":
                        "You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Assume you have created a BPMN model. Now you want to explain your BPMN model to users without knowledge on BPMN notation. Consider the standard BPMN 2.0.2 specification."
                        },
                        {"role": "user",
                        "content":
                        f"""Please create a textual process description for following BPMN model "{bpmn_model_name}" serialised in XML. Do not add any information that is not described in the given BPMN model. Your generated textual process description should enable users to map the relationship of the model elements to the corresponding textual elements in your generated description. 

                        BPMN model "{bpmn_model_name}" serialised in XML:
                        {bpmn_model}
                        
                        Textual process description for the given BPMN model serialised in XML above:"""
                        }
                    ]
        
        elif round == "5":
            # Initial prompt + System context + Output instructions (style of text)
            prompt = [  {"role": "system",
                        "content":
                        "You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Assume you have created a BPMN model. Now you want to explain your BPMN model to users without knowledge on BPMN notation. Consider the standard BPMN 2.0.2 specification."
                        },
                        {"role": "user",
                        "content":
                        f"""Please create a textual process description for following BPMN model "{bpmn_model_name}" serialised in XML. Do not add any information that is not described in the given BPMN model. Your generated textual process description should enable users to map the relationship of the model elements to the corresponding textual elements in your generated description. 

                        BPMN model "{bpmn_model_name}" serialised in XML:
                        {bpmn_model}"""
                        }
                    ]
    
    # in-context learning yes
    if in_context_learning == True:
        if round == "1":
            # Initial prompt without system
            prompt = [{
                "role": "user",
                "content": f"""Consider the standard BPMN 2.0.2 specification. Please create a textual process description for the given BPMN model serialised in XML.
                
                BPMN model "Example" serialised in XML:
                {example_bpmn_xml}
                
                Corresponding textual process description for the BPMN model "Example":
                {example_bpmn_text}
                
                BPMN model "{bpmn_model_name}" serialised in XML:
                {bpmn_model}
                
                Corresponding textual process description for the BPMN model "{bpmn_model_name}": """
                }]


        elif round == "2":
            
            # Initial prompt + System context
            prompt = [{
                "role": "system",
                "content": """You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Consider the standard BPMN 2.0.2 specification. Assume you have created a BPMN model. Now you want to explain the complete control flow with all interactions between participants and lanes represented by the BPMN notations used in your created BPMN model to users without knowledge on BPMN notation."""
                },
                {"role": "user",
                 "content": f"""Please create a textual process description for the given BPMN model serialised in XML.
                 
                 BPMN model "Example" serialised in XML:
                 {example_bpmn_xml}
                 
                 Corresponding textual process description for the BPMN model "Example":
                 {example_bpmn_text}
                 
                 BPMN model "{bpmn_model_name}" serialised in XML:
                 {bpmn_model}
                 
                 Corresponding textual process description for the BPMN model "{bpmn_model_name}": """
                 }]


        elif round == "3":

            # Initial prompt + System context + Output instructions
            prompt = [{
                "role": "system",
                "content": """You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Consider the standard BPMN 2.0.2 specification. Assume you have created a BPMN model. Now you want to explain the complete control flow with all interactions between participants and lanes represented by the BPMN notations used in your created BPMN model to users without knowledge on BPMN notation."""
                },
                {"role": "user",
                 "content": f"""Please create a textual process description for the given BPMN model serialised in XML. Add to each type of BPMN element used in the BPMN model a short explanation of this element type's semantics.
                 
                 BPMN model "Example" serialised in XML:
                 {example_bpmn_xml}
                 
                 Corresponding textual process description for the BPMN model "Example":
                 {example_bpmn_text}
                 
                 BPMN model "{bpmn_model_name}" serialised in XML:
                 {bpmn_model}
                 
                 Corresponding textual process description for the BPMN model "{bpmn_model_name}": """
                 }]


        elif round == "4":
            # Initial prompt + System context + Output instructions + Another example

            prompt = [{
                "role": "system",
                "content": """You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Consider the standard BPMN 2.0.2 specification. Assume you have created a BPMN model. Now you want to explain the complete control flow with all interactions between participants and lanes represented by the BPMN notations used in your created BPMN model to users without knowledge on BPMN notation."""
                },
                {"role": "user",
                 "content": f"""Please create a textual process description for the given BPMN model serialised in XML. Add to each type of BPMN element used in the BPMN model a short explanation of this element type's semantics.
                 
                 BPMN model "Example" serialised in XML:
                 {example_bpmn_xml}
                 
                 Corresponding textual process description for the BPMN model "Example":
                 {example_bpmn_text}
                 
                 BPMN model "{bpmn_model_name}" serialised in XML:
                 {bpmn_model}
                 
                 Corresponding textual process description for the BPMN model "{bpmn_model_name}": """
                 }]
            
        elif round == "5":
            # Initial prompt + System context + Output instructions + Another example

            prompt = [{
                "role": "system",
                "content": """You are an expert Q&A system with expert knowledge on the business process modeling language BPMN. Consider the standard BPMN 2.0.2 specification. Assume you have created a BPMN model. Now you want to explain the complete control flow with all interactions between participants and lanes represented by the BPMN notations used in your created BPMN model to users without knowledge on BPMN notation."""
                },
                {"role": "user",
                 "content": f"""Please create a textual process description for the given BPMN model serialised in XML. Add to each type of BPMN element used in the BPMN model a short explanation of this element type's semantics.
                 
                 BPMN model "{bpmn_model_name}" serialised in XML:
                 {bpmn_model}
                 
                 Corresponding textual process description for the BPMN model "{bpmn_model_name}": """
                 }]

    return prompt


def num_tokens_from_messages(messages, model="gpt-4"):
    """Return the number of tokens used by prompts."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        #print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        #print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def prompt_demonstrations(example_BPMN_model_id):
    """Return BPMN model in XML and corresponding textual process description.
    
    Input:
        example_BPMN_model_id: 3-7, 3-8, 5-1, 5-2, 6-2, or 8-2
    Return:
        example_bpmn_xml, example_bpmn_text: str
    """

    if example_BPMN_model_id == "3-7":

        example_bpmn_xml =  """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_0yb0ktp" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="5.11.0" modeler:executionPlatform="Camunda Cloud" modeler:executionPlatformVersion="8.2.0">
  <bpmn:process id="Process_03kcn31" isExecutable="true">
    <bpmn:startEvent id="StartEvent_1">
      <bpmn:outgoing>Flow_1x8kcbq</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Activity_0huhreq" name="Search Police report database">
      <bpmn:incoming>Flow_1x8kcbq</bpmn:incoming>
      <bpmn:outgoing>Flow_0ryvp0p</bpmn:outgoing>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_0lynl6x">
        <bpmn:targetRef>DataObjectReference_0sbmk34</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1x8kcbq" sourceRef="StartEvent_1" targetRef="Activity_0huhreq" />
    <bpmn:task id="Activity_0yzqumq" name="Compose file">
      <bpmn:incoming>Flow_0ryvp0p</bpmn:incoming>
      <bpmn:outgoing>Flow_0ot8n99</bpmn:outgoing>
      <bpmn:property id="Property_06usyus" name="__targetRef_placeholder" />
      <bpmn:dataInputAssociation id="DataInputAssociation_140xt9x">
        <bpmn:sourceRef>DataObjectReference_0sbmk34</bpmn:sourceRef>
        <bpmn:targetRef>Property_06usyus</bpmn:targetRef>
      </bpmn:dataInputAssociation>
      <bpmn:dataInputAssociation id="DataInputAssociation_0szqspg">
        <bpmn:sourceRef>DataObjectReference_1yk32tm</bpmn:sourceRef>
        <bpmn:targetRef>Property_06usyus</bpmn:targetRef>
      </bpmn:dataInputAssociation>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_1iub117">
        <bpmn:targetRef>DataObjectReference_1yyvmbj</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_0ryvp0p" sourceRef="Activity_0huhreq" targetRef="Activity_0yzqumq" />
    <bpmn:dataObjectReference id="DataObjectReference_0sbmk34" name="Police Report" dataObjectRef="DataObject_1ufq9ut" />
    <bpmn:dataObject id="DataObject_1ufq9ut" />
    <bpmn:dataObjectReference id="DataObjectReference_1yk32tm" name="Claim Documentation" dataObjectRef="DataObject_19iww9w" />
    <bpmn:dataObject id="DataObject_19iww9w" />
    <bpmn:dataObjectReference id="DataObjectReference_1yyvmbj" name="Claim file" dataObjectRef="DataObject_08tubol" />
    <bpmn:dataObject id="DataObject_08tubol" />
    <bpmn:task id="Activity_1e55wud" name="Calculate claim estimate">
      <bpmn:incoming>Flow_0ot8n99</bpmn:incoming>
      <bpmn:outgoing>Flow_1oo1z9u</bpmn:outgoing>
      <bpmn:property id="Property_08rwa23" name="__targetRef_placeholder" />
      <bpmn:dataInputAssociation id="DataInputAssociation_0qms8yy">
        <bpmn:sourceRef>DataObjectReference_1yyvmbj</bpmn:sourceRef>
        <bpmn:targetRef>Property_08rwa23</bpmn:targetRef>
      </bpmn:dataInputAssociation>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_0ot8n99" sourceRef="Activity_0yzqumq" targetRef="Activity_1e55wud" />
    <bpmn:task id="Activity_1bwjxfi" name="Create action plan">
      <bpmn:incoming>Flow_1oo1z9u</bpmn:incoming>
      <bpmn:outgoing>Flow_1mxrbpk</bpmn:outgoing>
      <bpmn:property id="Property_06xdum4" name="__targetRef_placeholder" />
      <bpmn:dataInputAssociation id="DataInputAssociation_0ylr8eq">
        <bpmn:sourceRef>DataObjectReference_14hmu5b</bpmn:sourceRef>
        <bpmn:targetRef>Property_06xdum4</bpmn:targetRef>
      </bpmn:dataInputAssociation>
      <bpmn:dataOutputAssociation id="DataOutputAssociation_0pzk989">
        <bpmn:targetRef>DataObjectReference_17mumyy</bpmn:targetRef>
      </bpmn:dataOutputAssociation>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1oo1z9u" sourceRef="Activity_1e55wud" targetRef="Activity_1bwjxfi" />
    <bpmn:task id="Activity_1albiw2" name="Negotiate estimate settlement">
      <bpmn:incoming>Flow_1mxrbpk</bpmn:incoming>
      <bpmn:outgoing>Flow_1y8vlta</bpmn:outgoing>
      <bpmn:property id="Property_0xc58jq" name="__targetRef_placeholder" />
      <bpmn:dataInputAssociation id="DataInputAssociation_1isldqh">
        <bpmn:sourceRef>DataObjectReference_17mumyy</bpmn:sourceRef>
        <bpmn:targetRef>Property_0xc58jq</bpmn:targetRef>
      </bpmn:dataInputAssociation>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1mxrbpk" sourceRef="Activity_1bwjxfi" targetRef="Activity_1albiw2" />
    <bpmn:task id="Activity_0n8qr56" name="Notify claimant">
      <bpmn:incoming>Flow_1y8vlta</bpmn:incoming>
      <bpmn:outgoing>Flow_0p5nfd4</bpmn:outgoing>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1y8vlta" sourceRef="Activity_1albiw2" targetRef="Activity_0n8qr56" />
    <bpmn:endEvent id="Event_1dirp9l">
      <bpmn:incoming>Flow_0p5nfd4</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_0p5nfd4" sourceRef="Activity_0n8qr56" targetRef="Event_1dirp9l" />
    <bpmn:dataObjectReference id="DataObjectReference_17mumyy" name="Action Plan" dataObjectRef="DataObject_1ysxdsm" />
    <bpmn:dataObject id="DataObject_1ysxdsm" />
    <bpmn:dataObjectReference id="DataObjectReference_14hmu5b" name="Action plan checklist" dataObjectRef="DataObject_0eboxt5" />
    <bpmn:dataObject id="DataObject_0eboxt5" />
    <bpmn:textAnnotation id="TextAnnotation_16tjowl">
      <bpmn:text>Police Report database</bpmn:text>
    </bpmn:textAnnotation>
    <bpmn:association id="Association_1x7pd76" sourceRef="DataObjectReference_0sbmk34" targetRef="TextAnnotation_16tjowl" />
    <bpmn:group id="Group_0xpfwt4" categoryValueRef="CategoryValue_1ize5xt" />
    <bpmn:textAnnotation id="TextAnnotation_08z9mi2">
      <bpmn:text>Document Management system</bpmn:text>
    </bpmn:textAnnotation>
    <bpmn:association id="Association_11ig4d5" sourceRef="DataObjectReference_14hmu5b" targetRef="TextAnnotation_08z9mi2" />
  </bpmn:process>
  <bpmn:category id="Category_1pqnpmn">
    <bpmn:categoryValue id="CategoryValue_1ize5xt" value="Claims handler" />
  </bpmn:category>"""

        example_bpmn_text = """The process "Claims Creation" begins with a start event. As the name implies, the Start Event indicates where a particular Process will start. 

The first task in the process is "Search Police report database". A Task is an atomic Activity that is included within a Process. A Task is used when the work in the Process is not broken down to a finer level of Process detail. In this case, the task involves searching a database for a police report. The output of this task is a "Police Report", which is a data object. Data Objects provide information about what Activities require to be performed and/or what they produce. There is a text annotation associated with the "Police Report" data object, providing additional context about the sources of the data object. Text Annotations in general are a mechanism to provide additional text information for the reader of a BPMN Diagram.

The next task is "Compose file". This task takes in the "Police Report" data object from the previous task and also requires "Claim Documentation" data object. The task involves composing a file using the provided data. The output of this task is a "Claim file", which is another data object that is passed on to the next task.

The third task is "Calculate claim estimate". This task takes in the "Claim file" data object from the previous task. The task involves calculating an estimate for the claim. 

Then, the fourth task is "Create action plan". This task requires an "Action plan checklist" data object to which another text annotation is associated with: "Document Management system", indicating the sources of the data object. The task involves creating an action plan. The output of this task is an "Action Plan", which is a data object that is passed on to the next task.

Both tasks "Compose file" and "Create action plan" can be grouped as "Claims handler". A Group is a grouping of objects that are within the same Category.

After this group, the fifth task is "Negotiate estimate settlement". This task takes in the "Action Plan" data object from the previous task. The task involves negotiating a settlement for the estimate.

The final task is "Notify claimant". This task involves notifying the claimant.

The process then ends with an end event. The End Event indicates where a Process will end."""

    elif example_BPMN_model_id == "3-8":

        example_bpmn_xml =  """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_0olsr0n" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="5.11.0" modeler:executionPlatform="Camunda Cloud" modeler:executionPlatformVersion="8.2.0">
  <bpmn:collaboration id="Collaboration_0iz0an2">
    <bpmn:participant id="Participant_0a7q4v0" name="Customer" processRef="Process_1ewbob1" />
    <bpmn:participant id="Participant_18a5p3c" name="Car Insurer" processRef="Process_01tezej" />
    <bpmn:participant id="Participant_0f0onrm" name="Garage" processRef="Process_1frlouu" />
    <bpmn:messageFlow id="Flow_0rr1xln" name="Claim documentation" sourceRef="Participant_0a7q4v0" targetRef="Activity_0686hn9" />
    <bpmn:messageFlow id="Flow_02apfuz" name="Damage information" sourceRef="Activity_072pala" targetRef="Participant_0f0onrm" />
    <bpmn:messageFlow id="Flow_1474a18" name="Payment details" sourceRef="Activity_16bxegr" targetRef="Participant_0f0onrm" />
    <bpmn:messageFlow id="Flow_0oqbxrj" name="Notification letter" sourceRef="Activity_19c3fj0" targetRef="Participant_0a7q4v0" />
  </bpmn:collaboration>
  <bpmn:process id="Process_1ewbob1" isExecutable="true" />
  <bpmn:process id="Process_01tezej" isExecutable="false">
    <bpmn:laneSet id="LaneSet_0gi7qfp">
      <bpmn:lane id="Lane_0ok7kee" name="Notification department">
        <bpmn:flowNodeRef>Event_11hpg0d</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0686hn9</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_1ydrt60</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_0au7c02" name="Handling department">
        <bpmn:flowNodeRef>Activity_1awfkpk</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0xogugs</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_0wp3q6n</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0ymp5qo</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_072pala</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_16bxegr</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_19776w0</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_19c3fj0</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Event_1lkae47</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    <bpmn:startEvent id="Event_11hpg0d">
      <bpmn:outgoing>Flow_1200nwn</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Activity_0686hn9" name="Check documentation">
      <bpmn:incoming>Flow_1200nwn</bpmn:incoming>
      <bpmn:outgoing>Flow_1gf4417</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_1ydrt60" name="Register claim">
      <bpmn:incoming>Flow_1gf4417</bpmn:incoming>
      <bpmn:outgoing>Flow_1d5516w</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_1awfkpk" name="Check insurance">
      <bpmn:incoming>Flow_1d5516w</bpmn:incoming>
      <bpmn:outgoing>Flow_0lvov8u</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_0xogugs" name="Perform assessmet">
      <bpmn:incoming>Flow_0lvov8u</bpmn:incoming>
      <bpmn:outgoing>Flow_0htr0cu</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_0wp3q6n">
      <bpmn:incoming>Flow_0htr0cu</bpmn:incoming>
      <bpmn:outgoing>Flow_18bi0f6</bpmn:outgoing>
      <bpmn:outgoing>Flow_150xx07</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Activity_0ymp5qo" name="Reject claim">
      <bpmn:incoming>Flow_18bi0f6</bpmn:incoming>
      <bpmn:outgoing>Flow_1y1umcr</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_072pala" name="Arrange repair">
      <bpmn:incoming>Flow_150xx07</bpmn:incoming>
      <bpmn:outgoing>Flow_1wpewwy</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_16bxegr" name="Schedule payment">
      <bpmn:incoming>Flow_1wpewwy</bpmn:incoming>
      <bpmn:outgoing>Flow_16r8wmw</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_19776w0">
      <bpmn:incoming>Flow_1y1umcr</bpmn:incoming>
      <bpmn:incoming>Flow_16r8wmw</bpmn:incoming>
      <bpmn:outgoing>Flow_14udxnf</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Activity_19c3fj0" name="Notify customer">
      <bpmn:incoming>Flow_14udxnf</bpmn:incoming>
      <bpmn:outgoing>Flow_0bx1bv1</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="Event_1lkae47">
      <bpmn:incoming>Flow_0bx1bv1</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_1200nwn" sourceRef="Event_11hpg0d" targetRef="Activity_0686hn9" />
    <bpmn:sequenceFlow id="Flow_1gf4417" sourceRef="Activity_0686hn9" targetRef="Activity_1ydrt60" />
    <bpmn:sequenceFlow id="Flow_1d5516w" sourceRef="Activity_1ydrt60" targetRef="Activity_1awfkpk" />
    <bpmn:sequenceFlow id="Flow_0lvov8u" sourceRef="Activity_1awfkpk" targetRef="Activity_0xogugs" />
    <bpmn:sequenceFlow id="Flow_0htr0cu" sourceRef="Activity_0xogugs" targetRef="Gateway_0wp3q6n" />
    <bpmn:sequenceFlow id="Flow_18bi0f6" sourceRef="Gateway_0wp3q6n" targetRef="Activity_0ymp5qo" />
    <bpmn:sequenceFlow id="Flow_150xx07" sourceRef="Gateway_0wp3q6n" targetRef="Activity_072pala" />
    <bpmn:sequenceFlow id="Flow_1y1umcr" sourceRef="Activity_0ymp5qo" targetRef="Gateway_19776w0" />
    <bpmn:sequenceFlow id="Flow_1wpewwy" sourceRef="Activity_072pala" targetRef="Activity_16bxegr" />
    <bpmn:sequenceFlow id="Flow_16r8wmw" sourceRef="Activity_16bxegr" targetRef="Gateway_19776w0" />
    <bpmn:sequenceFlow id="Flow_14udxnf" sourceRef="Gateway_19776w0" targetRef="Activity_19c3fj0" />
    <bpmn:sequenceFlow id="Flow_0bx1bv1" sourceRef="Activity_19c3fj0" targetRef="Event_1lkae47" />
  </bpmn:process>
  <bpmn:process id="Process_1frlouu" isExecutable="false" />"""

        example_bpmn_text = """Corresponding textual process description for the BPMN model "Case 3-8: Claims Car Insurance":
The process "Claims Car Insurance" involves three pools as participants: the Customer, the Car Insurer, and the Garage. A Pool is the graphical representation of a Participant in a Collaboration.  

Within the Car Insurer, there are two roles involved reflected in three different lanes within the pool: the Notification department and the Handling department. A Lane is a sub-partition within a Pool and will extend the entire length of the Pool. Lanes are used to organize and categorize Activities. 

The process begins with a start event in the "Notification department" lane". As the name implies, the Start Event indicates where a particular Process will start. 

The Notification department first checks the "claim documentation" within the task "Check documentation". A Task is an atomic Activity that is included within a Process. A Task is used when the work in the Process is not broken down to a finer level of Process detail. In this case, the task requires Notification department to receive the message "claim documentation", which is sent by the "Customer" via a message flow. A Message Flow is used to show the flow of Messages between two Participants that are prepared to send and receive them. Once the documentation is checked, the claim is registered within the task "Register claim".

The Handling department then takes over. They first check the insurance in the task "Check Insurance". Once the insurance is verified, they perform an assessment in the task "Perform assessment". Based on the assessment, a decision is made at an exclusive gateway.  A diverging Exclusive Gateway (Decision) is used to create alternative paths within a Process flow, whereas only one of the paths can be taken.

If the claim is rejected, the "Reject claim" task is performed. If the claim is accepted, the insurer arranges for repair with the Garage in the task "Arrange repair" by sending the "Damage information" to the Garage via a message flow. 

Once the repair is arranged, the insurer schedules the payment in the task "Schedule payment". The "Payment details" are also sent to the Garage via a message flow. 

After either rejecting the claim or scheduling the payment, both path follow the path to the joining exclusive gateway. The Handling department notifies the customer in the task "Notify customer" by sending a "Notification letter" to the Customer via a message flow. 

The process ends once the customer has been notified with an end event. The End Event indicates where a Process will end."""

    elif example_BPMN_model_id == "5-1":

        example_bpmn_xml =  """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_0f1y8x3" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="5.11.0" modeler:executionPlatform="Camunda Cloud" modeler:executionPlatformVersion="8.2.0">
  <bpmn:process id="Process_03htkt1" isExecutable="true">
    <bpmn:startEvent id="Event_1haplvf" name="Receive Customer Request for Loan Amount">
      <bpmn:outgoing>Flow_0haw72c</bpmn:outgoing>
      <bpmn:messageEventDefinition id="MessageEventDefinition_1xqu562" />
    </bpmn:startEvent>
    <bpmn:sequenceFlow id="Flow_0haw72c" sourceRef="Event_1haplvf" targetRef="Activity_0mew4hd" />
    <bpmn:serviceTask id="Activity_0mew4hd" name="Invoke Risk Assessor">
      <bpmn:incoming>Flow_0haw72c</bpmn:incoming>
      <bpmn:outgoing>Flow_1ssbkxk</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:exclusiveGateway id="Gateway_0wr5ews" name="If" default="Flow_1wkq6qn">
      <bpmn:incoming>Flow_1ssbkxk</bpmn:incoming>
      <bpmn:outgoing>Flow_1wkq6qn</bpmn:outgoing>
      <bpmn:outgoing>Flow_0syi6i2</bpmn:outgoing>
      <bpmn:outgoing>Flow_0jjln2v</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:sequenceFlow id="Flow_1ssbkxk" sourceRef="Activity_0mew4hd" targetRef="Gateway_0wr5ews" />
    <bpmn:endEvent id="Event_1dp2hvv" name="Deny">
      <bpmn:incoming>Flow_1wkq6qn</bpmn:incoming>
      <bpmn:messageEventDefinition id="MessageEventDefinition_15az6ri" />
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_1wkq6qn" name="high risk" sourceRef="Gateway_0wr5ews" targetRef="Event_1dp2hvv" />
    <bpmn:endEvent id="Event_0morg0q" name="Approve">
      <bpmn:incoming>Flow_0syi6i2</bpmn:incoming>
      <bpmn:messageEventDefinition id="MessageEventDefinition_07pzry4" />
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_0syi6i2" name="low risk" sourceRef="Gateway_0wr5ews" targetRef="Event_0morg0q" />
    <bpmn:sequenceFlow id="Flow_0jjln2v" name="large loan or review risk" sourceRef="Gateway_0wr5ews" targetRef="Activity_095hifm" />
    <bpmn:serviceTask id="Activity_095hifm" name="Invoke Loan Approval">
      <bpmn:incoming>Flow_0jjln2v</bpmn:incoming>
      <bpmn:outgoing>Flow_0rs7474</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:endEvent id="Event_0cf4khv" name="Return Approval Response">
      <bpmn:incoming>Flow_0rs7474</bpmn:incoming>
      <bpmn:messageEventDefinition id="MessageEventDefinition_113rcgc" />
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_0rs7474" sourceRef="Activity_095hifm" targetRef="Event_0cf4khv" />
  </bpmn:process>"""

        example_bpmn_text = """The "Loan Request" process begins when a customer sends a request for a loan amount via a message, which triggers the message start event "Receive Customer Request for Loan Amount". A message start event waits for receiving a message from a Participant to start the Process.

Once the request is received, the process moves to the service task "Invoke Risk Assessor". A Service Task is a Task that uses some sort of service, which could be a Web service or an automated application. 

After the risk assessment, the process reaches an exclusive gateway named "If". A diverging Exclusive Gateway (Decision) is used to create alternative paths within a Process flow, whereas only one of the paths can be taken. In this case, the gateway represents a decision point in the process where the flow of control will diverge based on the risk assessment. This gateway thereby defines a default flow. 

If the risk is high, the process will follow the default sequence flow named "high risk", and reach the throwing message end event "Deny". This type of End event indicates that a Message is sent to a Participant at the conclusion of the Process.

If the risk is low, the process will follow the sequence flow named "low risk" and reach the throwing message end event "Approve". 
s
If the loan is large or the risk needs review, the process will follow the sequence flow named "large loan or review risk" and reach the service task "Invoke Loan Approval".

After the loan approval process, the process reaches the throwing message end event "Return Approval Response". 

In summary, this process model represents a loan request process where the loan request is received, the risk is assessed, a decision is made based on the risk assessment, and the decision is communicated back to the customer."""

    elif example_BPMN_model_id == "5-2":

        example_bpmn_xml =  """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_12ezxwz" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="5.11.0" modeler:executionPlatform="Camunda Cloud" modeler:executionPlatformVersion="8.2.0">
  <bpmn:collaboration id="Collaboration_00ysc3x">
    <bpmn:participant id="Participant_1bz00hb" name="Vacation Request 1.0" processRef="Process_1hn2uxf" />
  </bpmn:collaboration>
  <bpmn:process id="Process_1hn2uxf" isExecutable="true">
    <bpmn:laneSet id="LaneSet_1hwdigb">
      <bpmn:lane id="Lane_1n933pm" name="Employee">
        <bpmn:flowNodeRef>Event_0zd80m9</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0ct056h</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_0yafu3t</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_09o8qey" name="Boss">
        <bpmn:flowNodeRef>Activity_19gfqo5</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Activity_06o03mj</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Gateway_0zjhyi4</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="Lane_0v8xugs" name="Human Resource Assistant">
        <bpmn:flowNodeRef>Activity_1bzqmzl</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>Event_1tsa3fo</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>
    <bpmn:startEvent id="Event_0zd80m9" name="Start">
      <bpmn:outgoing>Flow_0r4ekz3</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:task id="Activity_0ct056h" name="Register Vacation Request">
      <bpmn:incoming>Flow_0r4ekz3</bpmn:incoming>
      <bpmn:outgoing>Flow_085ltgc</bpmn:outgoing>
    </bpmn:task>
    <bpmn:serviceTask id="Activity_19gfqo5" name="Verify Available Vacation Days">
      <bpmn:incoming>Flow_085ltgc</bpmn:incoming>
      <bpmn:outgoing>Flow_0ur7g8a</bpmn:outgoing>
    </bpmn:serviceTask>
    <bpmn:task id="Activity_06o03mj" name="Check Vacation Request">
      <bpmn:incoming>Flow_0ur7g8a</bpmn:incoming>
      <bpmn:outgoing>Flow_1tywisx</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_0zjhyi4">
      <bpmn:incoming>Flow_1tywisx</bpmn:incoming>
      <bpmn:outgoing>Flow_19ypldc</bpmn:outgoing>
      <bpmn:outgoing>Flow_0p6n7v8</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Activity_0yafu3t" name="Review Rejection Reason">
      <bpmn:incoming>Flow_19ypldc</bpmn:incoming>
      <bpmn:outgoing>Flow_0w0l1ln</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_1bzqmzl" name="Make Administrative Task">
      <bpmn:incoming>Flow_0p6n7v8</bpmn:incoming>
      <bpmn:outgoing>Flow_06xsayd</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="Event_1tsa3fo">
      <bpmn:incoming>Flow_06xsayd</bpmn:incoming>
      <bpmn:incoming>Flow_0w0l1ln</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_0r4ekz3" sourceRef="Event_0zd80m9" targetRef="Activity_0ct056h" />
    <bpmn:sequenceFlow id="Flow_085ltgc" sourceRef="Activity_0ct056h" targetRef="Activity_19gfqo5" />
    <bpmn:sequenceFlow id="Flow_0ur7g8a" sourceRef="Activity_19gfqo5" targetRef="Activity_06o03mj" />
    <bpmn:sequenceFlow id="Flow_1tywisx" sourceRef="Activity_06o03mj" targetRef="Gateway_0zjhyi4" />
    <bpmn:sequenceFlow id="Flow_19ypldc" name="No" sourceRef="Gateway_0zjhyi4" targetRef="Activity_0yafu3t" />
    <bpmn:sequenceFlow id="Flow_0p6n7v8" name="Yes" sourceRef="Gateway_0zjhyi4" targetRef="Activity_1bzqmzl" />
    <bpmn:sequenceFlow id="Flow_0w0l1ln" sourceRef="Activity_0yafu3t" targetRef="Event_1tsa3fo" />
    <bpmn:sequenceFlow id="Flow_06xsayd" sourceRef="Activity_1bzqmzl" targetRef="Event_1tsa3fo" />
  </bpmn:process>"""

        example_bpmn_text = """The process "Vacation Request 1.0" involves one main pool as participant "Vacation Request 1.0". A Pool is the graphical representation of a Participant in a Collaboration. Within this pool, three roles are involved reflected in three different lanes: Employee, Boss, and Human Resource Assistant.  A Lane is a sub-partition within a Pool and will extend the entire length of the Pool. Lanes are used to organize and categorize Activities. 

The process begins with a start event in the "Employee" lane". As the name implies, the Start Event indicates where a particular Process will start. The Employee initiates the process by registering a vacation request in the task "Register Vacation Request". A Task is an atomic Activity that is included within a Process. A Task is used when the work in the Process is not broken down to a finer level of Process detail. Once the request is registered, the process moves to the Boss's lane.

The Boss then verifies the available vacation days in the "Verify Available Vacation Days" service task. A Service Task is a Task that uses some sort of service, which could be a Web service or an automated application. After verifying the vacation days, the Boss checks the vacation request in the "Check Vacation Request" task. 

After checking the request, the process reaches a decision point, represented by the "Exclusive Gateway". A diverging Exclusive Gateway (Decision) is used to create alternative paths within a Process flow, whereas only one of the paths can be taken. If the request is rejected, the process follows the "No" path to the "Review Rejection Reason" task back in the Employee's lane. The Employee reviews the rejection reason.

If the request is approved, the process follows the "Yes" path to the "Make Administrative Task" task in the Human Resource Assistant's lane. The Human Resource Assistant then performs the administrative task.

The process ends with an end event when either the Employee reviews the rejection reason or the Human Resource Assistant completes the administrative task. The End Event indicates where a Process will end."""

    elif example_BPMN_model_id == "6-2":

        example_bpmn_xml =  """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_1x767qx" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="5.11.0" modeler:executionPlatform="Camunda Cloud" modeler:executionPlatformVersion="8.2.0">
  <bpmn:collaboration id="Collaboration_1a32ji5">
    <bpmn:participant id="Participant_162ui5k" name="Supplier" processRef="Process_17uzqt4" />
    <bpmn:participant id="Participant_1ug52fc" name="Assembler AG" processRef="Process_0yqlgvw" />
    <bpmn:messageFlow id="Flow_0xbqisa" sourceRef="Activity_05ur72l" targetRef="Activity_0dv571v" />
    <bpmn:messageFlow id="Flow_13qagn9" sourceRef="Activity_1tr0g0r" targetRef="Activity_0hw1wev" />
  </bpmn:collaboration>
  <bpmn:process id="Process_17uzqt4" isExecutable="true">
    <bpmn:task id="Activity_0dv571v" name="Process Order">
      <bpmn:outgoing>Flow_1y50ogp</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_1tr0g0r" name="Send Invoice">
      <bpmn:incoming>Flow_1y50ogp</bpmn:incoming>
    </bpmn:task>
    <bpmn:sequenceFlow id="Flow_1y50ogp" sourceRef="Activity_0dv571v" targetRef="Activity_1tr0g0r" />
  </bpmn:process>
  <bpmn:process id="Process_0yqlgvw" isExecutable="false">
    <bpmn:startEvent id="Event_0whvdvf" name="1st each month">
      <bpmn:outgoing>Flow_0gue98o</bpmn:outgoing>
      <bpmn:timerEventDefinition id="TimerEventDefinition_11ca7lk" />
    </bpmn:startEvent>
    <bpmn:task id="Activity_05ur72l" name="Create Order">
      <bpmn:incoming>Flow_0gue98o</bpmn:incoming>
      <bpmn:outgoing>Flow_149sld7</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_0hw1wev" name="Receive Invoice">
      <bpmn:incoming>Flow_149sld7</bpmn:incoming>
      <bpmn:outgoing>Flow_1nnkzh5</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="Event_0s53iso">
      <bpmn:incoming>Flow_1nnkzh5</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_0gue98o" sourceRef="Event_0whvdvf" targetRef="Activity_05ur72l" />
    <bpmn:sequenceFlow id="Flow_149sld7" sourceRef="Activity_05ur72l" targetRef="Activity_0hw1wev" />
    <bpmn:sequenceFlow id="Flow_1nnkzh5" sourceRef="Activity_0hw1wev" targetRef="Event_0s53iso" />
  </bpmn:process>"""

        example_bpmn_text = """The "Ordering" process involves two main pools as participants: "Supplier" and "Assembler AG". A Pool is the graphical representation of a Participant in a Collaboration.

The process starts at "Assembler AG" with the timer start event "1st each month". A timer start event is triggered by a defined time-date or cycle (e.g., every Monday at 9am). In this case, the timer start event is triggered on the 1st of each month. After the start event is triggered, the first task is "Create Order". A Task is an atomic Activity that is included within a Process. A Task is used when the work in the Process is not broken down to a finer level of Process detail. In this case, the task involves creating an order. 

Once the order is created, it is sent to the "Supplier" via a message flow. This is represented by the message flow from "Create Order" in the Assembler AG pool to "Process Order" in the Supplier pool. A Message Flow is used to show the flow of Messages between two Participants that are prepared to send and receive them. While the Assembler Ag then waits for the invoice, the "Supplier" processes the order, which is represented by the task "Process Order".

After processing the order, the "Supplier" sends an invoice to "Assembler AG" in the task "Send Invoice". This is represented by the message flow from "Send Invoice" in the "Supplier" pool to "Receive Invoice" in the Assembler AG pool. The task "Receive Invoice" at "Assembler AG" represents the receipt of the invoice from the "Supplier".

Finally, the process at "Assembler AG" ends after the invoice is received. This is represented by the end event following the "Receive Invoice" task. The End Event indicates where a Process will end.

In summary, the process involves creating an order at "Assembler AG", sending it to the "Supplier", processing the order at the "Supplier", sending an invoice back to "Assembler AG", and receiving the invoice at "Assembler AG"."""

    elif example_BPMN_model_id == "8-2":

        example_bpmn_xml =  """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_19usbo1" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="5.11.0" modeler:executionPlatform="Camunda Cloud" modeler:executionPlatformVersion="8.2.0">
  <bpmn:collaboration id="Collaboration_12wu3o2">
    <bpmn:participant id="Participant_1j58fpd" name="HR Check" processRef="Process_0bit9t5" />
    <bpmn:participant id="Participant_1xtpo9z" name="Head of functional department" />
    <bpmn:messageFlow id="Flow_0h2idds" sourceRef="Participant_1xtpo9z" targetRef="Event_1brfzur" />
    <bpmn:messageFlow id="Flow_1hie6vs" sourceRef="Activity_1w1j62h" targetRef="Participant_1xtpo9z" />
    <bpmn:messageFlow id="Flow_0oc9eso" sourceRef="Participant_1xtpo9z" targetRef="Activity_1w1j62h" />
    <bpmn:messageFlow id="Flow_07q2rdj" sourceRef="Activity_0xqhmdb" targetRef="Participant_1xtpo9z" />
    <bpmn:messageFlow id="Flow_186drs6" sourceRef="Participant_1xtpo9z" targetRef="Event_0hpm4jf" />
    <bpmn:messageFlow id="Flow_003ev7x" sourceRef="Activity_15sh5ab" targetRef="Participant_1xtpo9z" />
    <bpmn:messageFlow id="Flow_144imhr" sourceRef="Participant_1xtpo9z" targetRef="Event_1buxx76" />
  </bpmn:collaboration>
  <bpmn:process id="Process_0bit9t5" isExecutable="true">
    <bpmn:startEvent id="Event_1brfzur" name="vacancy is reported">
      <bpmn:outgoing>Flow_0ohjt2x</bpmn:outgoing>
      <bpmn:messageEventDefinition id="MessageEventDefinition_0apa537" />
    </bpmn:startEvent>
    <bpmn:task id="Activity_0qjo343" name="review report">
      <bpmn:incoming>Flow_0ohjt2x</bpmn:incoming>
      <bpmn:outgoing>Flow_1b6bsrc</bpmn:outgoing>
    </bpmn:task>
    <bpmn:exclusiveGateway id="Gateway_166q4xg" name="Everything all right?">
      <bpmn:incoming>Flow_1b6bsrc</bpmn:incoming>
      <bpmn:outgoing>Flow_0xzv2y6</bpmn:outgoing>
      <bpmn:outgoing>Flow_1cieovx</bpmn:outgoing>
    </bpmn:exclusiveGateway>
    <bpmn:task id="Activity_1w1j62h" name="ask for details and requirements">
      <bpmn:incoming>Flow_0xzv2y6</bpmn:incoming>
      <bpmn:outgoing>Flow_0ffil64</bpmn:outgoing>
    </bpmn:task>
    <bpmn:task id="Activity_0xqhmdb" name="create job description">
      <bpmn:incoming>Flow_0ffil64</bpmn:incoming>
      <bpmn:incoming>Flow_1cieovx</bpmn:incoming>
      <bpmn:outgoing>Flow_0gw3us9</bpmn:outgoing>
    </bpmn:task>
    <bpmn:eventBasedGateway id="Gateway_018x86s">
      <bpmn:incoming>Flow_0gw3us9</bpmn:incoming>
      <bpmn:incoming>Flow_1lc75yp</bpmn:incoming>
      <bpmn:outgoing>Flow_0ijgo7h</bpmn:outgoing>
      <bpmn:outgoing>Flow_1raoshf</bpmn:outgoing>
    </bpmn:eventBasedGateway>
    <bpmn:intermediateCatchEvent id="Event_0hpm4jf" name="corrections are required">
      <bpmn:incoming>Flow_0ijgo7h</bpmn:incoming>
      <bpmn:outgoing>Flow_0mbzw3c</bpmn:outgoing>
      <bpmn:messageEventDefinition id="MessageEventDefinition_09e6ur2" />
    </bpmn:intermediateCatchEvent>
    <bpmn:task id="Activity_15sh5ab" name="correct job description">
      <bpmn:incoming>Flow_0mbzw3c</bpmn:incoming>
      <bpmn:outgoing>Flow_1lc75yp</bpmn:outgoing>
    </bpmn:task>
    <bpmn:intermediateCatchEvent id="Event_1buxx76" name="job description is approved">
      <bpmn:incoming>Flow_1raoshf</bpmn:incoming>
      <bpmn:outgoing>Flow_0ie3e2s</bpmn:outgoing>
      <bpmn:messageEventDefinition id="MessageEventDefinition_1fih5sp" />
    </bpmn:intermediateCatchEvent>
    <bpmn:task id="Activity_1r0ek8r" name="advertise post">
      <bpmn:incoming>Flow_0ie3e2s</bpmn:incoming>
      <bpmn:outgoing>Flow_04fifkr</bpmn:outgoing>
    </bpmn:task>
    <bpmn:endEvent id="Event_12fpmh8" name="post is avertised">
      <bpmn:incoming>Flow_04fifkr</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_0ohjt2x" sourceRef="Event_1brfzur" targetRef="Activity_0qjo343" />
    <bpmn:sequenceFlow id="Flow_1b6bsrc" sourceRef="Activity_0qjo343" targetRef="Gateway_166q4xg" />
    <bpmn:sequenceFlow id="Flow_0xzv2y6" sourceRef="Gateway_166q4xg" targetRef="Activity_1w1j62h" />
    <bpmn:sequenceFlow id="Flow_1cieovx" sourceRef="Gateway_166q4xg" targetRef="Activity_0xqhmdb" />
    <bpmn:sequenceFlow id="Flow_0ffil64" sourceRef="Activity_1w1j62h" targetRef="Activity_0xqhmdb" />
    <bpmn:sequenceFlow id="Flow_0gw3us9" sourceRef="Activity_0xqhmdb" targetRef="Gateway_018x86s" />
    <bpmn:sequenceFlow id="Flow_1lc75yp" sourceRef="Activity_15sh5ab" targetRef="Gateway_018x86s" />
    <bpmn:sequenceFlow id="Flow_0ijgo7h" sourceRef="Gateway_018x86s" targetRef="Event_0hpm4jf" />
    <bpmn:sequenceFlow id="Flow_1raoshf" sourceRef="Gateway_018x86s" targetRef="Event_1buxx76" />
    <bpmn:sequenceFlow id="Flow_0mbzw3c" sourceRef="Event_0hpm4jf" targetRef="Activity_15sh5ab" />
    <bpmn:sequenceFlow id="Flow_0ie3e2s" sourceRef="Event_1buxx76" targetRef="Activity_1r0ek8r" />
    <bpmn:sequenceFlow id="Flow_04fifkr" sourceRef="Activity_1r0ek8r" targetRef="Event_12fpmh8" />
  </bpmn:process>"""

        example_bpmn_text = """The process "Job posting" involves two main pools as participants: the "Head of functional department" and the "HR Check". A Pool is the graphical representation of a Participant in a Collaboration.

The process starts at "HR Check" with the message start event "vacancy is reported". A message start event waits for receiving a message from a Participant to start the Process. In this case, "HR Check" waits for the message sent by "Head of functional department" via a message flow. A Message Flow is used to show the flow of Messages between two Participants that are prepared to send and receive them. This message then triggers the start of the process. The first task of "HR Check" is to review the report (Task: review report). A Task is an atomic Activity that is included within a Process. A Task is used when the work in the Process is not broken down to a finer level of Process detail. After reviewing, a decision is made whether everything is alright with the report (Exclusive Gateway: Everything all right?). A diverging Exclusive Gateway (Decision) is used to create alternative paths within a Process flow, whereas only one of the paths can be taken. 

If there are issues with the report, the "HR Check" asks the "Head of functional department" for more details and requirements (Task: ask for details and requirements) via a message flow. Once the details and requirements are received from the "Head of functional department", the "HR Check" proceeds to create a job description (Task: create job description). 

If there were no issues with the report, the "HR Check" directly proceeds to create a job description. The "HR Check" then send the created job description to the "Head of functional department" via a message flow.  

After the job description is created and sent, the process flow reaches an event-based gateway. The Event-Based Gateway represents a branching point in the Process where the alternative paths that follow the Gateway are based on Events that occur. In this case, two possible events can occur. Either corrections are required (Message Intermediate Catch Event: corrections are required) or the job description is approved (Message Intermediate Catch Event: job description is approved). A Message Intermediate Catch Event can be used to receive a Message. This causes the Process to continue if it was waiting for the Message. 

In this case, "HR Check" waits for the message from the "Head of functional department" if "corrections are required" or the "job description is approved". If corrections are required, the "HR Check" corrects the job description (Task: correct job description). The "HR Check" then sends the corrected job description to the "Head of functional department" via a message flow. The process loops back to the event-based gateway, repeating the flow from the event-based gateway.

If the job description is approved by the "Head of functional department" via a message flow, the "HR Check" proceeds to advertise the post (Task: advertise post). The process ends when the post is advertised (End Event: post is advertised). The End Event indicates where a Process will end."""

    return example_bpmn_xml, example_bpmn_text 