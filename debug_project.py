import os
import sys
from pathlib import Path
from django.conf import settings
from django.urls import reverse
import django
import logging

# Configure logging
logging.basicConfig(
    filename='debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up Django environment
def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    try:
        django.setup()
        logger.info("Django setup completed successfully")
    except Exception as e:
        logger.error(f"Failed to setup Django: {e}")
        print(f"Failed to setup Django: {e}")
        sys.exit(1)

# Check settings.py configuration
def check_settings():
    logger.info("Checking settings.py...")
    print("Checking settings.py...")
    issues = []
    
    # Check INSTALLED_APPS
    required_apps = ['django.contrib.staticfiles', 'django_bootstrap5', 'core']
    for app in required_apps:
        if app not in settings.INSTALLED_APPS:
            issues.append(f"Missing {app} in INSTALLED_APPS")
    
    # Check static settings
    if not hasattr(settings, 'STATIC_URL') or settings.STATIC_URL != '/static/':
        issues.append("STATIC_URL not set to '/static/'")
    if not hasattr(settings, 'STATIC_ROOT') or not os.path.exists(settings.STATIC_ROOT):
        issues.append(f"STATIC_ROOT ({settings.STATIC_ROOT}) not found")
    
    # Check template settings
    templates = settings.TEMPLATES
    if not templates or not templates[0].get('APP_DIRS', False):
        issues.append("TEMPLATES setting missing or APP_DIRS not enabled")
    
    # Check session settings
    if not hasattr(settings, 'SESSION_ENGINE') or settings.SESSION_ENGINE != 'django.contrib.sessions.backends.db':
        issues.append("SESSION_ENGINE not set to 'django.contrib.sessions.backends.db'")
    
    return issues

# Check template files for load tags
def check_templates():
    logger.info("Checking template files...")
    print("Checking template files...")
    issues = []
    template_dir = Path('core/templates')
    for template_file in template_dir.rglob('*.html'):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                load_static = False
                load_bootstrap = False
                
                for i, line in enumerate(lines, 1):
                    line = line.strip()
                    if '{% load static %}' in line:
                        load_static = True
                    if '{% load django_bootstrap5 %}' in line:
                        load_bootstrap = True
                    if '{% static ' in line and not load_static:
                        issues.append(f"{template_file}: Uses 'static' tag on line {i} but '{{% load static %}}' not found earlier")
                    if ('{% bootstrap_css %}' in line or '{% bootstrap_javascript %}' in line) and not load_bootstrap:
                        issues.append(f"{template_file}: Uses bootstrap tags on line {i} but '{{% load django_bootstrap5 %}}' not found earlier")
        except Exception as e:
            issues.append(f"Error reading {template_file}: {e}")
    
    return issues

# Check static files
def check_static_files():
    logger.info("Checking static files...")
    print("Checking static files...")
    issues = []
    static_files = [
        'favicon.ico',
        'css/custom.css'
    ]
    for file in static_files:
        path = Path('core/static') / file
        if not path.exists():
            issues.append(f"Static file {path} not found")
    
    return issues

# Check URL routing
def check_urls():
    logger.info("Checking URLs...")
    print("Checking URLs...")
    issues = []
    try:
        reverse('home')
        reverse('shop')
        reverse('cart_add', args=[1])  # Updated to match core/urls.py
        reverse('cart_remove', args=[1])  # Added to check cart_remove
        reverse('cart')
        reverse('login')
    except Exception as e:
        issues.append(f"URL routing error: {e}")
    return issues

# Main debug function
def debug_project():
    setup_django()
    all_issues = []
    
    all_issues.extend(check_settings())
    all_issues.extend(check_templates())
    all_issues.extend(check_static_files())
    all_issues.extend(check_urls())
    
    if all_issues:
        logger.warning("Issues found:")
        print("\nIssues found:")
        for issue in all_issues:
            logger.warning(f"- {issue}")
            print(f"- {issue}")
    else:
        logger.info("No issues found. Project configuration looks good!")
        print("\nNo issues found. Project configuration looks good!")
    
    return len(all_issues) == 0

if __name__ == "__main__":
    try:
        debug_project()
    except Exception as e:
        logger.error(f"Debug failed: {e}")
        print(f"Debug failed: {e}")
        sys.exit(1)