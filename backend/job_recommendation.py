# -*- coding: utf-8 -*-
import sys 
import config, web_scrapper
from skill_keyword_match import skill_keyword_match
import nltk
nltk.download('stopwords')

def main():
    l = ''
    jobs_info = web_scrapper.get_jobs_info(l)
    skill_match = skill_keyword_match(jobs_info)
    skill_match.extract_jobs_keywords()
    resume_skills = skill_match.extract_resume_keywords(config.SAMPLE_RESUME_PDF)
    top_job_matches = skill_match.cal_similarity(resume_skills.index, l)
    print('File of recommended jobs saved')
    top_job_matches.drop_duplicates(subset=['location', 'company', 'title'], inplace=True)
    return top_job_matches
