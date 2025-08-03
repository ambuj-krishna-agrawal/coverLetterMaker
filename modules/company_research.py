#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.parse

class CompanyResearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def research_company(self, company_name, company_website=None):
        """Research company information using Google search"""
        try:
            print(f"Researching {company_name}...")
            
            company_info = {
                'name': company_name,
                'website': company_website,
                'description': '',
                'industry': '',
                'key_products': [],
                'recent_news': [],
                'company_values': [],
                'size': '',
                'founded': ''
            }
            
            # If website is provided, scrape it first
            if company_website:
                print(f"Scraping website: {company_website}")
                website_info = self._scrape_company_website(company_website)
                company_info.update(website_info)
            
            # Perform Google search for company information
            print(f"Performing Google search for {company_name}...")
            search_info = self._search_company_info(company_name)
            
            # Merge search results with website info
            for key, value in search_info.items():
                if not company_info[key] and value:
                    company_info[key] = value
                elif isinstance(company_info[key], list) and isinstance(value, list):
                    company_info[key].extend(value)
            
            print(f"✅ Research completed for {company_name}")
            return company_info
            
        except Exception as e:
            print(f"❌ Error researching company {company_name}: {e}")
            raise Exception(f"Failed to research company {company_name}: {str(e)}")
    
    def _scrape_company_website(self, website_url):
        """Scrape company website for information"""
        try:
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            response = self.session.get(website_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract description from meta description or about sections
            description = ''
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            
            # Look for about section
            if not description:
                about_sections = soup.find_all(['div', 'section', 'p'], 
                    text=re.compile(r'about|mission|vision', re.I))
                if about_sections:
                    description = about_sections[0].get_text(strip=True)[:500]
            
            # Extract title for additional context
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ''
            
            return {
                'description': description,
                'website_title': title_text,
                'scraped_content': soup.get_text()[:1000]  # First 1000 chars
            }
            
        except Exception as e:
            print(f"Error scraping website {website_url}: {e}")
            return {}
    
    def _search_company_info(self, company_name):
        """Search for company information using direct Google search"""
        company_info = {
            'description': '',
            'industry': '',
            'recent_news': [],
            'key_products': []
        }
        
        try:
            search_query = f"{company_name} company about"
            print(f"Searching: {search_query}")
            
            # Use direct Google search with requests
            search_results = self._google_search(search_query, num_results=5)
            
            print(f"Found {len(search_results)} search results")
            
            for i, url in enumerate(search_results):
                if i >= 3:  # Only process first 3 results
                    break
                    
                print(f"Processing URL {i+1}: {url}")
                try:
                    content = self._scrape_search_result(url)
                    if content and len(content) > 50:
                        company_info['description'] = content[:400]
                        print(f"✅ Got description from {url}")
                        break
                except Exception as e:
                    print(f"⚠️  Failed to scrape {url}: {e}")
                    continue
                        
            return company_info
            
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            raise Exception(f"Google search failed for {company_name}: {str(e)}")

    def _google_search(self, query, num_results=5):
        """Search using multiple search engines with fallbacks"""
        try:
            print(f"Searching for: {query}")
            
            # Try Bing first (more permissive than Google/DuckDuckGo)
            search_results = self._try_bing_search(query, num_results)
            
            if search_results:
                print(f"Found {len(search_results)} results from Bing")
                return search_results[:num_results]
            
            # If Bing fails, try Yahoo
            search_results = self._try_yahoo_search(query, num_results)
            
            if search_results:
                print(f"Found {len(search_results)} results from Yahoo")
                return search_results[:num_results]
            
            # If all search engines fail, raise error
            print("All search engines failed")
            raise Exception(f"All search engines failed for query: {query}")
            
        except Exception as e:
            print(f"Error in search: {e}")
            raise Exception(f"Search failed for query '{query}': {str(e)}")
    
    def _try_bing_search(self, query, num_results=5):
        """Try Bing search"""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.bing.com/search?q={encoded_query}&count={num_results}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            search_results = []
            
            # Bing result selectors
            for result in soup.find_all('h2'):
                link = result.find('a')
                if link:
                    href = link.get('href')
                    if href and href.startswith('http') and 'bing.com' not in href:
                        search_results.append(href)
                        if len(search_results) >= num_results:
                            break
            
            return search_results
            
        except Exception as e:
            print(f"Bing search failed: {e}")
            return []
    
    def _try_yahoo_search(self, query, num_results=5):
        """Try Yahoo search"""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://search.yahoo.com/search?p={encoded_query}&n={num_results}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            search_results = []
            
            # Yahoo result selectors
            for result in soup.find_all('h3', class_='title'):
                link = result.find('a')
                if link:
                    href = link.get('href')
                    if href and href.startswith('http') and 'yahoo.com' not in href:
                        search_results.append(href)
                        if len(search_results) >= num_results:
                            break
            
            return search_results
            
        except Exception as e:
            print(f"Yahoo search failed: {e}")
            return []
    
    
    def _scrape_search_result(self, url):
        """Scrape content from search result URL - simplified and faster"""
        try:
            response = self.session.get(url, timeout=3)  # Reduced timeout
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Quick text extraction - just get first few paragraphs
            paragraphs = soup.find_all('p')[:3]  # Only first 3 paragraphs
            text_content = ' '.join([p.get_text().strip() for p in paragraphs])
            
            return text_content[:500]  # Return first 500 characters
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
    
    def research_role(self, role_name, company_name):
        """Research specific role requirements"""
        try:
            if not role_name:
                return {
                    'title': 'General Position',
                    'responsibilities': [],
                    'requirements': [],
                    'skills_needed': []
                }
            
            role_info = {
                'title': role_name,
                'responsibilities': [],
                'requirements': [],
                'skills_needed': []
            }
            
            # Role research not implemented - return empty info
            # Cover letter generator should work without detailed role research
            
            return role_info
            
        except Exception as e:
            print(f"Error researching role {role_name}: {e}")
            raise Exception(f"Failed to research role {role_name}: {str(e)}")
    
    def _extract_role_details(self, content, detail_type):
        """Extract specific details from job content"""
        details = []
        content_lower = content.lower()
        
        # Define keywords for different sections
        keywords = {
            'responsibilities': ['responsibilities', 'duties', 'role', 'what you will do'],
            'requirements': ['requirements', 'qualifications', 'experience', 'must have'],
            'skills': ['skills', 'technologies', 'tools', 'programming', 'technical']
        }
        
        try:
            for keyword in keywords.get(detail_type, []):
                if keyword in content_lower:
                    # Find content after the keyword
                    start_idx = content_lower.find(keyword)
                    if start_idx != -1:
                        # Extract next 300 characters and split by sentences
                        section_content = content[start_idx:start_idx+300]
                        sentences = section_content.split('.')
                        details.extend([s.strip() for s in sentences[:3] if len(s.strip()) > 10])
                        break
        except Exception as e:
            print(f"Error extracting {detail_type}: {e}")
        
        return details[:5]  # Return max 5 items
    
    
