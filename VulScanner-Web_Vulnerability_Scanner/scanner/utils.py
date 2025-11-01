from urllib.parse import urljoin, urlparse

def validate_url(url):
    """Ensure URL starts with http:// or https:// and is valid"""
    if not url.startswith(('http://', 'https://')):
        return False
    
    try:
        parsed = urlparse(url)
        # Check if hostname exists
        if not parsed.netloc:
            return False
        return True
    except:
        return False

def is_localhost(url):
    """Check if URL is pointing to localhost"""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.netloc.split(':')[0]
        localhost_names = ['localhost', '127.0.0.1', '::1', '0.0.0.0']
        return hostname.lower() in localhost_names
    except:
        return False

def extract_forms(html, base_url):
    """Parse HTML and return list of form dicts"""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    forms = []
    for form in soup.find_all('form'):
        action = form.get('action') or base_url
        method = form.get('method', 'GET').upper()
        inputs = []
        for tag in form.find_all(['input', 'textarea']):
            name = tag.get('name')
            if name:
                inputs.append(name)
        forms.append({
            'action': urljoin(base_url, action),
            'method': method,
            'inputs': inputs
        })
    return forms