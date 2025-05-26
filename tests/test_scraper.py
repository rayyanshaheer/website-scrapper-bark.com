#!/usr/bin/env python3
"""
Test script for Bark scraper
"""

import requests
from bs4 import BeautifulSoup
import cloudscraper
import re
import json
from datetime import datetime

def test_basic_connection():
    """Test basic connection to Bark.com"""
    print("=== Testing Basic Connection ===")
    
    try:
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        url = 'https://www.bark.com/en/gb/cleaners/london/'
        print(f"Fetching: {url}")
        
        response = scraper.get(url, timeout=15)
        print(f"Status code: {response.status_code}")
        print(f"Content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✓ Successfully connected to Bark.com")
            return response.content
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None

def test_provider_url_extraction(content):
    """Test extraction of provider URLs"""
    print("\n=== Testing Provider URL Extraction ===")
    
    if not content:
        print("No content to parse")
        return []
    
    soup = BeautifulSoup(content, 'html.parser')
    provider_urls = []
    
    # Look for company profile links
    all_links = soup.find_all('a', href=True)
    
    for link in all_links:
        href = link.get('href', '')
        # Match pattern: /en/gb/company/name/id/
        if re.match(r'^/en/gb/company/[^/]+/[A-Za-z0-9]+/?$', href):
            full_url = 'https://www.bark.com' + href
            if full_url not in provider_urls:
                provider_urls.append(full_url)
    
    print(f"Found {len(provider_urls)} provider URLs")
    for i, url in enumerate(provider_urls[:5]):
        print(f"{i+1}. {url}")
    
    return provider_urls

def test_profile_scraping(url):
    """Test scraping of individual provider profile"""
    print(f"\n=== Testing Profile Scraping ===")
    print(f"Scraping: {url}")
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=15)
        
        if response.status_code != 200:
            print(f"✗ Failed to fetch profile: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic information
        profile_data = {
            'url': url,
            'scraped_at': datetime.now().isoformat()
        }
        
        # Try to extract name
        name_selectors = ['h1', '.company-name', '[data-testid="company-name"]']
        for selector in name_selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                profile_data['name'] = element.get_text(strip=True)
                break
        
        # Try to extract description
        about_section = soup.find('h4', string='About')
        if about_section:
            next_elem = about_section.find_next_sibling()
            if next_elem:
                text = next_elem.get_text(strip=True)
                if text:
                    profile_data['description'] = text
        
        # Look for contact patterns in page text
        text_content = soup.get_text()
        
        # Phone pattern
        phone_match = re.search(r'(?:\+44|0)\s*\d{2,4}\s*\d{3,4}\s*\d{3,4}', text_content)
        if phone_match:
            profile_data['phone'] = phone_match.group(0).strip()
        
        # Email pattern
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_content)
        if email_match:
            profile_data['email'] = email_match.group(0)
        
        print("✓ Profile scraped successfully")
        print("Extracted data:")
        for key, value in profile_data.items():
            if value:
                display_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                print(f"  {key}: {display_value}")
        
        return profile_data
        
    except Exception as e:
        print(f"✗ Profile scraping failed: {e}")
        return None

def main():
    print("Bark.com Scraper Test")
    print("=" * 50)
    
    # Test basic connection
    content = test_basic_connection()
    
    if content:
        # Test URL extraction
        urls = test_provider_url_extraction(content)
        
        if urls:
            # Test profile scraping on first URL
            profile_data = test_profile_scraping(urls[0])
            
            if profile_data:
                print("\n=== Test Summary ===")
                print("✓ All tests passed!")
                print("✓ Connection working")
                print("✓ URL extraction working")
                print("✓ Profile scraping working")
            else:
                print("\n=== Test Summary ===")
                print("✗ Profile scraping failed")
        else:
            print("\n=== Test Summary ===")
            print("✗ URL extraction failed")
    else:
        print("\n=== Test Summary ===")
        print("✗ Basic connection failed")

if __name__ == "__main__":
    main()
