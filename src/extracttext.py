import os
import json 
from PyPDF2 import PdfReader
from docx import Document
import pymupdf   

class ExtractText:
    
    def __init__(self, path): 
        self.path = path

    def extract_text_from_files(path):
        """
        Extracts text from files in a directory.

        This function takes a file path as input and extracts text from the file based on its extension.
        It supports PDF and DOCX files. For PDF files, it uses the pymupdf library to read and extract text
        from each page. For DOCX files, it uses the python-docx library to read and extract text from each paragraph.
        If the file is a DOC file, it simply prints a message and continues without extracting text.

        Parameters:
        path (str): The path to the file from which text needs to be extracted.

        Returns:
        str: The extracted text from the file.
        
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
    
    def extract_from_directory(path):
        """
        Extracts text from all files in a directory and its subdirectories.

        This function traverses through a given directory and its subdirectories, extracting text from each file
        using the `extract_text_from_files` method from the `ExtractText` class. It keeps a count of the files processed
        and prints the count and file names during the process. The extracted text from each file is stored in a dictionary
        with the file names as keys.

        Parameters:
        path (str): The path to the directory from which text needs to be extracted.

        Returns:
        dict: A dictionary where the keys are file names and the values are the extracted text from those files.
        """
        
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

output_data = ExtractText.extract_from_directory("documenten/")
json.dump(output_data, open("extractedtext/extractedtext.json", "w"))