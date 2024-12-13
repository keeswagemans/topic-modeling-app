import os
import json 
from PyPDF2 import PdfReader
from docx import Document
import pymupdf   

class ExtractText:

    @staticmethod 
    def extract_text_from_files(path):
        """
        Extracts text from files in directory.
        """
        text = ""
        _, ext = os.path.splitext(path)

        if ext == ".pdf":
            try:
                doc = pymupdf.open(path)
                for page in doc: 
                    text += page.get_text()
            except Exception as e: 
                print(f"Error reading PDF")

        elif ext == ".docx":
            try:
                doc = Document(path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            except Exception as e:
                print(f"Error reading DOCX {path}: {e}")

        elif ext == ".doc":
            print("Encountered doc file. Continuing.")

        return text
    
    @staticmethod 
    def extract_from_directory(path):
        count = 0

        all_text = {}

        for root, _, files in os.walk(path):
            for file_name in files:
                count += 1
                print(count)
                file_path = os.path.join(root, file_name)
                file_text = ExtractText.extract_text_from_files(file_path)
                file_text = str(file_text)
                all_text[file_name] = file_text
                print(file_name)
        return all_text 

# Run the code 
output_data = ExtractText.extract_from_directory("topic-modeling-app/documenten/")
json.dump(output_data, open("topic-modeling-app/extractedtext/extractedtext.json", "w"))