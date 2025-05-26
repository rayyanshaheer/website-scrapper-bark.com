#!/usr/bin/env python3
"""
Advanced Bark.com Scraper CLI
A command-line interface for scraping contact information from Bark.com professionals
"""

import argparse
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bark_scraper import BarkScraper


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Bark.com Contact Information Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape cleaners in London (max 50 providers)
  python scraper_cli.py cleaners --location london --max 50

  # Scrape all web designers nationwide (max 100)
  python scraper_cli.py web-design --max 100

  # Scrape personal trainers in Manchester with custom output file
  python scraper_cli.py personal-trainer --location manchester --output trainers_manchester.csv

  # Scrape multiple services
  python scraper_cli.py cleaners gardeners builders --location birmingham --max 30

Available Services:
  Home & Garden: cleaners, gardeners, builders, electricians, plumbers, painters
  Health & Wellbeing: personal-trainer, therapy, massage, nutrition
  Business: web-design, accountants, marketing, photography
  Events: dj, photographer, catering, entertainment
  Lessons: music-lessons, tutoring, driving-lessons

Popular Locations:
  london, birmingham, manchester, liverpool, leeds, sheffield, bristol,
  glasgow, leicester, coventry, nottingham, newcastle, belfast, cardiff,
  edinburgh, brighton, plymouth, stoke-on-trent
        """
    )
    
    # Required service argument
    parser.add_argument(
        'services',
        nargs='+',
        help='Service type(s) to scrape (e.g., cleaners, web-design, personal-trainer)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--location', '-l',
        type=str,
        help='Location to filter by (e.g., london, manchester, birmingham)'
    )
    
    parser.add_argument(
        '--max', '-m',
        type=int,
        default=100,
        help='Maximum number of providers to scrape per service (default: 100)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output CSV filename (auto-generated if not specified)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    
    parser.add_argument(
        '--visible',
        action='store_true',
        help='Run browser in visible mode (for debugging)'
    )
    
    parser.add_argument(
        '--filter-phone',
        action='store_true',
        help='Only include providers with phone numbers'
    )
    
    parser.add_argument(
        '--filter-email',
        action='store_true',
        help='Only include providers with email addresses'
    )
    
    parser.add_argument(
        '--filter-website',
        action='store_true',
        help='Only include providers with websites'
    )
    
    return parser


def validate_services(services):
    """Validate service names"""
    valid_services = {
        # Home & Garden
        'cleaners', 'gardeners', 'builders', 'electricians', 'plumbers', 'painters',
        'decorators', 'roofers', 'flooring', 'kitchen-fitting', 'bathroom-fitting',
        
        # Health & Wellbeing  
        'personal-trainer', 'personal-training', 'therapy', 'massage', 'nutrition',
        'counselling', 'physiotherapy', 'osteopathy', 'chiropractor',
        
        # Business Services
        'web-design', 'accountants', 'marketing', 'photography', 'graphic-design',
        'seo', 'social-media-marketing', 'bookkeeping', 'tax-services',
        
        # Events & Entertainment
        'dj', 'photographer', 'catering', 'entertainment', 'wedding-photography',
        'magician', 'band', 'singer', 'wedding-planner',
        
        # Lessons & Training
        'music-lessons', 'tutoring', 'driving-lessons', 'language-lessons',
        'fitness-training', 'dance-lessons', 'art-lessons'
    }
    
    invalid_services = []
    for service in services:
        if service not in valid_services:
            invalid_services.append(service)
    
    if invalid_services:
        print(f"Warning: Invalid service(s): {', '.join(invalid_services)}")
        print("Will attempt to scrape anyway, but results may be limited.")
        return False
    
    return True


def main():
    """Main CLI function"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not args.services:
        parser.error("At least one service type is required")
    
    # Validate services
    validate_services(args.services)
    
    # Set headless mode
    headless = args.headless and not args.visible
    
    # Initialize scraper
    scraper = BarkScraper(headless=headless)
    
    try:
        all_data = []
        
        for service in args.services:
            print(f"\n{'='*50}")
            print(f"Scraping {service.upper()}")
            print(f"{'='*50}")
            
            if args.location:
                print(f"Location: {args.location.title()}")
            print(f"Max providers: {args.max}")
            
            # Scrape the service
            service_data = scraper.scrape_service_category(
                service=service,
                location=args.location,
                max_providers=args.max
            )
            
            if service_data:
                # Add service type to each record
                for record in service_data:
                    record['service_category'] = service
                
                all_data.extend(service_data)
                print(f"Scraped {len(service_data)} providers for {service}")
            else:
                print(f"No providers found for {service}")
        
        if not all_data:
            print("\nNo data was scraped. Please check your service and location parameters.")
            return
        
        # Apply filters
        if args.filter_phone:
            all_data = [p for p in all_data if p.get('phone')]
            print(f"Filtered to {len(all_data)} providers with phone numbers")
        
        if args.filter_email:
            all_data = [p for p in all_data if p.get('email')]
            print(f"Filtered to {len(all_data)} providers with email addresses")
        
        if args.filter_website:
            all_data = [p for p in all_data if p.get('website')]
            print(f"Filtered to {len(all_data)} providers with websites")
        
        # Save results
        output_filename = args.output
        if not output_filename:
            location_suffix = f"_{args.location}" if args.location else ""
            services_suffix = "_".join(args.services[:2])  # Use first 2 services for filename
            output_filename = f"bark_{services_suffix}{location_suffix}.csv"
        
        scraper.save_to_csv(all_data, output_filename)
        
        # Print summary
        print(f"\n{'='*50}")
        print("SCRAPING COMPLETE")
        print(f"{'='*50}")
        print(f"Total providers scraped: {len(all_data)}")
        print(f"Services: {', '.join(args.services)}")
        if args.location:
            print(f"Location: {args.location.title()}")
        print(f"Output file: {output_filename}")
        
        # Contact info summary
        phone_count = len([p for p in all_data if p.get('phone')])
        email_count = len([p for p in all_data if p.get('email')])
        website_count = len([p for p in all_data if p.get('website')])
        
        print(f"\nContact Information Summary:")
        print(f"- Providers with phone: {phone_count} ({phone_count/len(all_data)*100:.1f}%)")
        print(f"- Providers with email: {email_count} ({email_count/len(all_data)*100:.1f}%)")
        print(f"- Providers with website: {website_count} ({website_count/len(all_data)*100:.1f}%)")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nError during scraping: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
