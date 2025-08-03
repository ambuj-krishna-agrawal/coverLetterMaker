# Cover Letter Generator

A Flask-based web application that generates personalized cover letters using AI, company research, and resume analysis.

## Features

- **Automated Company Research**: Multi-engine web scraping (Bing, Yahoo) for comprehensive company information
- **AI-Powered Generation**: Google Gemini API integration for intelligent cover letter creation
- **Resume Integration**: Parses resume content to extract relevant experiences and skills
- **Role-Specific Customization**: Adapts content based on job descriptions and role types
- **Experience Catalog**: Intelligent selection of most relevant projects and achievements
- **Professional Formatting**: Clean, ATS-friendly output with bold highlighting for key terms
- **Responsive UI**: Modern web interface for easy input and output management

## Technology Stack

- **Backend**: Flask (Python)
- **AI/ML**: Google Gemini API
- **Web Scraping**: BeautifulSoup, Requests
- **Document Processing**: python-docx
- **Frontend**: Bootstrap, HTML/CSS/JavaScript
- **Search**: Multi-engine approach (Bing, Yahoo)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Gemini API key (hardcoded: AIzaSyD0TI3u3s4xRh1nBmWLQQAEw0cnAzmZd5c)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ambuj-krishna-agrawal/coverLetterMaker.git
cd coverLetterMaker
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask flask-cors python-docx beautifulsoup4 requests python-dotenv google-generativeai
```

4. Place your resume:
Add your resume as `AMBUJ_AGRAWAL_RESUME_ML.docx` in the root directory

5. Run the application:
```bash
python app.py
```

6. Open your browser and go to `http://localhost:5000`

## Usage

1. **Company Name**: Enter the target company name (required)
2. **Company Website**: Optional website URL for additional research
3. **Role Name**: Position title for role-specific customization
4. **Job Description**: Paste job description for intelligent experience matching

The application will:
- Research the company automatically using 5 search results
- Analyze job requirements
- Select most relevant experiences from your background
- Generate a personalized, professional cover letter
- Provide clean output with key terms bolded

## Project Structure

```
coverLetterMaker/
├── app.py                          # Main Flask application
├── modules/
│   ├── resume_parser.py           # Resume parsing and user info extraction
│   ├── company_research.py        # Multi-engine company research
│   ├── llm_client.py             # Google Gemini API integration
│   └── cover_letter_generator.py  # Core cover letter generation logic
├── templates/
│   └── index.html                 # Main web interface
├── static/
│   ├── css/
│   │   └── style.css             # Application styling
│   └── js/
│       └── app.js                # Frontend JavaScript logic
├── resume_info.txt                # Processed resume content
├── AMBUJ_AGRAWAL_RESUME_ML.docx  # Resume document
└── README.md                     # Project documentation
```

## Key Features

### Intelligent Experience Selection
- Follows exact structure: Netflix → CMU Research → SLOT1 → SLOT2
- Automatically selects 2 most relevant projects beyond core experiences
- Role-specific focus (research vs engineering positions)
- Job description analysis for targeted matching
- Summarizes experiences instead of verbatim copying

### Company Research
- Multi-engine search approach (searches top 5 results, processes 3)
- Website scraping for comprehensive company information
- Handles unknown/fictional companies gracefully

### Technical Accuracy & Formatting
- Uses only factual content from resume
- No fabricated metrics or achievements
- Bold highlighting for key terms: Netflix, LinkedIn, CRED, CMU, +13%, 25%, granular and implicit human preferences, Routers In LLMs
- Professional closing without extra line spacing

### Cover Letter Structure
```
Paragraph 1: Opening with company excitement and background
Paragraph 2: 
  1. Netflix internship (mandatory)
  2. CMU research (mandatory) 
  3. SLOT 1 (most relevant project)
  4. SLOT 2 (second most relevant project)
Paragraph 3: Closing and contact info
```

## Experience Catalog

The application includes a comprehensive catalog of experiences:

- **Netflix**: ML Engineering Internship (audio retrieval, wav2vec2-2B, +13% improvement)
- **Carnegie Mellon**: Research on granular human preferences evaluation
- **LinkedIn**: Software Development Engineer (scalable systems, optimization)
- **CRED**: Senior SDE (payment systems, 25% cost reduction)
- **Hellosec.ai**: Startup co-founder (security analysis)
- **Academic Projects**: RAG-Chatbot, Routers In LLMs, Multimodal Web Agents

## API Endpoints

- `GET /` - Main application interface
- `POST /api/generate-cover-letter` - Generate cover letter
- `GET /api/health` - Health check

### Request Format
```json
{
  "company_name": "Apple",
  "company_website": "https://apple.com",
  "role_name": "Machine Learning Engineer", 
  "role_jd": "Job description text..."
}
```

## Contact Information

**Ambuj Krishna Agrawal**
- Email: ambujagrawal741@gmail.com
- Portfolio: https://ambuj-krishna-agrawal.github.io/
- Phone: (412) 918-0594

---

Built for efficient job application workflows with intelligent experience matching and professional formatting.