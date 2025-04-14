# Load libraries 
import streamlit as st 
import subprocess   
import tempfile 
from pathlib import Path  
import streamlit.components.v1 as components        

# Load fonts 
with open("style_header.html", "r", encoding="utf-8") as f:
    html_header = f.read()
with open("style_body.html", "r", encoding="utf-8") as f:
    html_body = f.read()
    
# Main title 
html_filled = html_header.replace("{{content_header}}", "BERTopic")
components.html(html_filled, height=150) 

# Main text 
st.markdown(html_body, unsafe_allow_html=True) 
st.markdown(
"""
BERTopic is een geavanceerde techniek voor topic modeling die gebruik maakt van moderne taalmodellen zoals BERT (Bidirectional Encoder Representations from Transformers) en c-TF-IDF (class-based Term Frequency-Inverse Document Frequency) om betekenisvolle clusters en onderwerpen te creëren. Het doel van BERTopic is om gemakkelijk interpreteerbare onderwerpen te genereren terwijl belangrijke woorden in de beschrijvingen van de onderwerpen behouden blijven. 

Het proces begint met het gebruik van BERT om tekstuele gegevens om te zetten in hoge-dimensionale vectoren die de semantische betekenis van de woorden vastleggen. Deze vectoren worden vervolgens geclusterd om groepen van gerelateerde documenten te vormen. Door c-TF-IDF toe te passen, kan BERTopic de belangrijkste woorden binnen elk cluster identificeren, wat helpt bij het beschrijven van de onderwerpen op een begrijpelijke manier. 

Een van de sterke punten van BERTopic is de flexibiliteit en de mogelijkheid om verschillende technieken te ondersteunen, zoals zero-shot topic modeling, waarbij nieuwe onderwerpen kunnen worden geïdentificeerd zonder voorafgaande training, en het gebruik van seed words om specifieke onderwerpen te sturen. Dit maakt BERTopic bijzonder nuttig voor het analyseren van grote hoeveelheden tekst en het ontdekken van verborgen patronen en trends. 

In de praktijk wordt BERTopic veel gebruikt in verschillende domeinen, zoals het analyseren van klantfeedback, het monitoren van sociale media en het verkennen van wetenschappelijke literatuur. Door de kracht van moderne taalmodellen te benutten, biedt BERTopic een robuuste en efficiënte manier om inzicht te krijgen in de inhoud van grote tekstcorpora.  

Kijk naar de onderstaande studie voor meer informatie:  

Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. arXiv (Cornell University). https://doi.org/10.48550/arxiv.2203.05794

"""
)

if "results_file_path_bertopic" not in st.session_state:    
    st.session_state.results_file_path_bertopic = None 
if "results_ready_bertopic" not in st.session_state:     
    st.session_state.results_ready_bertopic = False  

st.write("Druk hieronder op de knop om het model te laten lopen.")

if st.button("Train BERTopic model"): 
    st.write("Het BERTopic model is op dit moment aan het trainen.") 
    
    result = subprocess.run(["python", "functions/BERTopic.py"], shell=True, capture_output=True, text=True) 
    
    if result.returncode == 0: 
        st.success("BERTopic model is voltooid!")
        output = result.stdout 
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            tmp_file.write(output.encode("utf-8")) 
            st.session_state.results_file_path_bertopic = Path(tmp_file.name) 
        
        st.session_state.results_ready_bertopic = True 
        
    else: 
        st.error("Er is een fout opgetreden!") 
        st.write(result.stderr) 

if st.session_state.results_ready_bertopic: 
    st.write("De resultaten zijn klaar!")    
    with open(st.session_state.results_file_path_bertopic, "rb") as file:    
        st.download_button(label="Klik hier om de resultaten te downloaden", 
                            data=file, 
                            file_name="bertopic_results.txt", 
                            mime="text/plain") 
        
st.write("______________________________________________________________")

        
