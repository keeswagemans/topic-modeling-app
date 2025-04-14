import streamlit as st 
import subprocess 
import tempfile 
import json 
from pathlib import Path 
import streamlit.components.v1 as components   

# Load fonts
with open("style_header.html", "r", encoding="utf-8") as f:
    html_header = f.read()
with open("style_body.html", "r", encoding="utf-8") as f:
    html_body = f.read()

# Title 
html_filled = html_header.replace("{{content_header}}", "Latent Dirichlet Allocation met Large Language Model")
components.html(html_filled, height=200) 

# Main text 
st.markdown(html_body, unsafe_allow_html=True)   
st.markdown(
    """
    Op deze pagina kan een LDA met een Large Language Model getraind worden. De resultaten van het model kunnen eveneens gedownload worden. Een Large Language Model draait via de Azure Cloud, dat betekent dat alleen openbare documenten in dit model kunnen worden getraind. Hier documenten ingooien die niet-openbaar zijn, leidt tot een datalek. Succes!") 
    
    LET OP: Dit model draait via de Azure Cloud. Alleen openbare documenten in dit model trainen.
    
    """
)

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
        min_cf_input2 = 0
        min_df_input2 = 0
        top_words_input2 = 0
        number_topics_input2 = st.number_input(label="K (het aantal topics)", min_value=1, max_value=20, key="number_topics2")
        alpha_input2 = 0.01
        eta_input2 = 0.01 
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
        result = subprocess.run(["python", "functions/Latent Dirichlet Allocation met Large Language Model.py"], shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            st.success("LLM LDA model is voltooid!")
            output = result.stdout   
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                tmp_file.write(output.encode("utf-8")) 
                st.session_state.results_file_path_llm_lda = Path(tmp_file.name)     
            
            st.session_state.results_ready_llm_lda = True 
            
            st.write("De visualisatie wordt gegenereerd...")
            result_visualization_llm = subprocess.run(["python", "functions/visualization_llm.py"], shell=True, capture_output=True, text=True) 
                
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