"""
Bark.com Contact Information Scraper

A professional web scraper for extracting service provider contact information
from Bark.com with filtering capabilities by location and service type.

Author: rayyanshaheer
Version: 2.0.0
License: MIT
"""

__version__ = "2.0.0"
__author__ = "rayyanshaheer"
__license__ = "MIT"

from .bark_scraper import BarkScraper
from .config import ScrapingConfig

__all__ = ["BarkScraper", "ScrapingConfig"]
