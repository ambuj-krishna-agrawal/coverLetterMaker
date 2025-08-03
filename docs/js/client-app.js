// Client-side Cover Letter Generator (GitHub Pages version)

// User resume data (extracted from the resume)
const USER_RESUME_DATA = {
    name: 'Ambuj Krishna Agrawal',
    email: 'ambuja@andrew.cmu.edu',
    phone: '(412) 918-0594',
    website: 'https://ambuj-krishna-agrawal.github.io/',
    education: [
        'Carnegie Mellon University - Master of Science in Natural Language Processing (AI) - GPA: 3.92/4 - December 2025',
        'Indian Institute of Information Technology, Allahabad - Bachelor of Technology in Information Technology - 8.82/10 - July 2021'
    ],
    experience: [
        'Netflix - Machine Learning Engineering Intern (May 2025 – August 2025): Built full-catalog audio retrieval system, improved synthetic dubbing by 7.5% auto-eval and 13% human preference',
        'Carnegie Mellon University - ML Research Assistant (Sep 2024 – May 2025): Worked under Dr. Fernando Diaz on evaluation framework for human preferences',
        'CRED - Senior Software Development Engineer (Feb 2023 – July 2024): Built core bill payments platform, led products worth $30M monthly revenue',
        'LinkedIn - Software Development Engineer (July 2021 – Feb 2023): Upgraded authentication, fixed security vulnerabilities, optimized user processing'
    ],
    skills: [
        'Python', 'Java', 'C++', 'SQL', 'NoSQL', 'Go',
        'PyTorch', 'Keras', 'Numpy', 'Pandas', 'Langchain', 'Flask', 'scikit-learn', 'NLTK', 'Kafka', 'AWS', 'Spacy'
    ],
    projects: [
        'Hellosec.ai - Cofounded security copilot startup with multimodal web agent',
        'RAG-Chatbot - Developed RAG pipeline using multi-query, cross encoders, BM25',
        'Routers In LLMs - Developed synthetic preference data method for open-source models',
        'Multimodal Web Agents - Built ensemble verifier agents using tree search algorithm'
    ]
};

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('coverLetterForm');
    const generateBtn = document.getElementById('generateBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const welcomeMessage = document.getElementById('welcomeMessage');
    const coverLetterOutput = document.getElementById('coverLetterOutput');
    const errorMessage = document.getElementById('errorMessage');
    const coverLetterText = document.getElementById('coverLetterText');
    const outputTitle = document.getElementById('outputTitle');
    const llmProvider = document.getElementById('llmProvider');
    const apiKeySection = document.getElementById('apiKeySection');

    // Gemini is now the only provider, no need for provider selection

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = {
            company_name: document.getElementById('companyName').value.trim(),
            company_website: document.getElementById('companyWebsite').value.trim(),
            role_name: document.getElementById('roleName').value.trim(),
            role_jd: document.getElementById('jobDescription').value.trim()
        };

        // Validate required fields
        if (!formData.company_name) {
            showError('Company name is required');
            return;
        }

        try {
            // Show loading state
            showLoading();
            
            // Generate cover letter
            const coverLetter = await generateCoverLetter(formData);
            
            // Show the generated cover letter
            showCoverLetter({
                success: true,
                cover_letter: coverLetter,
                company_name: formData.company_name,
                role_name: formData.role_name
            });

        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'An error occurred while generating the cover letter');
        } finally {
            hideLoading();
        }
    });

    async function generateCoverLetter(formData) {
        // Simulate company research (simplified for client-side)
        const companyInfo = await simulateCompanyResearch(formData.company_name, formData.company_website);
        
        // Generate cover letter using Gemini API (via backend)
        return await generateGeminiCoverLetter(formData, companyInfo);
    }

    async function simulateCompanyResearch(companyName, website) {
        // Simulate a delay for research
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Basic company info (in a real implementation, this would use web scraping APIs)
        const companyInfo = {
            name: companyName,
            website: website,
            description: `${companyName} is a leading company known for innovation and excellence in its industry.`,
            industry: 'Technology',
            values: ['Innovation', 'Excellence', 'Collaboration', 'Growth']
        };
        
        // Try to infer industry from company name
        const techCompanies = ['google', 'microsoft', 'apple', 'amazon', 'netflix', 'meta', 'tesla', 'nvidia'];
        const financeCompanies = ['goldman', 'morgan', 'jpmorgan', 'wells fargo', 'bank of america'];
        
        const lowerName = companyName.toLowerCase();
        if (techCompanies.some(tech => lowerName.includes(tech))) {
            companyInfo.industry = 'Technology';
            companyInfo.description = `${companyName} is a leading technology company driving innovation in digital products and services.`;
        } else if (financeCompanies.some(fin => lowerName.includes(fin))) {
            companyInfo.industry = 'Financial Services';
            companyInfo.description = `${companyName} is a prominent financial institution providing comprehensive banking and investment services.`;
        }
        
        return companyInfo;
    }

    function generateMockCoverLetter(formData, companyInfo) {
        const roleText = formData.role_name ? `the ${formData.role_name} position` : 'a position';
        
        return `Dear Hiring Manager,

I am writing to express my strong interest in ${roleText} at ${formData.company_name}. As a Machine Learning Engineer with experience at Netflix and a Master's student in Natural Language Processing at Carnegie Mellon University, I am excited about the opportunity to contribute to your team.

During my internship at Netflix, I built a full-catalog audio retrieval system that improved synthetic dubbing quality by 7.5% through auto-evaluation and 13% through human preference studies. This experience, combined with my research background in multimodal machine learning and web agents, has prepared me well for the challenges of this role.

My technical expertise includes Python, PyTorch, machine learning, and distributed systems, which I developed through roles at CRED and LinkedIn. At CRED, I led zero-to-one products that added a revenue stream worth $30 Million a month and solved complex memory leak issues that cut AWS costs by 25%.

${companyInfo.description} I am particularly drawn to ${formData.company_name}'s innovative approach and believe my background in AI and software engineering would allow me to make meaningful contributions to your team.

I would welcome the opportunity to discuss how my experience and passion for technology can benefit ${formData.company_name}. Thank you for your consideration.

Sincerely,
${USER_RESUME_DATA.name}`;
    }

    async function generateGeminiCoverLetter(formData, companyInfo) {
        // For the static version, we'll use the Flask backend API
        // In a real deployment, you'd either:
        // 1. Use the Flask backend hosted somewhere
        // 2. Implement direct Gemini API calls (requires handling CORS)
        
        // Try to call the Flask backend first
        try {
            const response = await fetch('/api/generate-cover-letter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();
                return data.cover_letter;
            }
        } catch (error) {
            console.log('Backend not available, using fallback');
        }
        
        // Fallback to mock if backend is not available
        return generateMockCoverLetter(formData, companyInfo);
    }

    function createCoverLetterPrompt(formData, companyInfo) {
        const roleInfo = formData.role_jd ? `\nRole Description: ${formData.role_jd}` : '';
        
        return `You are an expert cover letter writer. Create a professional, personalized cover letter based on the following information:

CANDIDATE INFORMATION:
Name: ${USER_RESUME_DATA.name}
Email: ${USER_RESUME_DATA.email}
Phone: ${USER_RESUME_DATA.phone}
Website: ${USER_RESUME_DATA.website}

Education:
${USER_RESUME_DATA.education.map(edu => `• ${edu}`).join('\n')}

Work Experience:
${USER_RESUME_DATA.experience.map(exp => `• ${exp}`).join('\n')}

Key Skills:
${USER_RESUME_DATA.skills.join(', ')}

Notable Projects:
${USER_RESUME_DATA.projects.map(proj => `• ${proj}`).join('\n')}

COMPANY INFORMATION:
Company: ${companyInfo.name}
Industry: ${companyInfo.industry}
Description: ${companyInfo.description}
${roleInfo}

ROLE: ${formData.role_name || 'General Position'}

INSTRUCTIONS:
1. Write a professional cover letter that is 3-4 paragraphs long
2. Start with a strong opening that mentions the specific role and company
3. Highlight the most relevant experience and skills that match the role
4. Show knowledge of the company and explain why you're interested
5. Include specific achievements and quantified results
6. End with a strong call to action
7. Keep the tone professional but engaging
8. Make it personal and specific to this candidate and company

Generate the cover letter now:`;
    }


    // UI Helper Functions (same as server version)
    function showLoading() {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        loadingIndicator.style.display = 'block';
        hideError();
        hideCoverLetter();
    }

    function hideLoading() {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Cover Letter';
        loadingIndicator.style.display = 'none';
    }

    function showCoverLetter(data) {
        hideWelcomeMessage();
        hideError();
        
        const roleText = data.role_name ? `for ${data.role_name}` : '';
        outputTitle.textContent = `Cover Letter ${roleText} at ${data.company_name}`;
        
        coverLetterText.textContent = data.cover_letter;
        coverLetterOutput.style.display = 'block';
        
        if (window.innerWidth <= 768) {
            coverLetterOutput.scrollIntoView({ behavior: 'smooth' });
        }
    }

    function hideCoverLetter() {
        coverLetterOutput.style.display = 'none';
    }

    function showError(message) {
        hideWelcomeMessage();
        hideCoverLetter();
        
        document.getElementById('errorText').textContent = message;
        errorMessage.style.display = 'block';
        
        if (window.innerWidth <= 768) {
            errorMessage.scrollIntoView({ behavior: 'smooth' });
        }
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function hideWelcomeMessage() {
        welcomeMessage.style.display = 'none';
    }

    // Auto-resize textarea
    const textarea = document.getElementById('jobDescription');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});

