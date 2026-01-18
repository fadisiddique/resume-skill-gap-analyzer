import re
import pdfplumber
from sentence_transformers import SentenceTransformer,util
from typing import List
import warnings
import os
warnings.filterwarnings("ignore")

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def clean_text(text):
    text=re.sub(r'[^\w\s.+#]',' ',text)
    text=re.sub(r'\s+',' ',text)
    return text.strip().lower()

def extract_from_pdf(pdf_path):
    text=""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text() or ""
    return clean_text(text)

def get_skill_dictionary(skill_list_path):
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path=os.path.join(base_dir,skill_list_path)
    with open(full_path,"r", encoding="utf-8") as f:
        skill_list=[line.strip().lower() for line in f.readlines()]
    return skill_list
        
def get_phrases(text,maxN=3):
    words=text.split()
    phrases=[]
    for N in range(1,maxN+1):
        for i in range(len(words)-N+1):
            phrases.append(' '.join(words[i:i+N]))
    return phrases

def extract_skills_exact(text,skill_list):
    skill_found=[]
    for skill in skill_list:
        if re.search(r'\b'+re.escape(skill)+r'\b',text):
            skill_found.append(skill)  
    return skill_found

def skill_matching(text,skill_list,threshold=0.6):
    
    phrases=get_phrases(text)
    skill_embedded=model.encode(skill_list,convert_to_tensor=True)
    text_embedded=model.encode(phrases,convert_to_tensor=True)
    similarity=util.cos_sim(skill_embedded,text_embedded)
    semantic_skill_found=[]
    
    for i,skill in enumerate(skill_list):
        if similarity[i].max().item()>threshold:
            semantic_skill_found.append(skill)
    exact_skill=extract_skills_exact(text,skill_list)
    return list(set(semantic_skill_found+exact_skill))


def get_skill_reading(matched_resume_skills:List[str],matched_JD_skills:List[str]):
    matched=set(matched_resume_skills) & set(matched_JD_skills)
    missing=set(matched_JD_skills) - set(matched_resume_skills)
    score=(len(matched)/len(matched_JD_skills))*100
    return matched,missing,round(score,2)





    
    
    
            
    
                
        
