# ECE-Curriculum-NLP-Analysis
Code and materials for ACDSA2025 paper on aligning university curricula with ECE job skills using NLP

# ECE Curriculum and Job Skills Alignment Using NLP

This repository contains the code, data samples, and processing pipeline used in the ACDSA2025 research paper titled:  
**"Using Natural Language Processing to Correlate University Curricula with Required Job Skills"**

## Project Overview

This study investigates how well the undergraduate curriculum in the Department of Electrical and Computer Engineering (DECE) at The University of the West Indies aligns with the evolving skill demands of the global job market. Using Natural Language Processing (NLP), we analyze course outlines and job descriptions to identify overlaps and gaps in required technical and soft skills.

## Key Objectives

- Collect and process job descriptions across five ECE themes:
  - Communication Systems
  - Computer Systems
  - Control Systems
  - Electronics
  - Energy/Power Systems

- Extract relevant skills using the **SkillNER** toolkit

- Apply **LDA topic modeling** to identify dominant skill clusters in both curricula and job data

- Compute **alignment scores** to quantify the curriculum-to-industry match

## Contents
- Web scraping scripts
- SkillNER skill extraction tool
- LDA topic modeling and Closeness Metric


## Tools Used
- Python 3.12.7
- Selenium, BeautifulSoup
- SkillNER, spaCy, Gensim
  
## Ethical Considerations
- Job data was scraped from publicly available listings on major platforms (e.g., LinkedIn, Indeed, CaribbeanJobs).
- No personal or sensitive data was collected.
- Course outline data was provided by the DECE at UWI with department permission.
- No ethical clearance was required, and no conflicts of interest or funding were involved in this study.
  
## Reproducibility
All scripts are included to reproduce the skill extraction and topic modeling process.  
*Note: Full datasets available on request due to platform limitations.*

