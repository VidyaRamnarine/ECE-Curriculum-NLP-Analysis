import spacy
import pandas as pd
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from collections import Counter

# Load Spacy Model
nlp = spacy.load("en_core_web_lg")

# Initialize Skill Extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# Load course outlines dataset
df = pd.read_csv(r"C:\Users\vidya\Topic Modelling_3020\ECNG_Syllabus.csv")

# Check if 'Content' column exists
if "Content" in df.columns:
    extracted_skills_list = []

    for i, text in enumerate(df["Content"].fillna("")):  # Fill NaN with empty string
        skills = skill_extractor.annotate(text)  

        extracted_skills = []  

        # Extract skills from full_matches & ngram_scored
        skill_names = [match["doc_node_value"] for match in skills["results"]["full_matches"]]
        skill_names += [match["doc_node_value"] for match in skills["results"]["ngram_scored"]]

        # Count occurrences of each skill manually
        skill_counts = Counter(skill_names)
        for skill, count in skill_counts.items():
            extracted_skills.extend([skill] * count)  

        # Join skills with commas (with duplicates)
        extracted_skills_list.append(", ".join(extracted_skills))

    # Add extracted skills to DataFrame
    df["extracted_skills"] = extracted_skills_list

    # Save extracted skills to a CSV file
    df[["Content", "extracted_skills"]].to_csv("extracted_syllabus_skills.csv", index=False)

    print("Extraction complete! Results saved to 'extracted_syllabus_skills.csv'.")
else:
    print("Column 'Content' not found in the DataFrame.")

