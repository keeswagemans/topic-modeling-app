import os
from PyPDF2 import PdfReader
from docx import Document

class ExtractText:

    
    def __init__(self, path, output_data): 
        """
        Initialize the ExtractText class.

        Args:
            path (str): Path to the directory or file.
            output_data (dict): A dictionary to store extracted text data.
        """
        self.path = path  
        self.output_data = output_data 

    def extract_text_from_file(self, file_path): 
        """
        Extract text from a single file.

        Supports PDF and DOCX formats. Logs errors for unsupported or unreadable files.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Extracted text from the file or an empty string on failure.
        """
        text = ""
        _, ext = os.path.splitext(file_path.lower())

        try:
            if ext == ".pdf":
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    for page in reader.pages: 
                        if page:
                            text += " " + (page.extract_text() or "") + " "

            elif ext == ".docx": 
                doc = Document(file_path)
                for para in doc.paragraphs:
                    text += " " + para.text + " "
            
            elif ext == ".doc": 
                # Placeholder for handling .doc files if needed (requires additional libraries like `pywin32`).
                raise NotImplementedError(".doc file extraction is not supported.")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

        return text.strip()

    def extract_from_directory(self): 
        """
        Extract text from all files in the specified directory and its subdirectories.

        The text is stored in the `output_data` dictionary where keys are file names and values are the extracted text.

        Returns:
            dict: A dictionary containing file names and their extracted text.
        """
        all_text = {}
        count = 0 

        for root, _, files in os.walk(self.path): 
            for file_name in files:
                count += 1
                file_path = os.path.join(root, file_name)
                file_text = self.extract_text_from_file(file_path)
                if file_text:  # Only store non-empty text
                    all_text[file_name] = file_text
        
        self.output_data = all_text
        print(f"Processed {count} files.")
        return all_text
