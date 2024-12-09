import os
import json 
from PyPDF2 import PdfReader
from docx import Document

class ExtractText:

    def __init__(self, path): 
        """
        Initialize the ExtractText class.

        Args:
            path (str): Path to the directory or file.
            output_data (dict): A dictionary to store extracted text data.
        """
        self.path = path  

    def extract_text_from_files(self, path):
        """
        Extracts text from files in directory.
        """
        text = ""
        _, ext = os.path.splitext(path)

        if ext == ".pdf":
            try:
                with open(path, 'rb') as file:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        text += " " + page.extract_text() + " "
            except Exception as e:
                print(f"Error reading PDF {path}: {e}")

        elif ext == ".docx":
            try:
                doc = Document(path)
                for para in doc.paragraphs:
                    text += " " + para.text + " "
            except Exception as e:
                print(f"Error reading DOCX {path}: {e}")

        elif ext == ".doc":
            print("Encountered doc file. Continuing.")

        return text
    
    def extract_from_directory(self, path):
        count = 0

        all_text = {}

        for root, _, files in os.walk(path):
            for file_name in files:
                count += 1
                print(count)
                file_path = os.path.join(root, file_name)
                file_text = self.extract_text_from_files(file_path)
                file_text = str(file_text)
                all_text[file_name] = file_text
                print(file_name)
        return all_text

# Run the code 
instance = ExtractText("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/documenten/")
output_data = instance.extract_from_directory("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/documenten/")
json.dump(output_data, open("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/extractedtext/extractedtext.json", "w"))