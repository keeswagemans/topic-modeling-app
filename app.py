# Import libraries 
import streamlit as st
import subprocess 
import os 
from pathlib import Path 
import tempfile 
import webbrowser 
import json 
from preprocess import Preprocess    

LOCAL_REPO_PATH = os.path.join(os.getcwd(), "documenten")

tab1, tab2, tab3, tab4 = st.tabs(['Over project', 'LDA', 'BERTopic', 'Documenten'])

with tab1: 
    st.title("Topic Modeling voor het Ministerie van Sociale Zaken en Werkgelegenheid")
    text = "Het Latent Dirichlet Allocation (LDA)-model is ontworpen om kernonderwerpen binnen documenten te identificeren. Dit model kan het Ministerie van Sociale Zaken en Werkgelegenheid ondersteunen bij het proactief openbaar maken van documenten over onderwerpen die waarschijnlijk van publiek belang zijn. Naast het traditionele LDA-model is er ook een alternatief beschikbaar: het BERTopic-model. /n/n LDA is een probabilistisch model dat documenten analyseert door deze op te splitsen in een combinatie van onderwerpen. Elk onderwerp wordt gekarakteriseerd door een verzameling woorden met een bepaalde waarschijnlijkheid. Het model biedt een eenvoudige en snelle manier om documenten te groeperen op basis van deze onderwerpen, wat het geschikt maakt voor basisanalyses van grote datasets. \n\n Het BERTopic-model gaat een stap verder door gebruik te maken van transformer-gebaseerde taalmodellen zoals BERT. Deze modellen begrijpen de semantische betekenis van woorden en zinnen en zetten deze om in numerieke representaties (embeddings). BERTopic clustert deze representaties en bepaalt welke clusters als onderwerpen gelden. Dit maakt het model bijzonder effectief in het detecteren van onderwerpen in complexe of lange teksten. Bovendien biedt BERTopic de mogelijkheid om dynamisch onderwerpen te genereren, waardoor het flexibeler en nauwkeuriger is dan LDA.\n\n Het belangrijkste verschil tussen beide modellen is hun aanpak. LDA richt zich op afzonderlijke woorden en gebruikt statistische verbanden om onderwerpen te definiëren, terwijl BERTopic zinnen semantisch begrijpt en daardoor dieper inzicht biedt. Waar LDA eenvoudiger en sneller is, levert BERTopic rijkere en meer gedetailleerde inzichten. Dit maakt LDA geschikt voor basisanalyses, terwijl BERTopic ideaal is voor het analyseren van complexe beleidsdocumenten.\n\n Voor het Ministerie kan het gebruik van beide modellen nuttig zijn, afhankelijk van de mate van detail en precisie die nodig is. BERTopic is bij uitstek geschikt wanneer de focus ligt op een diepere interpretatie van teksten, terwijl LDA kan worden ingezet voor bredere, minder gedetailleerde analyses."
    paragraphs = text.split("/n/n")
    for i, paragraph in enumerate(paragraphs, 1):
        st.write(paragraph)
        
with tab2:  
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
        if st.button("Preprocessing"): 
            st.write("Er wordt aan gewerkt!")
            result = subprocess.run(["python", "preprocess.py"], shell=True, capture_output=True, text=True)
            
            if result.returncode == 0: 
                st.success("Preprocessing voltooid!")
            else:
                st.error("Er is een fout opgetreden!")
                st.code(result.stderr)

        number_topics = st.slider(label='Hoeveelheid topics', min_value=1, max_value=20, value=20, key=1) 
        st.write("Geselecteerde aantal topics: ", number_topics)
        
        words_to_remove_input = st.text_input("Woorden om te verwijderen (gescheiden door komma's):")
        if words_to_remove_input:
            words_to_remove = [word.strip() for word in words_to_remove_input.split(",")]
        else:
            words_to_remove = [] 

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
            
            else: 
                st.error("Er is een fout opgetreden bij het genereren van de resultaten en de visualisatie!")
        
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
            
                # if st.button("Open visualisatie in browser"):
                #     webbrowser.open_new_tab(st.session_state.visualization_file_path) 
                    
                                
        inner_topics = st.slider(label='Hoeveelheid topics', min_value=1, max_value=20, value=20, key=2) 
        st.write(inner_topics)
        
        remove_button = st.button("Verwijder woorden") 
        if remove_button: 
            if words_to_remove: 
                words_to_remove = [word.lower() for word in words_to_remove] 
                data = json.load(open("preprocessing/preprocessing.json"))   
                filter_words = Preprocess.remove_custom_filterwords(data, words_to_remove)
                json.dump(filter_words, open("preprocessing/preprocessing.json", "w"))
                st.write("Woorden verwijdert")
            else: 
                st.write("Er zijn geen woorden om te verwijderen.")

with tab3:
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
        if st.button("Preprocessing!"): 
            st.write("Er wordt achter de schermen keihard gewerkt!")
        number_topics_bert = st.slider(label='Het aantal topics!', min_value=1, max_value=20, value=20, key=3)  
        st.write(number_topics_bert)
         
    with col2: 
        if st.button("Verkrijg resultaten!"):
            st.write("Het Latent Dirichlet Model is aan het trainen. De resultaten verschijnen in een klikbare link zodra de machine klaar is.")
        inner_topics_bert = st.slider(label='Het aantal topics in de documenten!', min_value=1, max_value=20, value=20, key=4)
        st.write(inner_topics_bert) 

with tab4: 
    col1, col2, col3 = st.columns(3)

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

    st.title("Documenten Manager")

    # Create a two-column layout
    col1, col2 = st.columns(2)

    # Button to get list of documents in the repository
    with col1:
        if st.button("Verkrijg lijst van de documenten in de map!"):
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
                
        if st.button("Extraheer teksten uit bestanden!"): 
            result = subprocess.run(["python", "extracttext.py"], capture_output=True, text=True)
            st.success("Teksten succesvol geëxtraheerd uit bestanden.")
            # st.code(result.stdout) 

        with col2:
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
            
