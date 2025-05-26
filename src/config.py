"""
Configuration file for Bark.com scraper
"""

# Rate limiting settings
MIN_DELAY = 2  # Minimum delay between requests (seconds)
MAX_DELAY = 5  # Maximum delay between requests (seconds)
PAGE_LOAD_TIMEOUT = 30  # Maximum time to wait for page load (seconds)

# Browser settings
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
]

# Bark.com specific settings
BASE_URL = "https://www.bark.com/en/gb/"
MAX_RETRIES = 3
RETRY_DELAY = 5

# CSV output settings
CSV_ENCODING = 'utf-8'
CSV_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Service categories available on Bark.com
SERVICE_CATEGORIES = {
    'home_garden': [
        'cleaners', 'gardeners', 'builders', 'electricians', 'plumbers', 
        'painters', 'decorators', 'roofers', 'flooring', 'kitchen-fitting',
        'bathroom-fitting', 'handyman', 'locksmith', 'pest-control'
    ],
    'health_wellbeing': [
        'personal-trainer', 'personal-training', 'therapy', 'massage', 
        'nutrition', 'counselling', 'physiotherapy', 'osteopathy', 
        'chiropractor', 'acupuncture', 'hypnotherapy'
    ],
    'business_services': [
        'web-design', 'accountants', 'marketing', 'photography', 
        'graphic-design', 'seo', 'social-media-marketing', 'bookkeeping',
        'tax-services', 'business-consulting', 'copywriting'
    ],
    'events_entertainment': [
        'dj', 'photographer', 'catering', 'entertainment', 'wedding-photography',
        'magician', 'band', 'singer', 'wedding-planner', 'party-planner',
        'venue-hire'
    ],
    'lessons_training': [
        'music-lessons', 'tutoring', 'driving-lessons', 'language-lessons',
        'fitness-training', 'dance-lessons', 'art-lessons', 'cooking-lessons',
        'computer-lessons'
    ]
}

# UK cities and regions for location filtering
UK_LOCATIONS = [
    'london', 'birmingham', 'manchester', 'liverpool', 'leeds', 'sheffield',
    'bristol', 'glasgow', 'leicester', 'coventry', 'nottingham', 'newcastle',
    'belfast', 'cardiff', 'edinburgh', 'brighton', 'plymouth', 'stoke-on-trent',
    'wolverhampton', 'southampton', 'reading', 'derby', 'luton', 'preston',
    'aberdeen', 'newport', 'swansea', 'dundee', 'middlesbrough', 'milton-keynes',
    'sunderland', 'norwich', 'portsmouth', 'york', 'peterborough', 'stockport',
    'rotherham', 'cambridge', 'watford', 'ipswich', 'slough', 'exeter',
    'gloucester', 'lincoln', 'chester', 'carlisle', 'worcester', 'bath'
]

# CSS selectors for data extraction
SELECTORS = {
    'provider_name': ['[itemprop="name"]', 'h1', '.seller-name', '.provider-name'],
    'description': ['[itemprop="description"]', '.section-about p', '.about-text', '.description'],
    'services': ['[itemprop="knowsAbout"]', '.services', '.service-list'],
    'location': ['[itemprop="address"]', '.seller-location', '.location', '.address'],
    'phone': ['a[data-thing="tel"]', 'a[href^="tel:"]'],
    'email': ['a[data-thing="email"]', 'a[href^="mailto:"]'],
    'website': ['a[data-thing="website"]'],
    'facebook': ['a[data-thing="facebook"]', 'a[href*="facebook.com"]'],
    'rating': ['.rating', '[class*="star"]', '[class*="rating"]'],
    'reviews': ['[class*="review"]', '[class*="feedback"]']
}

# Data validation rules
VALIDATION_RULES = {
    'phone': {
        'min_length': 10,
        'max_length': 15,
        'patterns': [r'^\+?[\d\s\-\(\)]+$']
    },
    'email': {
        'patterns': [r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$']
    },
    'website': {
        'patterns': [r'^https?://']
    }
}
