# Contributing to Bark.com Contact Information Scraper

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the codebase.

## Development Environment Setup

1. Clone the repository
2. Run the setup script: `bash setup.sh`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install development dependencies: `pip install pytest black flake8`

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and modular
- Use type hints where appropriate

## Testing

- Write tests for new features in the `tests/` directory
- Run tests before submitting: `python -m pytest tests/`
- Ensure all existing tests pass
- Add integration tests for scraping functionality

## Submitting Changes

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes with clear, descriptive commit messages
3. Update documentation if needed
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request with a clear description

## Reporting Issues

When reporting bugs or issues:
- Include Python version and operating system
- Provide steps to reproduce the issue
- Include relevant error messages and logs
- Specify which service categories and locations were being scraped

## Feature Requests

- Check existing issues first to avoid duplicates
- Clearly describe the proposed feature and its benefits
- Provide examples of how the feature would be used

## Code of Conduct

- Be respectful and constructive in all interactions
- Focus on the technical aspects of contributions
- Help maintain a welcoming environment for all contributors

## Legal Considerations

- Ensure all contributions comply with applicable laws
- Respect website terms of service and robots.txt
- Use scraping responsibly with appropriate delays
- Do not contribute code that violates copyright or privacy laws
