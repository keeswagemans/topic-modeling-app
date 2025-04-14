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
import logging 
import sys 

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO  
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout)) 

# Import variables 
parameters = json.load(open("parameters/parameters2.json")) 
min_cf = parameters["min_cf2"]   
min_df = parameters["min_df2"]  
top_words = parameters["top_words2"]
number_topics = parameters["number_topics2"]
alpha_raw = parameters["alpha2"]
eta = parameters["eta2"]

# def change_alpha(alpha_raw): 
#     if alpha_raw == "": 
#         alpha = None 
#     if "," in alpha_raw: 
#         alpha = [float(x.strip()) for x in alpha_raw.split(",")]
#     else:
#         alpha = float(alpha_raw)
#     return alpha 

# alpha = change_alpha(alpha_raw)

class LDALLM():
    
    def __init__(self, data, min_cf, min_df, top_words, number_topics, eta): 
        self.data = data 
        self.min_cf = min_cf
        self.min_df = min_df
        self.top_words = top_words
        self.number_topics = number_topics 
        self.alpha_raw = alpha_raw 
        self.eta = eta 
        
    def change_alpha(alpha_raw): 
        if alpha_raw =="0.0": 
            alpha = float(0.1)   
        if "," in alpha_raw:
            alpha = [float(x.strip()) for x in alpha_raw.split(",")]
        else:
            alpha = float(alpha_raw)
        return alpha 
    
    def corpus(data): 
        
        """
        This function creates a corpus object from the data.
        
        """
        
        corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
        corpus.process(data)
        
        return corpus 
    
    def LDA(input_dict, corpus, min_cf, min_df, top_words, number_topics, eta): 
        
        """
        This function trains an LDA model on the data and saves the model to the specified path. 
        
        """
        mdl = tp.LDAModel(tw=tp.TermWeight.ONE, 
                          min_cf=min_cf, 
                          min_df=min_df, 
                          rm_top=top_words, 
                          k=number_topics, 
                          eta=eta, 
                          corpus=corpus) 
        
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
    
    def topics_llm(llm, input_dict, min_cf, min_df, rm_top=top_words, k=number_topics, eta=eta, corpus=corpus): 
        
        list_of_topicwords = LDALLM.LDA(input_dict, corpus, min_cf, min_df, top_words, number_topics, eta)
        
        string_lda = ""
        for list in list_of_topicwords: 
            string_lda += str(list) + "\n" 
            
        # Create the template
        template_string = """
        Voor elk van de {num_topics} onderwerpen, geef eerst een korte beschrijving, dan een korte beschrijvende zin, en dan vier aanvullende details die de subthema's verduidelijken. Gebruik het onderstaande format: 

        ### Onderwerp 1
        
        Hoofdthema: [Eenvoudige beschrijving van het hoofdonderwerp]  
        [Zin die het hoofdonderwerp omschrijft]
        1. [Frase die het eerste subthema omschrijft]
        2. [Frase die het tweede subthema omschrijft] 
        3. [Frase die het derde subthema omschrijft] 
        4. [Frase die het vierde subthema omschrijft] 
        
        ### Onderwerp 2
        
        Hoofdthema: [Eenvoudige beschrijving van het hoofdonderwerp]  
        [Zin die het hoofdonderwerp omschrijft]
        1. [Frase die het eerste subthema omschrijft]
        2. [Frase die het tweede subthema omschrijft] 
        3. [Frase die het derde subthema omschrijft] 
        4. [Frase die het vierde subthema omschrijft] 
        
        ...
`
        ### Onderwerp n
        
        Hoofdthema: [Eenvoudige beschrijving van het hoofdonderwerp]  
        [Zin die het hoofdonderwerp omschrijft]
        1. [Frase die het eerste subthema omschrijft]
        2. [Frase die het tweede subthema omschrijft] 
        3. [Frase die het derde subthema omschrijft] 
        4. [Frase die het vierde subthema omschrijft] 
        
        Lists: '''{string_lda}''' """
        
        # LLM call
        prompt_template = ChatPromptTemplate.from_template(template_string)
        chain = LLMChain(llm=llm, prompt=prompt_template) 
        for key, value in dictionary.items(): 
            string_text = " ".join(value)    
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
response = LDALLM.topics_llm(llm, dictionary, min_cf, min_df, top_words, number_topics, eta, corpus)
corpus.save("models/corpus_llm.cps") 
print(response) 
