"""
This is the main page, that you have to run with "streamlit run streamlit_app.py" in the terminal. 
Streamlit automatically create the tabs in the left sidebar from the .py files located in /pages.
Here we just have the home page, with a short description of the tabs, and some images.
    
"""

import streamlit as st  
from pathlib import Path 
import streamlit.components.v1 as components 

# Set the page config    
st.set_page_config(
    page_title="DeepCivic",
    layout="centered"
)

# Load fonts 
with open("style_header.html", "r", encoding="utf-8") as f:
    html_header = f.read()
with open("style_body.html", "r", encoding="utf-8") as f:
    html_body = f.read()   


# Main title 
html_filled = html_header.replace("{{content_header}}", "DeepCivic")
components.html(html_filled, height=150) 

# Image 
st.image('media/Gemini_Generated_Image_z5i16oz5i16oz5i1.jpg')

# Main text
st.markdown(html_body, unsafe_allow_html=True)   
st.markdown(
    """
    <div class="rijk-body">
    
    <p>DeepCivic kan gebruikt worden om topics (thema’s) te genereren uit tekstcorpora. Het bestaat uit drie modellen: LDA, BERTopic en LDA met een LLM.</p>
    
    <p>Voordat de modellen getraind kunnen worden, dien je documenten te oploaden. Dit kan gedaan worden in de Documenten Manager. Na het toevoegen van de documenten kun je de teksten extraheren en preprocessen. Dit is nodig om de tekst voor de analyse te kunnen gebruiken.</p>
    
    <p>In de tabbladen Latent Dirichlet Allocation, Latent Dirichlet Allocation met Large Language Model en BERTopic kun je de modellen trainen. De resultaten en visualisaties van de modellen zijn te downloaden in de respectievelijke tab.</P> 
    
    <p>De features die je links kunt ontdekken:</p>

    <li>Klik op BERTopic om een BERTopic model te trainen.</li> 
    
    <li>Klik op BERTopic vs. Latent Dirichlet Allocation vs. Latent Dirichlet Allocation met Large Language Model om de verschillen tussen de drie te ontdekken.</li> 
    
    <li>Klik op Documenten Manager om documenten toe te voegen en de teksten te extraheren en te preprocessen. Dit moet je voor elke analyse doen.</li> 

    <li>Klik op Latent Dirichlet Allocation om een LDA model te trainen.</li> 

    <li>Klik op Latent Dirichlet Allocation met Large Language model om een LDA te trainen en deze vervolgens te laten interpreteren door een Large Language Model.</li> 
    
    """, unsafe_allow_html=True 
) 

