from typing import Dict,Any
from backend.JD_resume_skill import skill_matching,extract_from_pdf,get_skill_dictionary,clean_text,get_skill_reading
import warnings
warnings.filterwarnings("ignore")

def analyze_for_main(resume_pdf_path: str, jd_text: str,skill_list_path:str)->Dict[str,Any]:
    resume_text=extract_from_pdf(resume_pdf_path)
    skill_list=get_skill_dictionary(skill_list_path)
    matched_resume_skills=skill_matching(resume_text,skill_list)
    jd_text=clean_text(jd_text)
    matched_jd_skills=skill_matching(jd_text,skill_list)
    matched,missing,score=get_skill_reading(matched_resume_skills,matched_jd_skills)
    return {
        "resume skills":sorted(matched_resume_skills),
        "Job Description skills":sorted(matched_jd_skills),
        "matched skills":sorted(matched),
        "missing skills":sorted(missing),
        "match Score":score
    }   
    