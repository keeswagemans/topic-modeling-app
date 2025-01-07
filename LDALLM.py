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
parameters = json.load(open("parameters.json"))  
min_cf = parameters["min_cf"]    
min_df = parameters["min_df"]   
top_words = parameters["top_words"] 
number_topics = parameters["number_topics"] 
alpha = parameters["alpha"]  
eta = parameters["eta"] 


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

        # Retrieve the topics and their corresponding words 
        topics_ls = []
        for i in range(number_topics): 
            topic = mdl.get_topic_words(i) 
            # topic_words = [word for word, _ in topic[:min_cf]]   
            topics_ls.append(topic) 
        
        return topics_ls 
    
    @staticmethod  
    def topics_llm(llm, input_dict,min_cf, min_df, rm_top=top_words, k=number_topics, eta=eta, corpus=corpus): 
        
        list_of_topicwords = LDALLM.LDA(input_dict, corpus, min_cf, min_df, top_words, number_topics, eta)
        
        string_lda = ""
        for list in list_of_topicwords: 
            string_lda += str(list) + "\n" 
            
        # Create the template
        template_string = '''Describe the topic of each of the {num_topics} 
            double-quote delimited lists in a simple sentence and also write down 
            three possible different subthemes. The lists are the result of an 
            algorithm for topic discovery.
            Do not provide an introduction or a conclusion, only describe the 
            topics. Do not mention the word "topic" when describing the topics.
            Use the following template for the response.

            1: <<<(sentence describing the topic)>>>
            - <<<(Phrase describing the first subtheme)>>>
            - <<<(Phrase describing the second subtheme)>>>
            - <<<(Phrase describing the third subtheme)>>>

            2: <<<(sentence describing the topic)>>>
            - <<<(Phrase describing the first subtheme)>>>
            - <<<(Phrase describing the second subtheme)>>>
            - <<<(Phrase describing the third subtheme)>>>

            ...

            n: <<<(sentence describing the topic)>>>
            - <<<(Phrase describing the first subtheme)>>>
            - <<<(Phrase describing the second subtheme)>>>
            - <<<(Phrase describing the third subtheme)>>>

            Lists: """{string_lda}""" '''

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
response = LDALLM.topics_llm(llm, dictionary, min_cf, min_df, top_words, number_topics, eta, corpus)
print(response) 
