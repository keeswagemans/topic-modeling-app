import streamlit as st 
import json 
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
html_filled = html_header.replace("{{content_header}}", "Latent Dirichlet Allocation")
components.html(html_filled, height=150)   

st.markdown(html_body, unsafe_allow_html=True) 
st.markdown(
"""
Latent Dirichlet Allocation (LDA) is een krachtige techniek die wordt gebruikt om verborgen thema's in een verzameling documenten te ontdekken. Het uitgangspunt van LDA is dat elk document een mix is van verschillende onderwerpen en dat elk onderwerp een mix is van woorden. Stel je voor dat je een verzameling artikelen hebt over verschillende onderwerpen zoals sport, politiek en technologie. LDA probeert te achterhalen welke onderwerpen in elk artikel voorkomen en welke woorden bij elk onderwerp horen. 

Het proces begint met het willekeurig toewijzen van woorden aan onderwerpen. Vervolgens wordt dit proces herhaaldelijk aangepast om de waarschijnlijkheid te maximaliseren dat de woorden bij de juiste onderwerpen horen. Uiteindelijk resulteert dit in een set onderwerpen met bijbehorende woorden en een verdeling van onderwerpen over de documenten. Dit maakt het mogelijk om patronen en trends in grote hoeveelheden tekst te ontdekken, wat bijzonder nuttig is in gebieden zoals tekstmining en data-analyse. 

LDA wordt veel toegepast in verschillende domeinen, zoals het analyseren van nieuwsartikelen, wetenschappelijke papers en sociale media. Door de verborgen thema's in teksten te identificeren, kunnen onderzoekers en analisten waardevolle inzichten verkrijgen en beter begrijpen welke onderwerpen in een bepaalde verzameling documenten domineren.  

Voor meer informatie kun je de volgende studie bekijken: 

Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. In jmlr.org. Journal of Machine Learning. https://proceedings.neurips.cc/paper/2001/file/296472c9542ad4d4788d543508116cbc-Paper.pdf

""" 
) 

# st.markdown("Kies hieronder de parameters voor het trainen van het Latent Dirichlet Allocation-model. De parameters  die voor het LDA-model gebruikt worden zijn:") 
# st.markdown("- Minimale collectiefrequentie van woorden: Het minimale aantal keren dat een woord in de gehele corpus moet voorkomen om opgenomen te worden in de analyse. Woorden die minder vaak voorkomen, worden verwijderd. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. De bovengrens is 10000.")
# st.markdown("- Minimale documentfrequentie van woorden: Het minimale aantal documenten waarin een woord moet voorkomen. Woorden die minder vaak voorkomen dan de gespecifideerde waarde, worden uitgesloten. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. De bovengrens is 10000. Alle woorden die aan deze grens voldoen, worden in deze analyse meegenomen.")
# st.markdown("- Aantal te verwijderen 'top'-woorden: Het aantal meest voorkomende woorden in de corpus dat verwijderd wordt. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. Alle woorden die voldoen aan deze drempel worden meegenomen in de analyse.")
# st.markdown("- K (aantal topics): Het aantal topics dat door het model gegenereerd moet worden. Kies een waarde tussen 1 ~ 32676.")
# st.markdown("- Alpha is de hyperparameter van de Dirichlet-verdeling voor de documenten-topicverdeling. Kies voor een symmetric prior of een asymmetric prior. Symmetric betekent voor alle topics dezelfde prior. Asymmetric betekent dat sommige topics prominenter zijn dan andere, afhankelijk van de specifiek afgestemde alpha.")    
# st.markdown("- Eta is de hyperparameter van de Dirichlet-verdeling voor de topic-woordverdeling. Een assymetrische eta zorgt ervoor dat sommige woorden prominenter in de topics voorkomen. Keuze tussen 0 en 1.")

# st.markdown('''
#             <style>
#             [data-testid="stMarkdownContainer"] ul{
#                 list-style-position: inside;
#                 list-style-type: square;
#                 }
#                 </style>
#                 ''', unsafe_allow_html=True
#                 )

col1, col2 = st.columns(2) 

with col1: 
    def form_callback(): 
        # Store variables in dictionary 
        parameters = {
            "min_cf": min_cf_input,
            "min_df": min_df_input,
            "top_words": top_words_input,
            "number_topics": number_topics_input,
            "alpha_input": alpha_input,
            "eta": eta_input
        }
        
        with open("parameters/parameters.json", "w") as f: 
            json.dump(parameters, f)
                    
    # Initialize the parameters for training the LDA model
    with st.form(key="my_form"):
        min_cf_input = 0 
        min_df_input = 0
        top_words_input = 0
        number_topics_input = st.number_input(label="K (het aantal topics)", min_value=1, max_value=20, key="number_topics") 
        alpha_input = 0.01
        eta_input = 0.01
        submit_button = st.form_submit_button(label="Leg vast", on_click=form_callback)
        if submit_button:
            st.write("Parameters vastgelegd!") 

with col2:  
    # Initialize the state variables and initialize the button for results and visualization   
    if "results_ready" not in st.session_state:
        st.session_state.results_ready = False   
    if "results_file_path" not in st.session_state:  
        st.session_state.results_file_path = False
    if "visualization_file_path" not in st.session_state:   
        st.session_state.visualization_file_path = False
        
    # Verkrijg resultaten en visualisatie 
    if st.button("Verkrijg resultaten en visualisatie!"):
        st.write("Het Latent Dirichlet Allocation Model is aan het trainen. De resultaten en de visualisatie verschijnen in een klikbare link.")
        result = subprocess.run(["python", "functions/Latent Dirichlet Allocation.py"], shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            st.success("LDA model is voltooid!")
            split_output = result.stdout.split("|")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                processed_content = "<br>".join(split_output)
                tmp_file.write(processed_content.encode("utf-8"))
                st.session_state.results_file_path = Path(tmp_file.name)     
                
            st.session_state.results_ready = True 
            
            st.write("De visualisatie wordt gegenereerd...")
            
            result_visualization = subprocess.run(["python", "functions/visualization.py"], shell=True, capture_output=True, text=True)    

            # Visualization section
            if result_visualization.returncode == 0:
                st.success("Resultaten en visualisatie zijn voltooid!")
                st.session_state.visualization_file_path = "models/ldavis.html"  
            else:
                st.error("Er is een fout opgetreden bij het genereren van de visualisatie!") 
                st.write(result_visualization.stderr) 
        else: 
            st.error("Er is een fout opgetreden bij het genereren van de resultaten en de visualisatie!")
            st.write(result.stderr) 
            
    if st.session_state.results_ready: 
        st.write("De resultaten zijn klaar!") 
        with open(st.session_state.results_file_path, "rb") as file: 
            st.download_button(label="Klik hier om de resultaten te downloaden",
                                data=file, 
                                file_name="lda_results.txt",
                                mime="text/plain") 
            
        if st.session_state.visualization_file_path:
            with open(st.session_state.visualization_file_path, "r") as file:
                html_content = file.read()
                
            st.download_button(label="Klik om de visualisatie te downloaden",
                                data=html_content,
                                file_name="ldavis.html",
                                mime="text/html")