#!/usr/bin/env python3

import os
import docx

class ResumeParser:
    def __init__(self, resume_path="resume_info.txt"):
        self.resume_path = resume_path
        self.user_info = self._load_resume_info()
    
    def _load_resume_info(self):
        """Load resume information from text file or extract from DOCX"""
        try:
            if os.path.exists(self.resume_path):
                with open(self.resume_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                # Fallback to DOCX if text file doesn't exist
                content = self._extract_from_docx("AMBUJ_AGRAWAL_RESUME_ML.docx")
            
            return self._parse_resume_content(content)
        except Exception as e:
            print(f"Error loading resume: {e}")
            return self._get_default_info()
    
    def _extract_from_docx(self, docx_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            full_text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    full_text.append(paragraph.text.strip())
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def _parse_resume_content(self, content):
        """Parse resume content and extract key information"""
        lines = content.split('\n')
        
        info = {
            'name': 'Ambuj Krishna Agrawal',
            'email': 'ambuja@andrew.cmu.edu',
            'phone': '(412) 918-0594',
            'linkedin': 'LinkedIn',
            'website': 'https://ambuj-krishna-agrawal.github.io/',
            'education': [],
            'experience': [],
            'skills': [],
            'projects': [],
            'full_resume': content
        }
        
        # Extract name from first line if available
        if lines and lines[0].strip():
            info['name'] = lines[0].strip()
        
        # Parse sections
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify sections
            upper_line = line.upper()
            if 'EDUCATION' in upper_line:
                current_section = 'education'
                current_content = []
            elif 'WORK EXPERIENCE' in upper_line or 'EXPERIENCE' in upper_line:
                current_section = 'experience'
                current_content = []
            elif 'SKILLS' in upper_line:
                current_section = 'skills'
                current_content = []
            elif 'PROJECTS' in upper_line or 'RESEARCH PROJECTS' in upper_line:
                current_section = 'projects'
                current_content = []
            elif current_section:
                current_content.append(line)
                info[current_section] = current_content.copy()
        
        return info
    
    def _get_default_info(self):
        """Default user information if resume parsing fails"""
        return {
            'name': 'Ambuj Krishna Agrawal',
            'email': 'ambuja@andrew.cmu.edu',
            'phone': '(412) 918-0594',
            'linkedin': 'LinkedIn',
            'website': 'https://ambuj-krishna-agrawal.github.io/',
            'education': ['Carnegie Mellon University - MS in NLP (AI)', 'IIIT Allahabad - BTech IT'],
            'experience': ['Netflix - ML Engineering Intern', 'CMU - ML Research Assistant', 'CRED - Senior SDE', 'LinkedIn - SDE'],
            'skills': ['Python', 'Java', 'Machine Learning', 'NLP', 'PyTorch', 'Flask', 'AWS'],
            'projects': ['Hellosec.ai', 'RAG-Chatbot', 'Multimodal Web Agents'],
            'full_resume': 'Resume content not available'
        }
    
    def get_user_info(self):
        """Get parsed user information"""
        return self.user_info
    
    def get_relevant_experience(self, role_keywords=None):
        """Get experience relevant to the role"""
        if not role_keywords:
            return self.user_info.get('experience', [])
        
        relevant_exp = []
        all_experience = self.user_info.get('experience', [])
        
        for exp in all_experience:
            if isinstance(exp, str):
                for keyword in role_keywords:
                    if keyword.lower() in exp.lower():
                        relevant_exp.append(exp)
                        break
        
        return relevant_exp if relevant_exp else all_experience[:3]  # Return top 3 if none match
    
    def get_relevant_skills(self, role_keywords=None):
        """Get skills relevant to the role"""
        all_skills = self.user_info.get('skills', [])
        
        if not role_keywords:
            return all_skills
        
        relevant_skills = []
        for skill in all_skills:
            if isinstance(skill, str):
                for keyword in role_keywords:
                    if keyword.lower() in skill.lower():
                        relevant_skills.append(skill)
                        break
        
        return relevant_skills if relevant_skills else all_skills[:5]  # Return top 5 if none match