// Cover Letter Generator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('coverLetterForm');
    const generateBtn = document.getElementById('generateBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const welcomeMessage = document.getElementById('welcomeMessage');
    const coverLetterOutput = document.getElementById('coverLetterOutput');
    const errorMessage = document.getElementById('errorMessage');
    const coverLetterText = document.getElementById('coverLetterText');
    const outputTitle = document.getElementById('outputTitle');

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
            
            // Make API call
            const response = await fetch('/api/generate-cover-letter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate cover letter');
            }

            // Show the generated cover letter
            showCoverLetter(data);

        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'An error occurred while generating the cover letter');
        } finally {
            hideLoading();
        }
    });

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
        
        // Update title
        const roleText = data.role_name ? `for ${data.role_name}` : '';
        outputTitle.textContent = `Cover Letter ${roleText} at ${data.company_name}`;
        
        // Set cover letter content (using innerHTML to render bold tags)
        coverLetterText.innerHTML = data.cover_letter;
        
        // Show the output
        coverLetterOutput.style.display = 'block';
        
        // Scroll to output on mobile
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
        
        // Scroll to error on mobile
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

    // Form validation feedback
    const inputs = form.querySelectorAll('input[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });
});

// Copy to clipboard function
function copyToClipboard() {
    const coverLetterText = document.getElementById('coverLetterText');
    
    // Create a temporary textarea to copy from (using textContent to get plain text)
    const tempTextArea = document.createElement('textarea');
    tempTextArea.value = coverLetterText.textContent;
    document.body.appendChild(tempTextArea);
    
    // Select and copy
    tempTextArea.select();
    document.execCommand('copy');
    
    // Remove temporary element
    document.body.removeChild(tempTextArea);
    
    // Show feedback
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

// Download cover letter function
function downloadCoverLetter() {
    const coverLetterText = document.getElementById('coverLetterText');
    const outputTitle = document.getElementById('outputTitle');
    
    // Create downloadable content
    const content = coverLetterText.textContent;
    const filename = `${outputTitle.textContent.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.txt`;
    
    // Create and trigger download
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    
    // Show feedback
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

// Health check on page load
fetch('/api/health')
    .then(response => response.json())
    .then(data => {
        console.log('API Status:', data.message);
    })
    .catch(error => {
        console.warn('API health check failed:', error);
    });