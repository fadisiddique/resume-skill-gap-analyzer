from fastapi import FastAPI, UploadFile,File,Form,HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import tempfile
import shutil
import os
from backend.service import analyze_for_main
from fastapi.middleware.cors import CORSMiddleware

import warnings
warnings.filterwarnings("ignore")

app=FastAPI(title="analyzer for resume pdf")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    resume_file:UploadFile=File(...),
    jd_text:str =Form(...),
    skill_list_path: Optional[str]=Form("skill_list/skill_list.txt")
    ):
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400,detail="Resume must be a pdf file")
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp:
            temp_path=tmp.name
            shutil.copyfileobj(resume_file.file,tmp)
    finally:
        resume_file.file.close()
        
    try:
        result=analyze_for_main(
            resume_pdf_path=temp_path,
            jd_text=jd_text,
            skill_list_path=skill_list_path
        )
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass

        
    return JSONResponse(content=result)
    
    



