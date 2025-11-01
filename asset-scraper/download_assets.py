import os
import re
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# 1. SET THE PATH TO YOUR HTML FILE
HTML_FILE_PATH = '' # e.g., 'main.html'

# 2. SET THE BASE URL OF THE CDN
CDN_BASE_URL = '' # e.g., 'https://cdn.prod.website-files.com/'

# 3. SET THE FILE TYPES TO DOWNLOAD
ASSET_TYPES = ('.png', '.avif', '.css', '.webp', '.svg', '.js', '.json')

# 4. SET THE FOLDER TO SAVE ASSETS
OUTPUT_DIR = 'downloaded_assets_test'

# 5. SET HOW MANY FILES TO DOWNLOAD AT ONCE
MAX_WORKERS = 10

# Regex to find urls() in inline styles
# e.g., style="background-image: url('.../image.png')"
STYLE_URL_REGEX = re.compile(r'url\([\'"]?(.*?)[\'"]?\)')

def find_assets_in_html(html_content):
    """Parses the HTML and finds all relevant asset URLs."""
    print("Parsing HTML to find assets...")
    soup = BeautifulSoup(html_content, 'lxml')
    found_urls = set()

    # 1. Find assets in standard tags (img, link, source, script)
    #    We check 'src', 'href', and 'srcset' attributes
    tags_to_check = {
        'img': ['src', 'srcset'],
        'link': ['href'],
        'source': ['src', 'srcset'],
        'script': ['src'], 
    }

    for tag_name, attrs in tags_to_check.items():
        for tag in soup.find_all(tag_name):
            for attr in attrs:
                if tag.has_attr(attr):
                    url_string = tag[attr]
                    
                    # 'srcset' can contain multiple URLs, comma-separated
                    if attr == 'srcset':
                        # 'image.png 1x, image-2x.png 2x' -> ['image.png', 'image-2x.png']
                        urls = [u.strip().split()[0] for u in url_string.split(',')]
                        found_urls.update(urls)
                    else:
                        found_urls.add(url_string)
                        
    # 2. Find assets in 'data-src' attributes (for Lottie animations), basically json
    for tag in soup.find_all(attrs={'data-src': True}):
        if tag.has_attr('data-src'):
            url = tag['data-src']
            found_urls.add(url)

    # 3. Find assets in inline 'style' attributes
    for tag in soup.find_all(style=True):
        style_string = tag['style']
        matches = STYLE_URL_REGEX.findall(style_string)
        for url in matches:
            found_urls.add(url)

    # 4. Filter the found URLs
    filtered_assets = set()
    for url in found_urls:
        if url and url.startswith(CDN_BASE_URL) and url.endswith(ASSET_TYPES):
            filtered_assets.add(url)
            
    return list(filtered_assets)

def download_asset(url):
    """Downloads a single asset from a URL and saves it."""
    try:
        # Get filename from URL (e.g., 'https://.../image.png' -> 'image.png')
        path = urlparse(url).path
        filename = os.path.basename(path)
        
        # Handle query parameters (e.g., image.png?v=123)
        if '?' in filename:
            filename = filename.split('?')[0]

        save_path = os.path.join(OUTPUT_DIR, filename)

        # Skip if file already exists
        if os.path.exists(save_path):
            return f"[SKIPPED] Already exists: {filename}"

        # Download the file
        response = requests.get(url, timeout=20)
        response.raise_for_status()  # Raise an error for bad responses (404, 500)

        # Save the file
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return f"[SUCCESS] Downloaded: {filename}"

    except requests.exceptions.RequestException as e:
        return f"[FAIL] Could not download {url}: {e}"
    except Exception as e:
        return f"[ERROR] Failed processing {url}: {e}"

def main():
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read the HTML file
    try:
        with open(HTML_FILE_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: HTML file not found at '{HTML_FILE_PATH}'")
        print("Please check the 'HTML_FILE_PATH' variable in the script.")
        return
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return

    # Find all assets
    assets_to_download = find_assets_in_html(html_content)

    if not assets_to_download:
        print("No assets found matching the criteria.")
        return

    print(f"\nFound {len(assets_to_download)} unique assets to download.")
    print(f"Downloading to '{OUTPUT_DIR}' using up to {MAX_WORKERS} workers...\n")

    # Use ThreadPoolExecutor to download files concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks
        future_to_url = {executor.submit(download_asset, url): url for url in assets_to_download}
        
        # Print results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            print(result)

    print("\n--- Download process complete. ---")

if __name__ == "__main__":
    main()