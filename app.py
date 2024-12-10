import streamlit as st
import subprocess 
import os 
from pathlib import Path 
import tempfile 

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
            st.write("Working on it!")
            result = subprocess.run(["python", "preprocess.py"], shell=True, capture_output=True, text=True)
            
            if result.returncode == 0: 
                st.success("Preprocessing voltooid!")
            else:
                st.error("Er is een fout opgetreden!")
                st.code(result.stderr)

        if st.select_slider(label='Number of topics', options=[x for x in range(1,21)], value=[1,20]): 
            st.write("Thanks!")

    with col2: 
        if st.button("Get results"):
            st.write("Training the Latent Dirichlet Allocation model for you and returning the results in a visualization.")
            
            # Run the LDA script
            result = subprocess.run(
                ["python", "C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/topic-modeling-app/latentdirichletallocation/lda.py"],
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                st.success("LDA model is voltooid!")
                
                # Save the output to an HTML file for visualization
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                    tmp_file.write(result.stdout.encode("utf-8"))
                    temp_file_path = Path(tmp_file.name)
                
                # Create a downloadable link
                with open(temp_file_path, "rb") as file:
                    btn = st.download_button(
                        label="Klik om de resultaten te bekijken",
                        data=file,
                        file_name="lda_visualization.html",
                        mime="text/html"
                    )
            else:
                st.error("Er is een fout opgetreden!")
                
                # Save the error details to a text file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                    tmp_file.write(result.stderr.encode("utf-8"))
                    temp_file_path = Path(tmp_file.name)
                
                # Create a downloadable link for the error log
                with open(temp_file_path, "rb") as file:
                    btn = st.download_button(
                        label="Klik hier om de foutdetails te bekijken",
                        data=file,
                        file_name="error_details.txt",
                        mime="text/plain"
                    )

        if st.select_slider(label='Number of topics within document', options=[x for x in range(1,21)], value=[1,20]): 
            st.write('Thanks!')


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
            st.write("Working on it!")
        if st.select_slider(label='Number of topics!', options=[x for x in range(1,21)], value=[1,20]): 
            st.write("Thanks!")

    with col2: 
        if st.button("Get results!"):
            st.write("Training the Latent Dirichlet Allocation model for you and returning the results in a visualization.")
        if st.select_slider(label='Number of topics within document!', options=[x for x in range(1,21)], value=[1,20]): 
            st.write('Thanks!') 

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

    st.title("Document Repository Manager")

    # Create a two-column layout
    col1, col2 = st.columns(2)

    # Button to get list of documents in the repository
    with col1:
        if st.button("Get list of documents in repository!"):
            # List the files in the local repository
            documents = os.listdir(LOCAL_REPO_PATH)
            if documents:
                st.write("Documents available in the repository:")
                st.write(", ".join(documents))
            else:
                st.write("No documents found in the repository yet.")

        with col2:
            uploaded_files = st.file_uploader("Choose a PDF or DOCX file to upload.", type=["pdf", "docx"], accept_multiple_files=True)

            if uploaded_files:
                if st.button("Documenten uploaden en teksten extraheren"): 
                    for uploaded_file in uploaded_files: 
                        try:
                            save_path = os.path.join("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/documenten/", uploaded_file.name)
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
            
