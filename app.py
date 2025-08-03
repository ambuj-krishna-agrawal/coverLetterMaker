#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import json

from modules.resume_parser import ResumeParser
from modules.company_research import CompanyResearch
from modules.llm_client import LLMClient
from modules.cover_letter_generator import CoverLetterGenerator

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize modules
resume_parser = ResumeParser()
company_research = CompanyResearch()
llm_client = LLMClient()
cover_letter_generator = CoverLetterGenerator(resume_parser, company_research, llm_client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        data = request.json
        company_name = data.get('company_name', '').strip()
        company_website = data.get('company_website', '').strip()
        role_name = data.get('role_name', '').strip()
        role_jd = data.get('role_jd', '').strip()
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        # Generate cover letter
        cover_letter = cover_letter_generator.generate(
            company_name=company_name,
            company_website=company_website,
            role_name=role_name,
            role_jd=role_jd
        )
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter,
            'company_name': company_name,
            'role_name': role_name if role_name else 'General Position'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Cover Letter Generator API is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)