# Import libraries 
import streamlit as st
import pandas as pd 
import subprocess 
from subprocess import Popen 
import os 
from pathlib import Path 
import tempfile 
import json 


LOCAL_REPO_PATH = os.path.join(os.getcwd(), "documenten")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Over project', 'Documenten Manager', 'Preprocessing', 'Over LDA', 'LDA', 'Over LLM LDA', 'LLM LDA']) 
                                            

with tab1: 
    st.title("Topic Modeling voor het ministerie van Sociale Zaken en Werkgelegenheid")
    st.video("video.mp4", start_time=0, loop=True) 
    text = "De modellen in deze webapp kunnen gebruikt worden om topics te modelleren uit tekstcorpora. Voordat de modellen getraind kunnen worden, dienen documenten geüpload te worden. Dit kan gedaan worden in de Documenten Manager. Na het toevoegen van de documenten kunnen de teksten geëxtraheerd worden onder hetzelfde kopje. Daarna kunnen de teksten gepreprocessed worden. In datzelfde tabblad kunnen woorden gekozen worden, die uit de tekstcorpus verwijdert dienen te worden. In Over LDA en Over BERTopic worden de modellen kort toegelicht. In de tabbladen LDA en BERTopic kunnen de parameters voor de modellen gekozen worden en kan het model getraind worden. De resultaten en visualisaties van de modellen zijn te downloaden in de respectievelijke tab."
    paragraphs = text.split("/n/n")
    for i, paragraph in enumerate(paragraphs, 1):
        st.write(paragraph)

      
with tab2: 
    st.title("Documenten Manager") 
    st.write("") 
        
    st.markdown("""
            <style>
            .stButton>button
                    {
            width: 340px;
            background-color: #01689b; 
            color: white; 
            margin: 0 auto; 
            }
            </style>
            """, unsafe_allow_html=True)

    os.makedirs(LOCAL_REPO_PATH, exist_ok=True)  # Ensure the directory exists

    # Create a two-column layout
    col1, col2 = st.columns(2)

    # Button to get list of documents in the repository
    with col1:
            uploaded_files = st.file_uploader("Kies een PDF of DOCX bestand.", type=["pdf", "docx"], accept_multiple_files=True)   

            if uploaded_files:
                if st.button("Documenten uploaden en teksten extraheren"): 
                    for uploaded_file in uploaded_files: 
                        try:
                            save_path = os.path.join("documenten/", uploaded_file.name)
                            with open(save_path, "wb") as f: 
                                f.write(uploaded_file.getvalue())
                            st.success(f"Document {uploaded_file.name} succesvol geupload.")
                            st.info(f"Bestand opgeslagen in {save_path}")
                        except Exception as e:
                            st.error(f"Er is een fout opgetreden met {uploaded_file.name}: {e}.")
                
                    try:
                        result = subprocess.run(["python", "extracttext.py"], capture_output=True, text=True)
                        st.success("Documenten succesvol geupload en teksten succesvol geëxtraheerd uit bestanden.")
                        st.code(result.stdout)
                    except Exception as e:
                        st.error(f"Fout bij extraheren teksten: {e}.") 
            
    with col2:  
        if st.button("Verkrijg lijst van de documenten in de map"):
            # List the files in the local repository
            documents = os.listdir(LOCAL_REPO_PATH)
            if documents:
                st.write("Documenten die beschikbaar zijn in de map:")
                for document in documents:
                    st.markdown('''
                                <style>
                                    - [data-testid="stMarkdownContainer"] ul{
                                padding-left:40px;v
                                }
                                </style>
                                ''', unsafe_allow_html=True) 
                    st.markdown(document)   
            else:
                st.write("Nog geen documenten in de map gevonden.")
            
        if st.button("Extraheer teksten uit bestanden"):
            result = subprocess.run(["python", "extracttext.py"])
            st.success("Teksten succesvol geëxtraheerd uit bestanden.")
            # st.code(result.stdout) 

        
