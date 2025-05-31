import spacy
import pandas as pd
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from collections import Counter

# Initialize the Spacy model and SkillExtractor
nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# Load job descriptions
df = pd.read_csv("Thematic_Jobs.csv")

# Check if 'Experience' column exists
if "Experience" in df.columns:
    extracted_skills_list = []

    for i, text in enumerate(df["Experience"].fillna("")):  # Fill NaN with empty string
        skills = skill_extractor.annotate(text)  

        extracted_skills = []  

        # Collect skills from both full_matches & ngram_scored
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
    df[["Experience", "extracted_skills"]].to_csv("extracted_skills.csv", index=False)

    print("Extraction complete! Results saved to 'extracted_skills.csv'.")
else:
    print("Column 'Experience' not found in the DataFrame.")

