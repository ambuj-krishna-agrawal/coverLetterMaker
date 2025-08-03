#!/usr/bin/env python3

import docx
import json

def extract_resume_info(docx_path):
    """Extract text content from a DOCX file"""
    try:
        doc = docx.Document(docx_path)
        full_text = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text.strip())
        
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return None

if __name__ == "__main__":
    resume_text = extract_resume_info("AMBUJ_AGRAWAL_RESUME_ML.docx")
    if resume_text:
        print(resume_text)
        
        # Save to a text file for easier access
        with open("resume_info.txt", "w", encoding="utf-8") as f:
            f.write(resume_text)
        print("\nResume content saved to resume_info.txt")
    else:
        print("Failed to extract resume content")