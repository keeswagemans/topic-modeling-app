import streamlit as st 
import os 
import subprocess    
import glob 
import json
import streamlit.components.v1 as components  

LOCAL_REPO_PATH = os.path.join(os.getcwd(), "documenten")

# Load fonts 
with open("style_header.html", "r", encoding="utf-8") as f:
    html_header = f.read()
with open("style_body.html", "r", encoding="utf-8") as f:
    html_body = f.read()
    
# Main title 
html_filled = html_header.replace("{{content_header}}", "Document Manager")
components.html(html_filled, height=150)    

os.makedirs(LOCAL_REPO_PATH, exist_ok=True)  # Ensure the directory exists

# Main text 
st.markdown(html_body, unsafe_allow_html=True)   
st.markdown("Volg de stappen hieronder. Stap 4 en stap 5 zijn optioneel.", unsafe_allow_html=True)   

# Step 1: Uploading the documents 
st.markdown("Stap 1: Upload je documenten. Dit kunnen PDF of DOCX bestanden zijn. Je kunt meerdere bestanden tegelijk uploaden.")   

# Set variables 
if "uploader_key" not in st.session_state: 
    st.session_state.uploader_key = 0 
    

# Button to get list of documents in the repository
uploaded_files = st.file_uploader("Kies een PDF of DOCX bestand.", type=["pdf", "docx"], accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")   
    
if uploaded_files:
    if st.button("Documenten uploaden"): 
        for uploaded_file in uploaded_files: 
            try:
                save_path = os.path.join("documenten/", uploaded_file.name)
                with open(save_path, "wb") as f: 
                    f.write(uploaded_file.getvalue())
                # st.success(f"Document {uploaded_file.name} succesvol geupload.")
                st.info(f"{save_path}")
            except Exception as e:
                st.error(f"Er is een fout opgetreden met {uploaded_file.name}: {e}.")
            
        
    if st.button("Verkrijg lijst van de documenten in de map"):
        # List the files in the local repository
        documents = os.listdir(LOCAL_REPO_PATH)
        if documents:
            st.markdown('''
            <style>
                - [data-testid="stMarkdownContainer"] ul{
            padding-left:20px;
            margin:0;
            font-size:12px; 
            }
            </style>
            ''', unsafe_allow_html=True) 
            st.markdown("Documenten die beschikbaar zijn in de map:")
            markdown_string = ""
            for document in documents:
                markdown_string += f"- {document}\n" 

                st.markdown(markdown_string)   
        else:
            st.markdown("Nog geen documenten in de map gevonden.")

# Stap 2: Extracting text from the documents 
st.markdown("Stap 2: Extraheren van de teksten.") 
if st.button("Extraheer teksten uit bestanden"):
    result = subprocess.run(["python", "functions/extracttext.py"])
    st.success("Teksten succesvol geëxtraheerd uit bestanden.")

# Stap 3: Preprocessing 
st.markdown("Stap 3: Preprocessen van de teksten.") 
if st.button("Preprocessing"): 
    st.markdown("Er wordt aan gewerkt!")
    
    result = subprocess.run(["python", "functions/Preprocessing.py"], shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        st.success("Preprocessing voltooid!")
    else:
        st.error("Er is een fout opgetreden!")
        st.code(result.stderr)
        
# Step 4: Delete words 
st.markdown("Stap 4: Woorden verwijderen. (Niet noodzakelijk.)")     
st.markdown("Hieronder kun je woorden intikken om te verwijderen, druk op enter en klik vervolgens op de knop 'Verwijder woorden' rechts. Wil je geen woorden verwijderen. Druk op 'Preprocessing' na het verwijderen van de woorden.") 

words_to_remove_input = st.text_input("Woorden om te verwijderen (gescheiden door komma's):")
if words_to_remove_input:
    words_to_remove = [word.strip() for word in words_to_remove_input.split(",")]
else:
    words_to_remove = [] 
    
remove_button = st.button("Verwijder woorden")          
if remove_button: 
    if words_to_remove: 
        words_to_remove = [word.lower() for word in words_to_remove] 
        json.dump(words_to_remove, open("preprocessing/words_to_remove.json", "w")) 
        result = subprocess.run(["python", "functions/remove_words.py"], capture_output=True, text=True)
        st.markdown("Woorden uit tekstcorpus gehaald.") 
    else: 
        st.markdown("Er zijn geen woorden om te verwijderen.")

# Verwijder bestanden 
st.markdown("Stap 5: Verwijder hier onder alle bestanden uit de map, als je een analyse wilt doen over andere bestanden. Deze stap is optioneel.")
if st.button("Verwijder alle bestanden"):
    files = glob.glob('documenten/*')
    for file in files: 
        os.remove(file)  
