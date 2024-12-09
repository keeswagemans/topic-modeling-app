import streamlit as st


tab1, tab2, tab3, tab4 = st.tabs(['Over project', 'LDA', 'LDA met LLM', 'Documents'])

with tab1: 
    st.title("Topic Modeling voor het Ministerie van Sociale Zaken en Werkgelegenheid 👋")
    st.write(
    "The Latent Dirichlet Allocation (LDA) model is designed to identify key topics within documents. This tool aims to assist the Ministry of Social Affairs and Employment in proactively disclosing documents on subjects that are likely to be of public interest. There are two models, a strict Latent Dirichlet Model and an Latent Dirichlet Model with an LLM as a backbone."
    )

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
        if st.select_slider(label='Number of topics', options=[x for x in range(1,21)], value=[1,20]): 
            st.write("Thanks!")

    with col2: 
        if st.button("Get results"):
            st.write("Training the Latent Dirichlet Allocation model for you and returning the results in a visualization.")
        if st.select_slider(label='Number of topics within document', options=[x for x in range(1,21)], value=[1,20]): 
            st.write('Thanks!')

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a pdf or a docx file.")

    # Button to upload the file
    if uploaded_file is not None:
        if st.button("Upload to Repository"):
            # Here you can add the logic to save the file to your repository
            # For example, saving the file locally
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully!")

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

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a pdf or a docx file!")

    # Button to upload the file
    if uploaded_file is not None:
        if st.button("Upload to Repository!"):
            # Here you can add the logic to save the filye to your repository
            # For example, saving the file locally
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully!")

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
    
    with col1:
        if st.button("Get list of documents in repository!"):
            st.write("Retrieving documents for you.")