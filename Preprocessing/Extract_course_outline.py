import fitz  # PyMuPDF
import spacy
import re
import os
import pandas as pd

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF file.
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Function to preprocess text by removing punctuation, special characters, numbers (unless alphanumeric), converting to lowercase, removing stop words, and tokenizing.
def clean_text(text):

    text = text.lower()  
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  
    doc = nlp(text)  
    tokens = [token.text for token in doc if not token.is_space and not token.is_stop and (not token.text.isdigit() or token.text.isalnum())]  # Remove stop words, standalone numbers, keep alphanumeric
    return tokens

# Get list of PDF files from a specified folder
folder_path = r'C:\Users\vidya\Pdf_Extraction\course outlines' 
pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]

cleaned_data = []

# Process each PDF file
for file in pdf_files:
    print(f"Processing {file}...")
    raw_text = extract_text_from_pdf(file)
    cleaned_tokens = clean_text(raw_text)
    cleaned_data.append({"file_name": os.path.basename(file), "cleaned_tokens": cleaned_tokens})

df = pd.DataFrame(cleaned_data)

# Save the cleaned data to a CSV file
output_file_path = "cleaned_pdf_data.csv"
df.to_csv(output_file_path, index=False)

print(f"Cleaned data saved to {output_file_path}")