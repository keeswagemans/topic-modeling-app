# Import libraries 
import streamlit as st
import subprocess 
import os 
from pathlib import Path 
import tempfile 
import json 


LOCAL_REPO_PATH = os.path.join(os.getcwd(), "documenten")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Over project', 'Documenten Manager', 'Preprocessing', 'Over LDA', 'LDA', 'Over BERTopic', 'BERTopic'])  
                                            

with tab1: 
    st.title("Topic Modeling voor het ministerie van Sociale Zaken en Werkgelegenheid")
    text = "Het Latent Dirichlet Allocation (LDA)-model is ontworpen om kernonderwerpen binnen documenten te identificeren. Dit model kan het Ministerie van Sociale Zaken en Werkgelegenheid ondersteunen bij het proactief openbaar maken van documenten over onderwerpen die waarschijnlijk van publiek belang zijn. Naast het traditionele LDA-model is er ook een alternatief beschikbaar: het BERTopic-model. /n/n LDA is een probabilistisch model dat documenten analyseert door deze op te splitsen in een combinatie van onderwerpen. Elk onderwerp wordt gekarakteriseerd door een verzameling woorden met een bepaalde waarschijnlijkheid. Het model biedt een eenvoudige en snelle manier om documenten te groeperen op basis van deze onderwerpen, wat het geschikt maakt voor basisanalyses van grote datasets. \n\n Het BERTopic-model gaat een stap verder door gebruik te maken van transformer-gebaseerde taalmodellen zoals BERT. Deze modellen begrijpen de semantische betekenis van woorden en zinnen en zetten deze om in numerieke representaties (embeddings). BERTopic clustert deze representaties en bepaalt welke clusters als onderwerpen gelden. Dit maakt het model bijzonder effectief in het detecteren van onderwerpen in complexe of lange teksten. Bovendien biedt BERTopic de mogelijkheid om dynamisch onderwerpen te genereren, waardoor het flexibeler en nauwkeuriger is dan LDA.\n\n Het belangrijkste verschil tussen beide modellen is hun aanpak. LDA richt zich op afzonderlijke woorden en gebruikt statistische verbanden om onderwerpen te definiëren, terwijl BERTopic zinnen semantisch begrijpt en daardoor dieper inzicht biedt. Waar LDA eenvoudiger en sneller is, levert BERTopic rijkere en meer gedetailleerde inzichten. Dit maakt LDA geschikt voor basisanalyses, terwijl BERTopic ideaal is voor het analyseren van complexe beleidsdocumenten.\n\n Voor het Ministerie kan het gebruik van beide modellen nuttig zijn, afhankelijk van de mate van detail en precisie die nodig is. BERTopic is bij uitstek geschikt wanneer de focus ligt op een diepere interpretatie van teksten, terwijl LDA kan worden ingezet voor bredere, minder gedetailleerde analyses."
    paragraphs = text.split("/n/n")
    for i, paragraph in enumerate(paragraphs, 1):
        st.write(paragraph)
        
with tab2: 
    st.title("Documenten Manager") 
    st.write("De Documenten Manager is de pagina waar men documenten kan uploaden en en teksten uit de bestanden kan extraheren. De geëxtraheerde teksten worden vervolgens gebruikt voor de preprocessing en het trainen van de modellen.") 
        
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
            result = subprocess.run(["python", "extracttext.py"], capture_output=True, text=True)
            st.success("Teksten succesvol geëxtraheerd uit bestanden.")
            # st.code(result.stdout) 

        
with tab3: 
    st.title("Preprocessing")
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
           
            result = subprocess.run(["python", "/preprocess.py"], shell=True, capture_output=True, text=True)
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
    st.write("Kies hieronder de parameters voor het trainen van het Latent Dirichlet Allocation-model. Druk links op trainen om het model te trainen.") 
    
    col1, col2 = st.columns(2) 
    
    with col1: 
        inner_topics = st.slider(label='Hoeveelheid topics', min_value=1, max_value=20, value=20, key=2) 
        st.write(inner_topics) 
        
        number_topics_bert = st.slider(label='Het aantal topics!', min_value=1, max_value=20, value=20, key=3)  
        st.write(number_topics_bert)
        
    with col2: 
        if "results_ready" not in st.session_state:
            st.session_state.results_ready = False   
        if "results_file_path" not in st.session_state:  
            st.session_state.results_file_path = None
        if "visualization_file_path" not in st.session_state:   
            st.session_state.visualization_file_path = None 
            
        
        if st.button("Verkrijg resultaten en visualisatie!"):
            st.write("Het Latent Dirichlet Model is aan het trainen. De resultaten en de visualisatie verschijnen in een klikbare link.")
            result = subprocess.run(["python", "latent-dirichlet-allocation/lda.py"], shell=True, capture_output=True, text=True)

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
    st.title("Over BERTopic") 
    st.write("Hieronder komt een schematische weergave van wat een BERTopic-model is.") 
    
with tab7: 
    st.title("BERTopic") 
    st.write("Kies links de paramaters voor het trainen van het BERTopic-model. Druk rechts op trainen om het model te trainen.") 

            
