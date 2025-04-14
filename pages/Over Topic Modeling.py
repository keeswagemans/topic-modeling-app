import streamlit as st 
import streamlit.components.v1 as components   

# Load fonts 
with open("style_header.html", "r", encoding="utf-8") as f:
    html_header = f.read()  
with open ("style_body.html", "r", encoding="utf-8") as f:
    html_body = f.read()   
    
# Title 
html_filled = html_header.replace("{{content_header}}", "Over Topic Modeling")
components.html(html_filled, height=150)
    
# Main text 
st.markdown(html_body, unsafe_allow_html=True) 
st.markdown("""
Topic modeling is een techniek binnen natuurlijke taalverwerking (NLP) die wordt gebruikt om automatisch thema’s of onderwerpen te ontdekken in een verzameling documenten. Het doel van topic modeling is om verborgen patronen in teksten te identificeren, zoals onderwerpen die vaak samen voorkomen, zonder dat er vooraf specifieke labels aan de teksten zijn gegeven. 

Veelgebruikte methoden voor topic modeling zijn Latent Dirichlet Allocation (LDA) en BERTopic. LDA zoekt naar een set van onderwerpen die de teksten het beste beschrijven door te kijken naar de frequentie en co-occurrence van woorden, terwijl BERTopic gebruik maakt van neural networks en BERT-embeddings voor het ontdekken van meer complexe, semantische structuren in de teksten.

Topic modeling wordt veel toegepast in verschillende domeinen, zoals het analyseren van klantfeedback, het ontdekken van trends in wetenschappelijke artikelen, of het organiseren van grote hoeveelheden tekstdata. Het helpt bedrijven en onderzoekers om snel inzicht te krijgen in de onderliggende thema's binnen een corpus van documenten.
""")