// Copy and download functions (same as server version)
function copyToClipboard() {
    const coverLetterText = document.getElementById('coverLetterText');
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = coverLetterText.textContent;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    document.execCommand('copy');
    document.body.removeChild(tempTextArea);
    
    const copyBtn = event.target.closest('button');
    const originalText = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    copyBtn.classList.add('btn-success');
    copyBtn.classList.remove('btn-outline-primary');
    
    setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.classList.remove('btn-success');
        copyBtn.classList.add('btn-outline-primary');
    }, 2000);
}

function downloadCoverLetter() {
    const coverLetterText = document.getElementById('coverLetterText');
    const outputTitle = document.getElementById('outputTitle');
    
    const content = coverLetterText.textContent;
    const filename = `${outputTitle.textContent.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.txt`;
    
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    
    const downloadBtn = event.target.closest('button');
    const originalText = downloadBtn.innerHTML;
    downloadBtn.innerHTML = '<i class="fas fa-check"></i> Downloaded!';
    downloadBtn.classList.add('btn-success');
    downloadBtn.classList.remove('btn-outline-success');
    
    setTimeout(() => {
        downloadBtn.innerHTML = originalText;
        downloadBtn.classList.remove('btn-success');
        downloadBtn.classList.add('btn-outline-success');
    }, 2000);
}