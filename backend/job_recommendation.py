# -*- coding: utf-8 -*-
import sys 
import config, web_scrapper
from skill_keyword_match import skill_keyword_match
import nltk
nltk.download('stopwords')

def main():
    location = ''
    jobs_info = web_scrapper.get_jobs_info(location)
    skill_match = skill_keyword_match(jobs_info)
    skill_match.extract_jobs_keywords()
    resume_skills = skill_match.extract_resume_keywords(config.SAMPLE_RESUME_PDF)
    top_job_matches = skill_match.cal_similarity(resume_skills.index, location)
    print('File of recommended jobs saved')
    return top_job_matches
