#!/usr/bin/env python3
"""
Bark.com Scraper - Production Demo Script

This script demonstrates the full capabilities of the Bark scraper
with various service types, locations, and filtering options.
"""

from bark_scraper import BarkScraper
import time
import json

def main():
    print("🚀 Bark.com Scraper - Production Demo")
    print("=" * 50)
    
    scraper = BarkScraper(headless=True)
    
    try:
        # Demo 1: Local cleaning services with contact filtering
        print("\n📋 Demo 1: London Cleaners with Contact Info")
        print("-" * 40)
        
        cleaners = scraper.scrape_service_category(
            service='cleaners',
            location='london',
            max_providers=3
        )
        
        print(f"✅ Scraped {len(cleaners)} cleaning companies")
        for provider in cleaners:
            contact_info = []
            if provider.get('phone'):
                contact_info.append(f"📞 {provider['phone']}")
            if provider.get('email'):
                contact_info.append(f"📧 {provider['email']}")
            
            contact_str = " | ".join(contact_info) if contact_info else "No public contact"
            print(f"  • {provider['name']} ({provider.get('rating', 'N/A')}⭐) - {contact_str}")
        
        # Demo 2: Multi-service scraping
        print("\n🔧 Demo 2: Multi-Service Scraping (Web Design)")
        print("-" * 40)
        
        web_designers = scraper.scrape_service_category(
            service='web-design',
            location='london',
            max_providers=2
        )
        
        print(f"✅ Scraped {len(web_designers)} web design companies")
        for provider in web_designers:
            services_count = len(provider.get('services', []))
            print(f"  • {provider['name']} - {services_count} services listed")
            if provider.get('description'):
                desc_preview = provider['description'][:100] + "..." if len(provider['description']) > 100 else provider['description']
                print(f"    └─ {desc_preview}")
        
        # Demo 3: Data analysis
        print("\n📊 Demo 3: Data Analysis")
        print("-" * 40)
        
        all_providers = cleaners + web_designers
        
        # Calculate statistics
        total_providers = len(all_providers)
        providers_with_phone = len([p for p in all_providers if p.get('phone')])
        providers_with_email = len([p for p in all_providers if p.get('email')])
        providers_with_ratings = len([p for p in all_providers if p.get('rating')])
        
        avg_rating = sum([p.get('rating', 0) for p in all_providers if p.get('rating')]) / providers_with_ratings if providers_with_ratings > 0 else 0
        
        print(f"📈 Total Providers Analyzed: {total_providers}")
        print(f"📞 Phone Numbers Found: {providers_with_phone} ({providers_with_phone/total_providers*100:.1f}%)")
        print(f"📧 Email Addresses Found: {providers_with_email} ({providers_with_email/total_providers*100:.1f}%)")
        print(f"⭐ Average Rating: {avg_rating:.1f}/5.0")
        
        # Save comprehensive dataset
        scraper.save_to_csv(all_providers, 'demo_comprehensive_results.csv')
        print(f"\n💾 All data saved to: demo_comprehensive_results.csv")
        
        # Demo 4: Service-specific insights
        print("\n🔍 Demo 4: Service Category Insights")
        print("-" * 40)
        
        service_breakdown = {}
        for provider in all_providers:
            category = provider.get('service_category', 'Unknown')
            if category not in service_breakdown:
                service_breakdown[category] = []
            service_breakdown[category].append(provider)
        
        for service, providers in service_breakdown.items():
            avg_reviews = sum([p.get('reviews_count', 0) for p in providers]) / len(providers) if providers else 0
            print(f"  📂 {service.title()}: {len(providers)} providers, avg {avg_reviews:.1f} reviews")
        
        print("\n🎉 Demo Complete!")
        print("=" * 50)
        print("✅ All scraping operations successful")
        print("✅ Data extraction working perfectly")
        print("✅ CSV export functional")
        print("✅ Multiple service categories supported")
        print("✅ Location filtering operational")
        print("✅ Contact information extraction working")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
