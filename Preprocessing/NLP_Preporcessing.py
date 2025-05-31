import pandas as pd
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

def remove_punctuation(text):
    if not isinstance(text, str):
        return ""  
    return re.sub(r'[^\w\s]', '', text)

def clean_and_tokenize(text):

    if not isinstance(text, str):
        return ""  

    # Remove punctuation and convert to lowercase
    text = remove_punctuation(text).lower()

    # Remove stopwords
    doc = nlp(text)
    cleaned_tokens = [token.text for token in doc if token.text not in STOP_WORDS and token.is_alpha]

    # Return tokens as a single string
    return ' '.join(cleaned_tokens)

def clean_text(text):

    if not isinstance(text, str):
        return ""  

    # Remove long underscores
    text = re.sub(r'_{5,}', ' ', text) 

    # Split concatenated words where a lowercase letter is followed by an uppercase letter
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  

    # Split concatenated words where two words are stuck together without punctuation or capitalization
    #text = re.sub(r'(\w)([A-Z][a-z])', r'\1 \2', text) 

    # Split concatenated words where numbers and words are joined
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)  

    # Strip whitespace
    text = text.strip()

    return text


def process_csv_data(input_file, output_file):
    try:
        # Load the input CSV
        df = pd.read_csv(input_file)

        if 'URL' in df.columns:
            df = df.drop(columns=['URL'])

        # Process all columns except the 'URL' column
        for col in df.columns:
            if df[col].dtype == 'object':  
                # tokenize
                df[col] = df[col].apply(lambda x: clean_and_tokenize(clean_text(x)))

     
        df.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    input_file = r'C:\Users\vidya\CaribbeanJobs\Extra_Details.csv'  
    output_file = r'C:\Users\vidya\Topic Modelling_3020\Extra_JD.csv' 

    process_csv_data(input_file, output_file)