with tab3: 
    st.title("Preprocessing")
    st.write("Links kun je woorden intikken om te verwijderen, druk op enter en klik vervolgens op de knop 'Verwijder woorden' rechts. Wil je geen woorden verwijderen, druk dan gelijk op de knop 'Preprocessing'. Eerst preprocessen voodat je woorden verwijdert, is raadzaam.")
    col1, col2 = st.columns(2)

    st.markdown("""
            <style>
            .stButton>button {
            width: 340px;
            background-color: #01689b; 
            color: white; 
            }
            </style>
            """, unsafe_allow_html=True)

    with col1: 
        words_to_remove_input = st.text_input("Woorden om te verwijderen (gescheiden door komma's):")
        if words_to_remove_input:
            words_to_remove = [word.strip() for word in words_to_remove_input.split(",")]
        else:
            words_to_remove = [] 

    with col2: 
        if st.button("Preprocessing"): 
            st.write("Er wordt aan gewerkt!")
           
            result = subprocess.run(["python", "preprocess.py"], shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Preprocessing voltooid!")
            else:
                st.error("Er is een fout opgetreden!")
                st.code(result.stderr)
                
        remove_button = st.button("Verwijder woorden")          
        if remove_button: 
            if words_to_remove: 
                words_to_remove = [word.lower() for word in words_to_remove] 
                json.dump(words_to_remove, open("preprocessing/words_to_remove.json", "w")) 
                result = subprocess.run(["python", "remove_words.py"], capture_output=True, text=True)
                st.write("Woorden uit tekstcorpus gehaald")
            else: 
                st.write("Er zijn geen woorden om te verwijderen.")
    
            
with tab4: 
    st.title("Over LDA") 
    st.write("Hieronder komt een schematische weergave van wat een Latent Dirichlet Allocation-model is.") 

with tab5: 
    st.title("Latent Dirichlet Allocation") 
    st.write("Kies hieronder de parameters voor het trainen van het Latent Dirichlet Allocation-model. Voor een uitvoerige beschrijving van het Latent Dirichlet Allocation-model, bekijk het tabblad 'Over LDA'. De parameters  die voor het LDA-model gebruikt worden zijn:") 
    st.markdown("- Minimale collectiefrequentie van woorden: Het minimale aantal keren dat een woord in de gehele corpus moet voorkomen om opgenomen te worden in de analyse. Woorden die minder vaak voorkomen, worden verwijderd. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. De bovengrens is 10000.")
    st.markdown("- Minimale documentfrequentie van woorden: Het minimale aantal documenten waarin een woord moet voorkomen. Woorden die minder vaak voorkomen dan de gespecifideerde waarde, worden uitgesloten. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. De bovengrens is 10000. Alle woorden die aan deze grens voldoen, worden in deze analyse meegenomen.")
    st.markdown("- Aantal te verwijderen 'top'-woorden: Het aantal meest voorkomende woorden in de corpus dat verwijderd wordt. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. Alle woorden die voldoen aan deze drempel worden meegenomen in de analyse.")
    st.markdown("- K (aantal topics): Het aantal topics dat door het model gegenereerd moet worden. Kies een waarde tussen 1 ~ 32676.")
    st.markdown("- Alpha is de hyperparameter van de Dirichlet-verdeling voor de documenten-topicverdeling. Kies voor een symmetric prior of een asymmetric prior. Kijk in 'Over LDA' voor meer informatie.")
    st.markdown("- Eta is de hyperparameter van de Dirichlet-verdeling voor de topic-woordverdeling. Een assymetrische eta zorgt ervoor dat sommige woorden prominenter in de topics voorkomen. Keuze tussen 0 en 1.")
    
    st.markdown('''
                <style>
                [data-testid="stMarkdownContainer"] ul{
                    list-style-position: inside;
                    list-style-type: square;
                    }
                    </style>
                    ''', unsafe_allow_html=True
                    )
    
    col1, col2 = st.columns(2) 
    
    with col1: 
        # Define form_callback 
        def form_callback():
            # Save session state values to an external file
            parameters = {
                "min_cf": min_cf_input,
                "min_df": min_df_input,
                "top_words": top_words_input,
                "number_topics": number_topics_input,
                "alpha": alpha_input,
                "eta": eta_input
            }
            with open("parameters.json", "w") as f:
                json.dump(parameters, f)
        
        # Initialize the parameters for training the LDA model
        with st.form(key="my_form"):
            min_cf_input = st.number_input(label="Minimale collectie frequentie van woorden:", min_value=0, max_value=10000, value=0, key="min_cf")
            min_df_input = st.number_input(label="Minimale documentfrequentie van woorden:", min_value=0, max_value=10000, value=0, key="min_df")  
            top_words_input = st.number_input(label="Aantal te verwijderen 'top-woorden:", min_value=0, max_value=10000, value=5, key="top_words") 
            number_topics_input = st.number_input(label=' K (het aantal topics)', min_value=1, max_value=20, value=20, key="number_topics")
            alpha_input = st.radio("Alpha:", ["symmetric", "asymmetric"], key="alpha")  
            eta_input = st.slider("Eta:", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="eta") 
            submit_button = st.form_submit_button(label="Leg parameters vast", on_click=form_callback)
    
    with col2:  
        # Initialize the state variables and initialize the button for results and visualization   
        if "results_ready" not in st.session_state:
            st.session_state.results_ready = False   
        if "results_file_path" not in st.session_state:  
            st.session_state.results_file_path = None
        if "visualization_file_path" not in st.session_state:   
            st.session_state.visualization_file_path = None 
            
        # Verkrijg resultaten en visualisatie 
        if st.button("Verkrijg resultaten en visualisatie!"):
            st.write("Het Latent Dirichlet Allocation Model is aan het trainen. De resultaten en de visualisatie verschijnen in een klikbare link.")
            result = subprocess.run(["python", "lda.py"], shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                st.success("LDA model is voltooid!")
                split_output = result.stdout.split("|")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                    processed_content = "<br>".join(split_output)
                    tmp_file.write(processed_content.encode("utf-8"))
                    st.session_state.results_file_path = Path(tmp_file.name)     
                    
                st.session_state.results_ready = True 
                
                st.write("De visualisatie wordt gegenereerd...")
                
                result_visualization = subprocess.run(["python", "visualization.py"], shell=True, capture_output=True, text=True)    

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
                                 
with tab6: 
    st.title("Over LLM LDA") 
    st.write("Op de volgende pagina kan een LDA met een Large Language Model getraind worden. De resultaten van het model kunnen eveneens gedownload worden. Een Large Language Model draait via de Azure Cloud, dat betekent dat alleen openbare documenten in dit model kunnen worden getraind. Hier documenten ingooien die niet-openbaar zijn, leidt tot een datalek. De parameters zijn hetzelfde en die kun je op de volgende pagina ook aanpassen. Succes!") 

with tab7: 
    st.title("LLM LDA")
    st.write("LET OP: Dit model draait via de Azure Cloud. Alleen openbare documenten in dit model trainen.") 
    
    col1, col2 = st.columns(2) 
    
    with col1: 
        # Define form_callback 
        def form_callback2(): 
            # Save session state values to an external file
            parameters = {
                "min_cf2": min_cf_input,
                "min_df2": min_df_input,
                "top_words2": top_words_input,
                "number_topics2": number_topics_input,
                "alpha2": alpha_input,
                "eta2": eta_input
            }
            with open("parameters2.json", "w") as f:
                json.dump(parameters, f)
        
        # Initialize the parameters for training the LDA model
        with st.form(key="my_form2"): 
            min_cf_input = st.number_input(label="Minimale collectie frequentie van woorden:", min_value=0, max_value=10000, value=0, key="min_cf2") 
            min_df_input = st.number_input(label="Minimale documentfrequentie van woorden:", min_value=0, max_value=10000, value=0, key="min_df2") 
            top_words_input = st.number_input(label="Aantal te verwijderen 'top-woorden:", min_value=0, max_value=10000, value=5, key="top_words2") 
            number_topics_input = st.number_input(label=' K (het aantal topics)', min_value=1, max_value=20, value=20, key="number_topics2") 
            alpha_input = st.radio("Alpha:", ["symmetric", "asymmetric"], key="alpha2") 
            eta_input = st.slider("Eta:", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="eta2") 
            submit_button = st.form_submit_button(label="Leg parameters vast", on_click=form_callback2) 
    
    with col2: 
        # Define session states 
        if "results_ready_llm_lda" not in st.session_state:  
            st.session_state.results_ready_llm_lda = False 
        if "results_file_path_llm_lda" not in st.session_state:  
            st.session_state.results_file_path_llm_lda = None 
        # if "visualization_file_path_llm_lda" not in st.session_state:   
        #     st.session_state.visualization_file_path_llm_lda = None 
        
        # Verkrijg resultaten en visualisatie    
        if st.button("Verkrijg resultaten en visualisatie van het lDA-model met een Large Language Model!"): 
            st.write("De resultaten en de visualisatie verschijnen in een klikbare link.")   
            result = subprocess.run(["python", "LDALLM.py"], shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("LLM LDA model is voltooid!")
                output = result.stdout   
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                    tmp_file.write(output.encode("utf-8")) 
                    st.session_state.results_file_path_llm_lda = Path(tmp_file.name)     
                
                st.session_state.results_ready_llm_lda = True 
                
                # st.write("De visualisatie wordt gegenereerd...")
                result_visualization_llm = subprocess.run(["python", "visualization_llm.py"], shell=True, capture_output=True, text=True) 
                  
                # Visualization section
                # if result_visualization_llm.returncode == 0:
                #     st.success("Resultaten en visualisatie zijn voltooid!")
                #     st.session_state.visualization_file_path_llm_lda = "models/ldavis_llm.html" 
                # else:
                #     st.error("Er is een fout opgetreden bij het genereren van de visualisatie!") 
                #     st.write(result_visualization_llm.stderr) 
            else: 
                st.error("Er is een fout opgetreden bij het genereren van de resultaten en de visualisatie!")
                st.write(result.stderr) 
                    
        if st.session_state.results_ready_llm_lda: 
            st.write("De resultaten zijn klaar!") 
            with open(st.session_state.results_file_path_llm_lda, "rb") as file: 
                st.download_button(label="Klik hier om de resultaten te downloaden",
                                    data=file, 
                                    file_name="llm_lda_results.txt",
                                    mime="text/plain")  
            
            # if st.session_state.visualization_file_path_llm_lda: 
            #     with open(st.session_state.visualization_file_path_llm_lda, "r") as file:
            #         html_content = file.read()
                    
            #     st.download_button(label="Klik om de visualisatie te downloaden",
            #                         data=html_content,
            #                         file_name="ldavis_llm.html",
            #                         mime="text/html")
        