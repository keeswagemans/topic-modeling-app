import tomotopy as tp 
import json 
import openai 
from openai import AzureOpenAI 
from langchain.llms import OpenAI 
from langchain.chains import LLMChain 
from langchain.prompts import ChatPromptTemplate 
from langchain_core.runnables import Runnable 
from langchain.chat_models import AzureChatOpenAI 

from llama_index.llms.azure_openai import AzureOpenAI    
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding 
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReading
import logging 
import sys 

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO  
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout)) 

# Import variables 
parameters = json.load(open("parameters2.json")) 
min_cf = parameters["min_cf2"]   
min_df = parameters["min_df2"]  
top_words = parameters["top_words2"]
number_topics = parameters["number_topics2"]
alpha = parameters["alpha2"]
eta = parameters["eta2"]

class LDALLM(): 
    
    @staticmethod 
    def corpus(data): 
        
        """
        This function creates a corpus object from the data.
        
        """
        
        corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
        corpus.process(data)
        
        return corpus 
    
    @staticmethod 
    def LDA(input_dict, corpus, min_cf, min_df, top_words, number_topics, eta): 
        
        """
        This function trains an LDA model on the data and saves the model to the specified path. 
        
        """
        mdl = tp.LDAModel(tw=tp.TermWeight.ONE, min_cf=min_cf, min_df=min_df, rm_top=top_words, k=number_topics, eta=eta, corpus=corpus) # Add alpha as parameter 
        
        for pdf, words in input_dict.items():
            mdl.add_doc(words)   
        
        mdl.train(10000, show_progress=True)
        
        mdl.save("models/lda_model_llm.bin", True) 

        # Retrieve the topics and their corresponding words 
        topics_ls = []
        for i in range(number_topics): 
            topic = mdl.get_topic_words(i) 
            # topic_words = [word for word, _ in topic[:min_cf]]   
            topics_ls.append(topic) 
        
        return topics_ls 
    
    @staticmethod  
    def topics_llm(llm, input_dict, min_cf, min_df, rm_top=top_words, k=number_topics, eta=eta, corpus=corpus): 
        
        list_of_topicwords = LDALLM.LDA(input_dict, corpus, min_cf, min_df, top_words, number_topics, eta)
        
        string_lda = ""
        for list in list_of_topicwords: 
            string_lda += str(list) + "\n" 
            
        # Create the template
        template_string = '''
        Beschrijf het onderwerp van elk van de {num_topics} dubbel aanhalingstekens omgeven lijsten in een eenvoudige zin en schrijf daarnaast drie mogelijke verschillende subthema's op. De lijsten zijn het resultaat van een algoritme voor het ontdekken van onderwerpen.  
        Geef geen introductie of conclusie, beschrijf alleen de onderwerpen. Vermeld het woord "onderwerp" niet bij het beschrijven van de onderwerpen.  
        Gebruik het volgende sjabloon voor de reactie.  

        1: <<<(zin die het onderwerp beschrijft)>>>
        - <<<(Frase die het eerste subthema beschrijft)>>>
        - <<<(Frase die het tweede subthema beschrijft)>>>
        - <<<(Frase die het derde subthema beschrijft)>>>

        2: <<<(zin die het onderwerp beschrijft)>>>
        - <<<(Frase die het eerste subthema beschrijft)>>>
        - <<<(Frase die het tweede subthema beschrijft)>>>
        - <<<(Frase die het derde subthema beschrijft)>>>

        ...

        n: <<<(zin die het onderwerp beschrijft)>>>
        - <<<(Frase die het eerste subthema beschrijft)>>>
        - <<<(Frase die het tweede subthema beschrijft)>>>
        - <<<(Frase die het derde subthema beschrijft)>>>

        Lijsten: """{string_lda}"""
        '''
        
        template_string2 = '''
        Beschrijf het onderwerp van elk van de {num_topics} dubbel aanhalingstekens omgeven lijsten met een woord en schrijf daarnaast vier woorden die de verschillende subthema's beschrijven. De woorden zijn het resultaat van een algoritme voor het ontdekken van onderwerpen. 
        Geef geen introductie of conclusie, beschrijf alleen de onderwerpen. Vermeld het woord "onderwerp" niet bij het beschrijven van de onderwerpen.  
        Gebruik het volgende sjabloon voor de reactie. 
        
        1: <<<(woord dat het onderwerp beschrijft)>>>
        - <<<(woord dat het eerste subthema beschrijft)>>>
        - <<<(woord dat het tweede subthema beschrijft)>>>
        - <<<(woord dat het derde subthema beschrijft)>>>
        
        2: <<<(woord dat het onderwerp beschrijft)>>>   
        - <<<(woord dat het eerste subthema beschrijft)>>>
        - <<<(woord dat het tweede subthema beschrijft)>>>
        - <<<(woord dat het derde subthema beschrijft)>>>
        
        ...
        
        n: <<<(woord dat het onderwerp beschrijft)>>>
        - <<<(woord dat het eerste subthema beschrijft)>>>
        - <<<(woord dat het tweede subthema beschrijft)>>>
        - <<<(woord dat het derde subthema beschrijft)>>>
        
        Woorden: """{string_lda}"""  
        '''


        # LLM call
        prompt_template = ChatPromptTemplate.from_template(template_string)
        chain = LLMChain(llm=llm, prompt=prompt_template) 
        response = chain.run({
            "string_lda" : string_lda,
            "num_topics" : number_topics 
            })

        return response

#Set up the llm
api_type = "azure" 
api_key = "ChciroJAUkT4AOFa7GOu9RaXxvwPdFQHkbaAJ8La5ObUTuBhvJNTJQQJ99AKACYeBjFXJ3w3AAAAACOGphGX" 
azure_endpoint = "https://premi0648592--openai.cognitiveservices.azure.com/openai/deployments/gpt-4o-szw/chat/completions?api-version=2024-08-01-preview" 
api_version = "2024-10-01-preview" 
deployment_name = "gpt-4o-szw" 


llm = AzureChatOpenAI( 
    model="gpt-4o",
    azure_deployment=deployment_name, 
    api_key=api_key,
    azure_endpoint=azure_endpoint, 
    api_version=api_version,
) 
        
dictionary = json.load(open("preprocessing/preprocessing.json"))
data = dictionary.values()
final_data = [item for sublist in data for item in sublist]
corpus = LDALLM.corpus(dictionary) 
corpus.save("models/corpus_llm.cps") 
response = LDALLM.topics_llm(llm, dictionary, min_cf, min_df, top_words, number_topics, eta, corpus)
print(response) 
