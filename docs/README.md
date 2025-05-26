# Bark.com Contact Information Scraper

**✅ LIVE & WORKING** - Successfully tested on May 26, 2025

**⚠️ IMPORTANT LEGAL NOTICE**: This tool is for educational and research purposes only. Users must comply with Bark.com's terms of service, robots.txt, and applicable laws regarding web scraping. Always obtain proper authorization before scraping any website.

A powerful, production-ready web scraper for extracting contact information from Bark.com service providers. Built with modern Python technologies and anti-detection capabilities.

## 📊 Test Results (May 26, 2025)

```
✅ VERIFIED WORKING
Test: London Cleaners (5 providers)
• 5/5 profiles successfully scraped
• 100% provider names extracted
• 100% descriptions extracted  
• 100% service lists extracted
• 100% ratings extracted
• 20% phone numbers found
• 20% email addresses found
• CSV export successful

Sample Provider Data:
• Spotless Horizon Cleaning Ltd (5.0★, 11 reviews)
• NeatNest Cleaners (5.0★, 31 reviews) + Contact Info
• Danny's Cleaning Services (5.0★, 7 reviews)
```

## Features

- **Multi-Service Scraping**: Extract data from any service category on Bark.com
- **Location Filtering**: Filter providers by UK cities and regions
- **Contact Information**: Extract phone numbers, emails, websites, and social media
- **Anti-Detection**: Uses undetected Chrome and rotating user agents
- **CSV Export**: Automatic CSV generation with filtering options
- **CLI Interface**: Easy-to-use command-line interface
- **Rate Limiting**: Respectful scraping with built-in delays
- **Error Handling**: Robust error handling and retry mechanisms

## Installation

1. Clone or download this repository:
```bash
cd website-scrapper-bark.com
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. The scraper will automatically download and manage Chrome drivers.

## Quick Start

### Basic Usage

Scrape cleaners in London:
```bash
python scraper_cli.py cleaners --location london --max 50
```

Scrape web designers nationwide:
```bash
python scraper_cli.py web-design --max 100
```

### Advanced Usage

Scrape multiple services with filters:
```bash
python scraper_cli.py cleaners gardeners --location birmingham --max 30 --filter-phone
```

Custom output file:
```bash
python scraper_cli.py personal-trainer --location manchester --output trainers_manchester.csv
```

## Available Services

### Home & Garden
- cleaners, gardeners, builders, electricians, plumbers, painters, decorators, roofers

### Health & Wellbeing  
- personal-trainer, therapy, massage, nutrition, counselling, physiotherapy

### Business Services
- web-design, accountants, marketing, photography, graphic-design, seo

### Events & Entertainment
- dj, photographer, catering, entertainment, wedding-photography, magician

### Lessons & Training
- music-lessons, tutoring, driving-lessons, language-lessons, fitness-training

## Popular Locations

london, birmingham, manchester, liverpool, leeds, sheffield, bristol, glasgow, leicester, coventry, nottingham, newcastle, belfast, cardiff, edinburgh, brighton, plymouth

## Command Line Options

```
python scraper_cli.py [services] [options]

Positional Arguments:
  services              Service type(s) to scrape (e.g., cleaners, web-design)

Options:
  --location, -l       Location to filter by (e.g., london, manchester)
  --max, -m           Maximum providers per service (default: 100)
  --output, -o        Output CSV filename (auto-generated if not specified)
  --visible           Run browser in visible mode (for debugging)
  --filter-phone      Only include providers with phone numbers
  --filter-email      Only include providers with email addresses
  --filter-website    Only include providers with websites
```

## Output Format

The scraper generates CSV files with the following columns:

- **name**: Provider/company name
- **description**: Business description
- **services**: List of services offered
- **location**: Address/location
- **phone**: Phone number
- **email**: Email address
- **website**: Website URL
- **facebook**: Facebook profile URL
- **rating**: Customer rating (if available)
- **reviews_count**: Number of reviews
- **service_category**: Scraped service type
- **url**: Original Bark.com profile URL
- **scraped_at**: Timestamp of when data was collected

## Examples

### Example 1: Local Cleaning Services
```bash
python scraper_cli.py cleaners --location london --max 25 --filter-phone
```
Output: Cleaning companies in London with phone numbers

### Example 2: Web Design Agencies
```bash
python scraper_cli.py web-design --max 50 --filter-website --output web_designers.csv
```
Output: Web design agencies with websites

### Example 3: Health & Fitness Professionals
```bash
python scraper_cli.py personal-trainer massage therapy --location manchester --max 20
```
Output: Health and fitness professionals in Manchester

## Programmatic Usage

You can also use the scraper in your Python code:

```python
from bark_scraper import BarkScraper

# Initialize scraper
scraper = BarkScraper(headless=True)

# Scrape cleaners in London
data = scraper.scrape_service_category(
    service='cleaners',
    location='london',
    max_providers=50
)

# Save to CSV
scraper.save_to_csv(data, 'cleaners_london.csv')

# Filter data
phone_providers = scraper.filter_by_location(data, 'central london')

# Clean up
scraper.close()
```

## Configuration

You can modify scraping behavior by editing `config.py`:

- Rate limiting delays
- CSS selectors for data extraction
- User agent rotation
- Validation rules

## Ethical Usage

This scraper is designed for legitimate business research and lead generation. Please use responsibly:

- Respect Bark.com's terms of service
- Don't overload their servers with requests
- Use scraped data ethically and in compliance with GDPR
- Consider contacting providers through Bark.com's platform when possible

## Troubleshooting

### Common Issues

1. **No data scraped**: Check if the service name and location are correct
2. **Browser crashes**: Try running with `--visible` flag to debug
3. **Slow performance**: Reduce `--max` parameter or check internet connection
4. **Missing contact info**: Some providers may not have public contact details

### Dependencies

- Python 3.8+
- Chrome browser (automatically managed)
- Stable internet connection

## Technical Features

- **Undetected Chrome**: Bypasses most anti-bot detection
- **Cloudscraper**: Handles Cloudflare protection
- **Smart Selectors**: Multiple fallback selectors for reliable data extraction
- **Rate Limiting**: Configurable delays between requests
- **User Agent Rotation**: Randomized browser signatures
- **Error Recovery**: Automatic retries on failures

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the command-line help: `python scraper_cli.py --help`
3. Examine the configuration in `config.py`

## License

This tool is for educational and research purposes. Users are responsible for complying with applicable laws and website terms of service.
