import requests
import csv
import json
import time
import random
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import cloudscraper
import os
from datetime import datetime


class BarkScraper:
    """
    Advanced Bark.com scraper for extracting contact information from service providers.
    Handles anti-bot protection and provides data filtering capabilities.
    """
    
    def __init__(self, headless: bool = True):
        self.base_url = "https://www.bark.com/en/gb/"
        self.session = self._setup_session()
        self.driver = None
        self.headless = headless
        self.ua = UserAgent()
        self.scraped_data = []
        
        # Service categories mapping
        self.service_categories = {
            'home': ['cleaners', 'gardeners', 'builders', 'electricians', 'plumbers', 'painters'],
            'health': ['personal-trainer', 'therapy', 'massage', 'nutrition'],
            'business': ['web-design', 'accountants', 'marketing', 'photography'],
            'events': ['dj', 'photographer', 'catering', 'entertainment'],
            'lessons': ['music-lessons', 'tutoring', 'driving-lessons']
        }
        
        # UK regions for location filtering
        self.uk_regions = [
            'london', 'birmingham', 'manchester', 'liverpool', 'leeds', 'sheffield',
            'bristol', 'glasgow', 'leicester', 'coventry', 'nottingham', 'newcastle',
            'belfast', 'cardiff', 'edinburgh', 'brighton', 'plymouth', 'stoke-on-trent'
        ]
    
    def _setup_session(self) -> requests.Session:
        """Setup cloudscraper session to bypass Cloudflare protection"""
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        return scraper
    
    def _setup_driver(self) -> uc.Chrome:
        """Setup undetected Chrome driver for dynamic content"""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'--user-agent={self.ua.random}')
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def get_service_providers_urls(self, service: str, location: str = None, max_pages: int = 5) -> List[str]:
        """
        Extract URLs of individual service provider profiles from Bark.com
        """
        urls = []
        
        # Construct search URL based on current Bark.com structure
        if location:
            # Format: /en/gb/{service}/{location}/
            search_url = f"{self.base_url}{service}/{location.lower()}/"
        else:
            # Format: /en/gb/{service}/
            search_url = f"{self.base_url}{service}/"
        
        print(f"Searching for {service} providers in {location or 'all locations'}...")
        print(f"URL: {search_url}")
        
        try:
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for "View Profile" links which lead to provider profiles
            # Current structure: /en/gb/company/{name}/{id}/
            view_profile_links = soup.find_all('a', string='View Profile')
            
            for link in view_profile_links:
                href = link.get('href', '')
                if href and '/company/' in href:
                    full_url = urljoin('https://www.bark.com', href)
                    if full_url not in urls:
                        urls.append(full_url)
            
            # Also look for direct profile links in the HTML
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                # Match new Bark provider profile URL pattern: /en/gb/company/name/id/
                if re.match(r'^/en/gb/company/[^/]+/[A-Za-z0-9]+/?$', href):
                    full_url = urljoin('https://www.bark.com', href)
                    if full_url not in urls:
                        urls.append(full_url)
                        
        except Exception as e:
            print(f"Error fetching providers from {search_url}: {e}")
        
        print(f"Found {len(urls)} provider URLs")
        return urls
    
    def _has_next_page(self, soup: BeautifulSoup) -> bool:
        """Check if there's a next page"""
        next_button = soup.find('a', string='Next') or soup.find('a', {'aria-label': 'Next page'})
        return next_button is not None
    
    def scrape_provider_profile(self, url: str) -> Optional[Dict]:
        """
        Scrape individual provider profile for contact information
        """
        try:
            print(f"Scraping profile: {url}")
            
            # Try with session first (faster)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract provider information using updated selectors
            provider_data = {
                'url': url,
                'name': self._extract_name(soup),
                'description': self._extract_description(soup),
                'services': self._extract_services_from_soup(soup),
                'location': self._extract_location_from_soup(soup),
                'rating': self._extract_rating_from_soup(soup),
                'reviews_count': self._extract_reviews_count_from_soup(soup),
                'phone': None,  # Usually requires interaction
                'email': None,  # Usually requires interaction  
                'website': None,  # Usually requires interaction
                'facebook': None,  # Usually requires interaction
                'scraped_at': datetime.now().isoformat()
            }
            
            # Try to get contact info if available publicly
            contact_info = self._extract_contact_info_from_soup(soup)
            provider_data.update(contact_info)
            
            # Clean up the data
            provider_data = {k: (v if v not in [None, '', []] else None) for k, v in provider_data.items()}
            provider_data = {k: v for k, v in provider_data.items() if v is not None}
            
            print(f"✓ Scraped: {provider_data.get('name', 'Unknown')}")
            return provider_data
            
        except Exception as e:
            print(f"✗ Error scraping {url}: {e}")
            return None

    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract provider name"""
        selectors = ['h1', '.company-name', '[data-testid="company-name"]']
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract provider description"""
        # Look for About section content
        about_section = soup.find('h4', string='About')
        if about_section:
            # Get the next paragraph or div after "About"
            next_elem = about_section.find_next_sibling()
            if next_elem:
                text = next_elem.get_text(strip=True)
                if text:
                    return text
        
        # Fallback selectors
        selectors = [
            '.about-content',
            '.company-description', 
            '.seller-description',
            'p:contains("provide")',
            'div:contains("service")'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if len(text) > 50:  # Only return substantial descriptions
                    return text
        return None

    def _extract_services_from_soup(self, soup: BeautifulSoup) -> List[str]:
        """Extract list of services offered"""
        services = []
        
        # Look for service badges/links
        service_links = soup.find_all('a', href=True)
        for link in service_links:
            href = link.get('href', '')
            if '/en/gb/' in href and any(service in href for service in ['cleaners', 'cleaning', 'commercial']):
                service_text = link.get_text(strip=True)
                if service_text and service_text not in services:
                    services.append(service_text)
        
        return services

    def _extract_location_from_soup(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract provider location"""
        # Look for location information
        location_text = soup.find(string=re.compile(r'London|Birmingham|Manchester|Leeds|Glasgow'))
        if location_text:
            return location_text.strip()
            
        selectors = ['.location', '.address', '.seller-location']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None

    def _extract_rating_from_soup(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract provider rating"""
        # Look for rating display
        rating_elements = soup.find_all(string=re.compile(r'(\d+\.?\d*)/5'))
        for rating_text in rating_elements:
            match = re.search(r'(\d+\.?\d*)/5', rating_text)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    pass
        return None

    def _extract_reviews_count_from_soup(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract number of reviews"""
        # Look for review count patterns
        review_patterns = [
            re.compile(r'(\d+)\s+customer reviews'),
            re.compile(r'(\d+)\s+reviews'),
            re.compile(r'\((\d+)\)'),
        ]
        
        for pattern in review_patterns:
            for element in soup.find_all(string=pattern):
                match = pattern.search(element)
                if match:
                    try:
                        return int(match.group(1))
                    except ValueError:
                        pass
        return None

    def _extract_contact_info_from_soup(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract any publicly available contact information"""
        contact_info = {
            'phone': None,
            'email': None, 
            'website': None,
            'facebook': None
        }
        
        # Look for any contact information in text
        text_content = soup.get_text()
        
        # Phone number patterns
        phone_patterns = [
            r'(?:\+44|0)\s*\d{2,4}\s*\d{3,4}\s*\d{3,4}',
            r'(?:\+44|0)\d{10,11}',
            r'\(0\d{2,4}\)\s*\d{3,4}\s*\d{3,4}'
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text_content)
            if match:
                contact_info['phone'] = match.group(0).strip()
                break
        
        # Email pattern
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_content)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Website patterns
        website_match = re.search(r'(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?', text_content)
        if website_match:
            url = website_match.group(0)
            if not url.startswith('http'):
                url = 'http://' + url
            if 'bark.com' not in url:  # Exclude bark.com URLs
                contact_info['website'] = url
        
        return contact_info
    
    def _safe_extract_text(self, selector: str) -> Optional[str]:
        """Safely extract text from an element"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip() if element.text else None
        except NoSuchElementException:
            return None
    
    def _extract_services(self) -> List[str]:
        """Extract list of services offered"""
        services = []
        try:
            service_elements = self.driver.find_elements(By.CSS_SELECTOR, '[itemprop="knowsAbout"]')
            services = [elem.text.strip() for elem in service_elements if elem.text.strip()]
        except:
            pass
        return services
    
    def _extract_location(self) -> Optional[str]:
        """Extract provider location/address"""
        selectors = [
            '[itemprop="address"]',
            '.seller-location',
            '.location',
            '.address'
        ]
        
        for selector in selectors:
            location = self._safe_extract_text(selector)
            if location:
                return location
        return None
    
    def _extract_contact_info(self, contact_type: str) -> Optional[str]:
        """Extract contact information by type"""
        try:
            if contact_type == 'tel':
                element = self.driver.find_element(By.CSS_SELECTOR, f'a[data-thing="{contact_type}"], a[href^="tel:"]')
                href = element.get_attribute('href')
                return href.replace('tel:', '') if href else None
            
            elif contact_type == 'email':
                element = self.driver.find_element(By.CSS_SELECTOR, f'a[data-thing="{contact_type}"], a[href^="mailto:"]')
                href = element.get_attribute('href')
                return href.replace('mailto:', '') if href else None
            
            elif contact_type == 'website':
                element = self.driver.find_element(By.CSS_SELECTOR, f'a[data-thing="{contact_type}"]')
                return element.get_attribute('href')
            
            elif contact_type == 'facebook':
                element = self.driver.find_element(By.CSS_SELECTOR, f'a[data-thing="{contact_type}"], a[href*="facebook.com"]')
                return element.get_attribute('href')
                
        except NoSuchElementException:
            pass
        return None
    
    def _extract_rating(self) -> Optional[float]:
        """Extract provider rating"""
        try:
            # Look for star ratings
            rating_elements = self.driver.find_elements(By.CSS_SELECTOR, '.rating, [class*="star"], [class*="rating"]')
            for elem in rating_elements:
                text = elem.text.strip()
                if '/' in text:
                    return float(text.split('/')[0])
        except:
            pass
        return None
    
    def _extract_reviews_count(self) -> Optional[int]:
        """Extract number of reviews"""
        try:
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, '[class*="review"], [class*="feedback"]')
            for elem in review_elements:
                text = elem.text.strip()
                if 'review' in text.lower():
                    # Extract number from text
                    import re
                    numbers = re.findall(r'\d+', text)
                    if numbers:
                        return int(numbers[0])
        except:
            pass
        return None
    
    def scrape_service_category(self, service: str, location: str = None, max_providers: int = 100) -> List[Dict]:
        """
        Scrape all providers for a specific service category
        """
        provider_urls = self.get_service_providers_urls(service, location)
        
        if max_providers:
            provider_urls = provider_urls[:max_providers]
        
        scraped_data = []
        
        for i, url in enumerate(provider_urls, 1):
            print(f"Scraping provider {i}/{len(provider_urls)}: {url}")
            
            provider_data = self.scrape_provider_profile(url)
            if provider_data:
                scraped_data.append(provider_data)
            
            # Rate limiting
            time.sleep(random.uniform(3, 6))
            
            # Rotate user agent occasionally for session
            if i % 10 == 0:
                # Update session headers with new user agent
                new_ua = self.ua.random
                self.session.headers.update({'User-Agent': new_ua})
                print(f"🔄 Rotated user agent after {i} providers")
        
        return scraped_data
    
    def save_to_csv(self, data: List[Dict], filename: str = None):
        """Save scraped data to CSV file"""
        if not data:
            print("No data to save")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bark_providers_{timestamp}.csv"
        
        # Ensure the filename has .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Create DataFrame and save
        df = pd.DataFrame(data)
        
        # Flatten list columns for CSV
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
        print(f"Total records: {len(data)}")
    
    def filter_by_location(self, data: List[Dict], location: str) -> List[Dict]:
        """Filter providers by location"""
        location_lower = location.lower()
        filtered = []
        
        for provider in data:
            provider_location = provider.get('location', '').lower()
            if location_lower in provider_location:
                filtered.append(provider)
        
        return filtered
    
    def filter_by_service(self, data: List[Dict], service: str) -> List[Dict]:
        """Filter providers by service type"""
        service_lower = service.lower()
        filtered = []
        
        for provider in data:
            services = provider.get('services', [])
            if isinstance(services, str):
                services = [services]
            
            for provider_service in services:
                if service_lower in provider_service.lower():
                    filtered.append(provider)
                    break
        
        return filtered
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def main():
    """
    Main function demonstrating how to use the scraper
    """
    scraper = BarkScraper(headless=True)
    
    try:
        # Example: Scrape cleaners in London
        print("Starting Bark.com scraper...")
        print("Scraping cleaners in London...")
        
        cleaners_data = scraper.scrape_service_category(
            service='cleaners',
            location='london',
            max_providers=50  # Limit for demo
        )
        
        if cleaners_data:
            # Save to CSV
            scraper.save_to_csv(cleaners_data, 'bark_cleaners_london.csv')
            
            # Show some statistics
            print("\n=== SCRAPING RESULTS ===")
            print(f"Total providers found: {len(cleaners_data)}")
            
            providers_with_phone = len([p for p in cleaners_data if p.get('phone')])
            providers_with_email = len([p for p in cleaners_data if p.get('email')])
            providers_with_website = len([p for p in cleaners_data if p.get('website')])
            
            print(f"Providers with phone: {providers_with_phone}")
            print(f"Providers with email: {providers_with_email}")
            print(f"Providers with website: {providers_with_website}")
            
        else:
            print("No data scraped. Please check the service and location parameters.")
    
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
