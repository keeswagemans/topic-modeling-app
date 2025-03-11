# Import libraries 
import streamlit as st
import subprocess 
import os 
from pathlib import Path 
import tempfile 
import json 
import glob 

with open("styles.css") as f:   
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) 

LOCAL_REPO_PATH = os.path.join(os.getcwd(), "documenten")

# Center an image using HTML and CSS
st.markdown(
    """
    <style>
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


tab1, tab2, tab3, tab4, tab5, tab6 =  st.tabs(['Over project', 
                                         'Documenten', 
                                         'Preprocessing',  
                                         'LDA',
                                         'LLM LDA',
                                         'BERTopic'])
                                            
with tab1: 
    custom = f"<p style='font-size:65px; font-weight:bold'; align:center>DeepCivic</p>" 
    st.markdown(custom, unsafe_allow_html=True)
    st.image("media/Gemini_Generated_Image_z5i16oz5i16oz5i1.jpg")
    
    text = """
        DeepCivic kan gebruikt worden om topics (thema’s) te genereren uit tekstcorpora. Het bestaat uit drie modellen: LDA, BERTopic en LDA met een LLM. /n/n 
        Voordat de modellen getraind kunnen worden, dienen documenten geüpload te worden. Dit kan gedaan worden in de Documenten Manager. Na het toevoegen van de documenten kunt u de teksten extraheren door op de knop te drukken onder hetzelfde kopje. Onder het kopje preprocessen, kunt u de tekst preprocessen (tekst gereed maken voor de analyse) en kunt u woorden verwijderen die u niet in de analyse wenst te hebben. /n/n
        In de tabbladen LDA, LLM LDA en BERTopic kunnen de parameters voor de modellen gekozen worden en kunnen de modellen getraind worden. Daar vind je ook informatie over de modellen. De resultaten en visualisaties van de modellen zijn te downloaden in de respectievelijke tab.
    """   
      
    paragraphs = text.split("/n/n")
    for i, paragraph in enumerate(paragraphs, 1):
        st.write(paragraph)
    
      
with tab2: 
    custom_tab2 =     custom = f"<p style='font-size:65px; font-weight:bold'>Documenten Manager</p>" 
    st.markdown(custom_tab2, unsafe_allow_html=True)     
        
    os.makedirs(LOCAL_REPO_PATH, exist_ok=True)  # Ensure the directory exists

    # Create a two-column layout
    col1, col2 = st.columns(2)

    # Set variables 
    if "uploader_key" not in st.session_state: 
        st.session_state.uploader_key = 0 
        
    
    # Button to get list of documents in the repository
    with col1:
            uploaded_files = st.file_uploader("Kies een PDF of DOCX bestand.", type=["pdf", "docx"], accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")   
               

            if uploaded_files:
                if st.button("Documenten uploaden"): 
                    for uploaded_file in uploaded_files: 
                        try:
                            save_path = os.path.join("documenten/", uploaded_file.name)
                            with open(save_path, "wb") as f: 
                                f.write(uploaded_file.getvalue())
                            st.success(f"Document {uploaded_file.name} succesvol geupload.")
                            st.info(f"Bestand opgeslagen in {save_path}")
                        except Exception as e:
                            st.error(f"Er is een fout opgetreden met {uploaded_file.name}: {e}.")
                
    with col2:  
        if st.button("Extraheer teksten uit bestanden"):
            result = subprocess.run(["python", "src/extracttext.py"])
            st.success("Teksten succesvol geëxtraheerd uit bestanden.")
            
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
                
        if st.button("Verwijder alle bestanden bestanden"):
            files = glob.glob('documenten/*')
            for file in files: 
                os.remove(file)  
            

with tab3:
    custom_tab3 = f"<p style='font-size:65px; font-weight:bold'>Preprocessing</p>"  
    st.markdown(custom_tab3, unsafe_allow_html=True)     
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
           
            result = subprocess.run(["python", "src/preprocess.py"], shell=True, capture_output=True, text=True)
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
                result = subprocess.run(["python", "src/remove_words.py"], capture_output=True, text=True)
                st.write("Woorden uit tekstcorpus gehaald")
            else: 
                st.write("Er zijn geen woorden om te verwijderen.")
    
            
with tab4: 
    custom_tab4 = f"<p style='font-size:65px; font-weight:bold'>LDA</p>"    
    st.markdown(custom_tab4, unsafe_allow_html=True) 
    text_lda = """
    Latent Dirichlet Allocation (LDA) is een krachtige techniek die wordt gebruikt om verborgen thema's in een verzameling documenten te ontdekken. Het uitgangspunt van LDA is dat elk document een mix is van verschillende onderwerpen en dat elk onderwerp een mix is van woorden. Stel je voor dat je een verzameling artikelen hebt over verschillende onderwerpen zoals sport, politiek en technologie. LDA probeert te achterhalen welke onderwerpen in elk artikel voorkomen en welke woorden bij elk onderwerp horen. /n/n

    Het proces begint met het willekeurig toewijzen van woorden aan onderwerpen. Vervolgens wordt dit proces herhaaldelijk aangepast om de waarschijnlijkheid te maximaliseren dat de woorden bij de juiste onderwerpen horen. Uiteindelijk resulteert dit in een set onderwerpen met bijbehorende woorden en een verdeling van onderwerpen over de documenten. Dit maakt het mogelijk om patronen en trends in grote hoeveelheden tekst te ontdekken, wat bijzonder nuttig is in gebieden zoals tekstmining en data-analyse. /n/n

    LDA wordt veel toegepast in verschillende domeinen, zoals het analyseren van nieuwsartikelen, wetenschappelijke papers en sociale media. Door de verborgen thema's in teksten te identificeren, kunnen onderzoekers en analisten waardevolle inzichten verkrijgen en beter begrijpen welke onderwerpen in een bepaalde verzameling documenten domineren. /n/n 
    
    Voor meer informatie kun je de volgende studie bekijken: /n/n 
    
    Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. In jmlr.org. Journal of Machine Learning. https://proceedings.neurips.cc/paper/2001/file/296472c9542ad4d4788d543508116cbc-Paper.pdf
    
    """ 
    paragraphs_lda = text_lda.split("/n/n")
    for i, paragraph in enumerate(paragraphs_lda, 1):
        st.write(paragraph)  

    st.write("Kies hieronder de parameters voor het trainen van het Latent Dirichlet Allocation-model. De parameters  die voor het LDA-model gebruikt worden zijn:") 
    st.markdown("- Minimale collectiefrequentie van woorden: Het minimale aantal keren dat een woord in de gehele corpus moet voorkomen om opgenomen te worden in de analyse. Woorden die minder vaak voorkomen, worden verwijderd. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. De bovengrens is 10000.")
    st.markdown("- Minimale documentfrequentie van woorden: Het minimale aantal documenten waarin een woord moet voorkomen. Woorden die minder vaak voorkomen dan de gespecifideerde waarde, worden uitgesloten. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. De bovengrens is 10000. Alle woorden die aan deze grens voldoen, worden in deze analyse meegenomen.")
    st.markdown("- Aantal te verwijderen 'top'-woorden: Het aantal meest voorkomende woorden in de corpus dat verwijderd wordt. Laat dit veld leeg om de standaardwaarde 0 te gebruiken. Alle woorden die voldoen aan deze drempel worden meegenomen in de analyse.")
    st.markdown("- K (aantal topics): Het aantal topics dat door het model gegenereerd moet worden. Kies een waarde tussen 1 ~ 32676.")
    st.markdown("- Alpha is de hyperparameter van de Dirichlet-verdeling voor de documenten-topicverdeling. Kies voor een symmetric prior of een asymmetric prior. Symmetric betekent voor alle topics dezelfde prior. Asymmetric betekent dat sommige topics prominenter zijn dan andere, afhankelijk van de specifiek afgestemde alpha.")    
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
            min_cf_input = st.number_input(label="Minimale collectie frequentie van woorden:", min_value=0, max_value=10000, key="min_cf")
            min_df_input = st.number_input(label="Minimale documentfrequentie van woorden:", min_value=0, max_value=10000, key="min_df")  
            top_words_input = st.number_input(label="Aantal te verwijderen 'top-woorden:", min_value=0, max_value=10000, key="top_words") 
            number_topics_input = st.number_input(label="K (het aantal topics)", min_value=1, max_value=20, key="number_topics") 
            alpha_input = st.text_input("Enter symmetric alpha or asymmetric alpha:")
            eta_input = st.number_input("Eta:", min_value=0.01, max_value=1.0, step=0.01, key="eta")  
            submit_button = st.form_submit_button(label="Leg parameters vast", on_click=form_callback)
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
            result = subprocess.run(["python", "src/lda.py"], shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                st.success("LDA model is voltooid!")
                split_output = result.stdout.split("|")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                    processed_content = "<br>".join(split_output)
                    tmp_file.write(processed_content.encode("utf-8"))
                    st.session_state.results_file_path = Path(tmp_file.name)     
                    
                st.session_state.results_ready = True 
                
                st.write("De visualisatie wordt gegenereerd...")
                
                result_visualization = subprocess.run(["python", "src/visualization.py"], shell=True, capture_output=True, text=True)    

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
                                 
with tab5: 
    custom_tab6 = f"<p style='font-size:65px; font-weight:bold'>LLM LDA</p>" 
    st.markdown(custom_tab6, unsafe_allow_html=True)     
    st.write("Op de volgende pagina kan een LDA met een Large Language Model getraind worden. De resultaten van het model kunnen eveneens gedownload worden. Een Large Language Model draait via de Azure Cloud, dat betekent dat alleen openbare documenten in dit model kunnen worden getraind. Hier documenten ingooien die niet-openbaar zijn, leidt tot een datalek. De parameters zijn hetzelfde en die kun je op de volgende pagina ook aanpassen. Succes!") 
    
    st.write("LET OP: Dit model draait via de Azure Cloud. Alleen openbare documenten in dit model trainen.") 
    
    col1, col2 = st.columns(2) 
    
    with col1: 
        # Define form_callback 
        def form_callback2(): 
            # Save session state values to an external file
            parameters = {
                "min_cf2": min_cf_input2,
                "min_df2": min_df_input2,
                "top_words2": top_words_input2,
                "number_topics2": number_topics_input2,
                "alpha2": alpha_input2,
                "eta2": eta_input2
            }
            with open("parameters/parameters2.json", "w") as f:
                json.dump(parameters, f)
        
        # Initialize the parameters for training the LDA model
        with st.form(key="my_form2"): 
            min_cf_input2 = st.number_input(label="Minimale collectie frequentie van woorden:", min_value=0, max_value=10000, key="min_cf2")
            min_df_input2 = st.number_input(label="Minimale documentfrequentie van woorden:", min_value=0, max_value=10000, key="min_df2")  
            top_words_input2 = st.number_input(label="Aantal te verwijderen 'top-woorden:", min_value=0, max_value=10000, key="top_words2") 
            number_topics_input2 = st.number_input(label="K (het aantal topics)", min_value=1, max_value=20, key="number_topics2")
            alpha_input2 = st.text_input("Enter symmetric alpha or asymmetric alpha:")
            eta_input2 = st.number_input(label="Eta:", min_value=0.01, max_value=1.0, step=0.01, key="eta2")
            submit_button2 = st.form_submit_button(label="Leg parameters vast", on_click=form_callback2)
            if submit_button2:
                st.write("Parameters vastgelegd!") 
                
    with col2: 
        # Define session states 
        if "results_ready_llm_lda" not in st.session_state:  
            st.session_state.results_ready_llm_lda = False 
        if "results_file_path_llm_lda" not in st.session_state:  
            st.session_state.results_file_path_llm_lda = None 
        if "visualization_file_path_llm_lda" not in st.session_state:   
            st.session_state.visualization_file_path_llm_lda = None 
        
        # Verkrijg resultaten en visualisatie    
        if st.button("Verkrijg resultaten en visualisatie van het lDA-model met een Large Language Model!"): 
            st.write("De resultaten en de visualisatie verschijnen in een klikbare link.")   
            result = subprocess.run(["python", "src/LDALLM.py"], shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("LLM LDA model is voltooid!")
                output = result.stdout   
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                    tmp_file.write(output.encode("utf-8")) 
                    st.session_state.results_file_path_llm_lda = Path(tmp_file.name)     
                
                st.session_state.results_ready_llm_lda = True 
                
                st.write("De visualisatie wordt gegenereerd...")
                result_visualization_llm = subprocess.run(["python", "src/visualization_llm.py"], shell=True, capture_output=True, text=True) 
                  
                # Visualization section
                if result_visualization_llm.returncode == 0:
                    st.success("Resultaten en visualisatie zijn voltooid!")
                    st.session_state.visualization_file_path_llm_lda = "models/ldavis_llm.html" 
                else:
                    st.error("Er is een fout opgetreden bij het genereren van de visualisatie!") 
                    st.write(result_visualization_llm.stderr) 
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
            
            if st.session_state.visualization_file_path_llm_lda: 
                with open(st.session_state.visualization_file_path_llm_lda, "r") as file:
                    html_content_llm = file.read()
                    
                st.download_button(label="Klik om de visualisatie te downloaden",
                                    data=html_content_llm,
                                    file_name="ldavis_llm.html",
                                    mime="text/html")
        
with tab6:
    custom_tab8 = f"<p style='font-size:65px; font-weight:bold'>BERTopic</p>"  
    st.markdown(custom_tab8, unsafe_allow_html=True)     
    text_bertopic = """
    BERTopic is een geavanceerde techniek voor topic modeling die gebruik maakt van moderne taalmodellen zoals BERT (Bidirectional Encoder Representations from Transformers) en c-TF-IDF (class-based Term Frequency-Inverse Document Frequency) om betekenisvolle clusters en onderwerpen te creëren. Het doel van BERTopic is om gemakkelijk interpreteerbare onderwerpen te genereren terwijl belangrijke woorden in de beschrijvingen van de onderwerpen behouden blijven. /n/n

    Het proces begint met het gebruik van BERT om tekstuele gegevens om te zetten in hoge-dimensionale vectoren die de semantische betekenis van de woorden vastleggen. Deze vectoren worden vervolgens geclusterd om groepen van gerelateerde documenten te vormen. Door c-TF-IDF toe te passen, kan BERTopic de belangrijkste woorden binnen elk cluster identificeren, wat helpt bij het beschrijven van de onderwerpen op een begrijpelijke manier. /n/n

    Een van de sterke punten van BERTopic is de flexibiliteit en de mogelijkheid om verschillende technieken te ondersteunen, zoals zero-shot topic modeling, waarbij nieuwe onderwerpen kunnen worden geïdentificeerd zonder voorafgaande training, en het gebruik van seed words om specifieke onderwerpen te sturen. Dit maakt BERTopic bijzonder nuttig voor het analyseren van grote hoeveelheden tekst en het ontdekken van verborgen patronen en trends. /n/n

    In de praktijk wordt BERTopic veel gebruikt in verschillende domeinen, zoals het analyseren van klantfeedback, het monitoren van sociale media en het verkennen van wetenschappelijke literatuur. Door de kracht van moderne taalmodellen te benutten, biedt BERTopic een robuuste en efficiënte manier om inzicht te krijgen in de inhoud van grote tekstcorpora. /n/n 

    Kijk naar de onderstaande studie voor meer informatie: /n/n 

    Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. arXiv (Cornell University). https://doi.org/10.48550/arxiv.2203.05794
    
    """
    paragraphs_bertopic = text_bertopic.split("/n/n")
    for i, paragraph in enumerate(paragraphs_bertopic, 1):
        st.write(paragraph)
    
    if "results_file_path_bertopic" not in st.session_state:    
        st.session_state.results_file_path_bertopic = None 
    if "results_ready_bertopic" not in st.session_state:     
        st.session_state.results_ready_bertopic = False  
    
    st.write("Druk hieronder op de knop om het model te laten lopen.")
    
    if st.button("Train BERTopic model"): 
        st.write("Het BERTopic model is op dit moment aan het trainen.") 
        
        result = subprocess.run(["python", "src/BERTopic.py"], shell=True, capture_output=True, text=True) 
        
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

col1, col2, col3 = st.columns(3) 

with col2: 
    st.image("media/2560px-Logo_Ministerie_SZW.svg.png", width=300) 
            
   