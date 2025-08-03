#!/usr/bin/env python3

from .resume_parser import ResumeParser
from .company_research import CompanyResearch
from .llm_client import LLMClient

class CoverLetterGenerator:
    def __init__(self, resume_parser: ResumeParser, company_research: CompanyResearch, llm_client: LLMClient):
        self.resume_parser = resume_parser
        self.company_research = company_research
        self.llm_client = llm_client
        
        # Experience catalog for targeted content
        self.experience_catalog = {
            'linkedin_experience': {
                'company': 'LinkedIn',
                'role': 'Software Development Engineer',
                'achievements': [
                    'Built scalable authentication and security systems for millions of users',
                    'Optimized distributed systems and streaming pipelines reducing resource consumption by 50%',
                    'Collaborated across teams to deliver high-impact features for user engagement'
                ],
                'skills': ['distributed systems', 'scalable architecture', 'security', 'optimization']
            },
            'netflix_experience': {
                'company': 'Netflix',
                'role': 'ML Engineering Intern',
                'achievements': [
                    'Built catalog-wide audio-retrieval platform for synthetic dubbing',
                    'Fine-tuned wav2vec2-2B with contrastive loss improving synthetic voice quality by +13% in human preference (CMOS +0.2)',
                    'Developed auto-evaluation suite with human evaluation study for model optimization',
                    'Achieved 7.5% improvement in auto-evaluations for emotion and speaker style matching'
                ],
                'skills': ['ML infrastructure', 'model fine-tuning', 'human evaluation', 'audio processing', 'contrastive learning']
            },
            'cmu_research': {
                'institution': 'Carnegie Mellon University',
                'focus': 'Research Assistant under Dr. Fernando Diaz',
                'achievements': [
                    'Proposed a new evaluation framework focusing on capturing granular and implicit human preferences through targeted masking and infilling',
                    'Results show increase in inter-annotator agreement, lesser cognitive overload, and increased overall quality of human annotation',
                    'Advanced coursework in NLP, Multimodal ML, Search and Recommendation systems'
                ],
                'skills': ['human preference evaluation', 'annotation frameworks', 'NLP research', 'evaluation methodologies']
            },
            'cred_experience': {
                'company': 'CRED',
                'role': 'Senior Software Development Engineer',
                'achievements': [
                    'Built core components in bill payments platform powering credit cards, electricity, rent, and gift vouchers',
                    'Led zero-to-one products that added $30 Million monthly revenue stream handling 100+ QPS spiky traffic',
                    'Solved complex native memory leak in JVM due to memory fragmentation, cutting AWS cost by 25%',
                    'Developed pipeline to deploy product config saving $150k annually, team placed third in 70+ submissions'
                ],
                'skills': ['distributed systems', 'JVM optimization', 'high-scale platforms', 'cost optimization', 'payment systems']
            },
            'hellosec_startup': {
                'name': 'Hellosec.ai',
                'role': 'Co-founder',
                'achievements': [
                    'Cofounded startup that auto-scans PRDs/tech specs with multimodal web agent',
                    'Built system simulating requests, analyzing responses, surfacing compliance & security gaps',
                    'Created real-time "security copilot" for automated security analysis'
                ],
                'skills': ['entrepreneurship', 'security analysis', 'multimodal agents', 'web automation', 'compliance']
            },
            'rag_chatbot_project': {
                'name': 'RAG-Chatbot',
                'description': 'Retrieval-Augmented Generation pipeline for Pittsburgh information',
                'achievements': [
                    'Developed RAG pipeline using multi-query, cross encoders, lost in the middle, BM25, and vector embeddings',
                    'Built with Langchain and scraped over 5000 documents using selenium',
                    'Implemented advanced retrieval techniques to answer latest questions about Pittsburgh'
                ],
                'skills': ['information retrieval', 'RAG systems', 'vector embeddings', 'multi-query retrieval', 'cross-encoders']
            },
            'routers_llms_project': {
                'name': 'Routers In LLMs',
                'description': 'Novel method for synthetic preference data and model routing',
                'achievements': [
                    'Developed novel method to obtain synthetic preference data between open-source models with scarce existing preference data',
                    'Built routers by fine-tuning Llama models and matrix factorization using new data to enhance routing',
                    'Tested on GSM8K dataset for mathematical reasoning tasks'
                ],
                'skills': ['LLM optimization', 'preference learning', 'model routing', 'fine-tuning', 'mathematical reasoning']
            },
            'multimodal_agents_project': {
                'name': 'Multimodal Web Agents',
                'description': 'Ensemble verifier agents with tree search for web automation',
                'achievements': [
                    'Developed ensemble of verifier agents using tree search algorithm',
                    'Addressed web agents inefficiencies by pruning unnecessary paths',
                    'Improved resource efficiency and accuracy, benchmarked on VisualWebArena dataset'
                ],
                'skills': ['multimodal AI', 'web automation', 'tree search algorithms', 'agent systems', 'efficiency optimization']
            },
            'core_background': {
                'education': 'Master\'s in Natural Language Processing from Carnegie Mellon University (graduating Dec 2025)',
                'total_experience': '3+ years of industry experience',
                'key_companies': ['LinkedIn', 'Netflix', 'CRED'],
                'core_skills': ['machine learning', 'distributed systems', 'software engineering', 'NLP', 'information retrieval']
            },
            'technical_skills': {
                'programming_languages': ['Python', 'Java', 'C++', 'SQL', 'NOSQL', 'Go'],
                'frameworks_and_tools': [
                    'PyTorch', 'vLLM', 'Huggingface', 'Keras', 'Numpy', 'Pandas', 
                    'Langchain', 'Flask', 'scikit-learn', 'NLTK', 'Kafka', 'AWS', 
                    'Spacy', 'MTurk', 'Labelbox'
                ],
                'specializations': [
                    'Machine Learning', 'Deep Learning', 'NLP', 'Information Retrieval',
                    'Distributed Systems', 'Cloud Computing', 'Data Processing'
                ]
            }
        }
    
    def generate(self, company_name: str, company_website: str = None, role_name: str = None, role_jd: str = None) -> str:
        """Generate a personalized cover letter"""
        try:
            # Get user information
            user_info = self.resume_parser.get_user_info()
            
            # Research company
            print(f"Researching company: {company_name}")
            company_info = self.company_research.research_company(company_name, company_website)
            
            # Research role if provided
            role_info = None
            if role_name:
                print(f"Researching role: {role_name}")
                role_info = self.company_research.research_role(role_name, company_name)
            
            # Generate cover letter using LLM
            prompt = self._create_cover_letter_prompt(user_info, company_info, role_info, role_jd)
            cover_letter = self.llm_client.generate_text(prompt, max_tokens=800, temperature=0.6)
            
            # Post-process the cover letter
            cover_letter = self._post_process_cover_letter(cover_letter, user_info, company_name, role_name)
            
            return cover_letter
            
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            raise Exception(f"Failed to generate cover letter for {company_name}: {str(e)}")
    
    def _create_cover_letter_prompt(self, user_info: dict, company_info: dict, role_info: dict = None, role_jd: str = None) -> str:
        """Create a detailed prompt for the LLM to generate the cover letter"""
        
        # Select relevant experiences based on job requirements
        relevant_experiences = self._select_relevant_experiences(role_jd, role_info)
        
        prompt = f"""
You are an expert cover letter writer. Create a human-written, professional cover letter that follows this EXACT template and structure.

COMPANY INFORMATION:
Company: {company_info.get('name', 'Unknown Company')}
Description: {company_info.get('description', 'A technology company')}
Domain/Industry: {company_info.get('industry', 'Technology')}

ROLE INFORMATION:
Position: {role_info.get('title', 'Software Engineer') if role_info else 'the position'}

JOB DESCRIPTION (analyze for requirements and connect to my experiences):
{role_jd if role_jd else 'No specific job description provided'}

EXPERIENCE CATALOG TO USE:
{self._format_experience_catalog(relevant_experiences)}

CRITICAL INSTRUCTIONS:
1. EXACT STRUCTURE - 3 paragraphs with this MANDATORY flow:

PARAGRAPH 1 (Opening):
- Excitement to apply for [Role] at [Company] because of their reputation in [specific domain from company info]
- CRITICAL: Add a line that EXPLICITLY connects your most relevant previous work to this specific job description. Analyze the job requirements and state "My experience in [specific area from catalog that matches job] at [company] makes me uniquely qualified for this role"
- Brief background: Master's in NLP from CMU (graduating Dec 2025) and industry experience at LinkedIn, Netflix, and CRED
- Value proposition aligned with their mission

PARAGRAPH 2 (Experience - EXACT ORDER):
This paragraph MUST follow this EXACT sequence:
1. START with Netflix internship: "During my recent ML Engineering internship at Netflix, I built a catalog wide audio retrieval platform and fine tuned wav2vec2 2B with contrastive loss, improving synthetic voice quality by +13% in human preference (CMOS + 0.2)."
2. THEN CMU research: Use EXACT text from catalog about "evaluation framework focusing on capturing granular and implicit human preferences through targeted masking and infilling" and its impact
3. SLOT 1: Select ONE most relevant project from catalog that connects to job requirements
4. SLOT 2: Select ONE more project from catalog that connects to job requirements

PARAGRAPH 3 (Closing):
- Eagerness to contribute to [Company] products
- Thank you and looking forward to discussion
- How background contributes to team success

2. JOB REQUIREMENT MATCHING:
- CAREFULLY analyze the job description for specific technical requirements, skills, domains, programming languages, and frameworks
- PRIORITY: Look for technical skill matches between job requirements and my technical_skills catalog (Python, Java, C++, PyTorch, AWS, etc.)
- When mentioning experiences, weave in relevant technical skills that match the job description
- For each SLOT (3rd and 4th experiences), EXPLICITLY explain HOW that experience connects to job requirements
- Use phrases like "directly applicable to [specific requirement]", "relevant to [company domain]", "experience in [required skill]"
- SKILL MATCHING: When job description mentions specific technologies/frameworks I have, naturally incorporate them (e.g., "using PyTorch and Huggingface", "leveraging AWS infrastructure", "implemented in Python")
- BUT NEVER make up connections that don't exist - only use what's actually in my experience catalog

3. SLOT SELECTION CRITERIA:
- SLOT 1 & 2: Choose the 2 most relevant projects from the catalog based on:
  * Direct technical overlap with job requirements
  * Company domain relevance (e.g., search → RAG project, ML → routers project, security → Hellosec)
  * Specific skills mentioned in job description
- Prioritize experiences that have concrete technical details matching job needs
- IMPORTANT: For SLOT 1 & 2, do NOT copy the exact text from the experience catalog verbatim
- Instead, SUMMARIZE and CONDENSE each selected experience to include only the most essential and impactful details
- Focus on the key outcome, main technology used, and direct relevance to the job requirements
- Keep each slot description to 1-2 sentences maximum to maintain flow and readability

4. TECHNICAL ACCURACY:
- Use ONLY factual content from experience catalog as source of truth
- Do NOT make up numbers, metrics, or details not in the catalog
- NEVER use symbols like dashes, hyphens, or special characters
- For SLOT 1 & 2: Summarize and condense the catalog content while keeping all technical details and metrics accurate
- You can rephrase and shorten descriptions, but NEVER change or invent technical specifications, numbers, or outcomes

5. TONE AND STYLE:
- Human, conversational tone (not AI-generated)
- Confident and direct
- No flowery language or overly formal phrases

6. OUTPUT FORMAT:
Return ONLY the regular text version without any formatting or bold tags.

7. CONTACT INFO: End with: 
ambujagrawal741@gmail.com | (412) 918-0594 | https://ambuj-krishna-agrawal.github.io/

Generate the cover letter now, following the EXACT Netflix → CMU → SLOT1 → SLOT2 structure in paragraph 2:
"""
        
        return prompt
    
    def _select_relevant_experiences(self, role_jd: str = None, role_info: dict = None) -> dict:
        """Send ALL experiences to LLM for intelligent selection"""
        # Send ALL experiences - let LLM decide what's most relevant
        return self.experience_catalog
    
    def _format_experience_catalog(self, experiences: dict) -> str:
        """Format the experience catalog for the prompt"""
        formatted = []
        
        for key, exp in experiences.items():
            if key == 'linkedin_experience':
                formatted.append("LINKEDIN EXPERIENCE:")
                formatted.append(f"- {exp['role']} at {exp['company']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'netflix_experience':
                formatted.append("\nNETFLIX EXPERIENCE:")
                formatted.append(f"- {exp['role']} at {exp['company']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'cred_experience':
                formatted.append("\nCRED EXPERIENCE:")
                formatted.append(f"- {exp['role']} at {exp['company']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'cmu_research':
                formatted.append(f"\nCMU RESEARCH:")
                formatted.append(f"- {exp['focus']} at {exp['institution']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'hellosec_startup':
                formatted.append(f"\nHELLOSEC.AI STARTUP:")
                formatted.append(f"- {exp['role']}: {exp['name']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'rag_chatbot_project':
                formatted.append(f"\nRAG-CHATBOT PROJECT:")
                formatted.append(f"- {exp['name']}: {exp['description']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'routers_llms_project':
                formatted.append(f"\nROUTERS IN LLMS PROJECT:")
                formatted.append(f"- {exp['name']}: {exp['description']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'multimodal_agents_project':
                formatted.append(f"\nMULTIMODAL WEB AGENTS PROJECT:")
                formatted.append(f"- {exp['name']}: {exp['description']}")
                for achievement in exp['achievements']:
                    formatted.append(f"  • {achievement}")
                    
            elif key == 'core_background':
                formatted.append(f"\nCORE BACKGROUND:")
                formatted.append(f"- Education: {exp['education']}")
                formatted.append(f"- Experience: {exp['total_experience']}")
                formatted.append(f"- Companies: {', '.join(exp['key_companies'])}")
                
            elif key == 'technical_skills':
                formatted.append(f"\nTECHNICAL SKILLS:")
                formatted.append(f"- Programming Languages: {', '.join(exp['programming_languages'])}")
                formatted.append(f"- Frameworks & Tools: {', '.join(exp['frameworks_and_tools'])}")
                formatted.append(f"- Specializations: {', '.join(exp['specializations'])}")
        
        return '\n'.join(formatted)
    
    def _format_list(self, items: list) -> str:
        """Format a list of items for the prompt"""
        if not items:
            return "Not specified"
        
        if isinstance(items[0], str):
            return '\n'.join(f"• {item}" for item in items[:5])  # Max 5 items
        else:
            return '\n'.join(f"• {str(item)}" for item in items[:5])
    
    def _post_process_cover_letter(self, cover_letter: str, user_info: dict, company_name: str, role_name: str = None) -> str:
        """Post-process the generated cover letter and return clean version"""
        try:
            # Clean any version indicators from LLM response
            if "REGULAR VERSION:" in cover_letter:
                cover_letter = cover_letter.split("REGULAR VERSION:")[1]
            if "BOLD VERSION:" in cover_letter:
                cover_letter = cover_letter.split("BOLD VERSION:")[0]
            
            # Return cleaned version
            return self._clean_cover_letter(cover_letter, user_info, company_name, role_name)
            
        except Exception as e:
            print(f"Error post-processing cover letter: {e}")
            return cover_letter
    
    def _clean_cover_letter(self, cover_letter: str, user_info: dict, company_name: str, role_name: str = None) -> str:
        """Clean and format a single version of cover letter"""
        # Remove any remaining placeholder text
        cover_letter = cover_letter.replace('[COMPANY]', company_name)
        cover_letter = cover_letter.replace('[ROLE]', role_name or 'the position')
        cover_letter = cover_letter.replace('[NAME]', user_info.get('name', 'Ambuj Krishna Agrawal'))
        
        # Ensure proper formatting
        paragraphs = cover_letter.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('---'):  # Remove mock response notes
                formatted_paragraphs.append(para)
        
        # Add proper greeting if missing
        if not formatted_paragraphs[0].startswith('Dear'):
            formatted_paragraphs.insert(0, 'Dear Hiring Manager,')
        
        # Add proper closing if missing
        if not formatted_paragraphs[-1].startswith(('Sincerely', 'Best regards', 'Thank you')):
            formatted_paragraphs.append('Sincerely,\nAmbuj Krishna Agrawal')
        
        # Apply bolding to specific key terms
        final_content = '\n\n'.join(formatted_paragraphs)
        final_content = self._apply_bold_formatting(final_content)
        
        return final_content
    
    def _apply_bold_formatting(self, content: str) -> str:
        """Apply HTML bold tags to specific key terms"""
        # Define terms to bold
        bold_terms = [
            'Netflix',
            'LinkedIn', 
            'CRED',
            'CMU',
            'graduating in December 2025',
            '+13%',
            'CMOS + 0.2',
            'CMOS +0.2',
            'Carnegie Mellon University',
            'granular and implicit human preferences',
            'Routers In LLMs',
            'Multimodal Web Agents',
            '25%'
        ]
        
        # Apply bold formatting
        import re
        for term in bold_terms:
            # Handle special cases for terms with symbols
            if term in ['+13%', '25%', 'CMOS + 0.2', 'CMOS +0.2']:
                # For terms with symbols, use exact match with word boundaries where appropriate
                escaped_term = re.escape(term)
                if term.startswith('+'):
                    pattern = r'(?<!\w)' + escaped_term + r'(?!\w)'
                else:
                    pattern = r'\b' + escaped_term + r'\b'
            else:
                # Use word boundaries for regular terms
                pattern = r'\b' + re.escape(term) + r'\b'
            
            content = re.sub(pattern, f'<b>{term}</b>', content, flags=re.IGNORECASE)
        
        return content
    
