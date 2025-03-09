import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_fire_code_rules(index_url):
    """
    Scrapes MN Revisor fire code rules from the index page - Corrected index page logic.
    """
    markdown_document = ""
    base_url = "https://www.revisor.mn.gov"

    try:
        # --- Fetch and Parse Index Page (using requests) ---
        response = requests.get(index_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Extract Rule Links (Corrected Logic) ---
        rule_links = []
        for a_tag in soup.find_all('a', href=True):  # Find ALL 'a' tags with href
            match = re.search(r'Minn\.\s+Rules\s+(\d+\.\d+)', a_tag.get_text())  # Correct regex
            if match:
                rule_number = match.group(1)
                rule_url = urljoin(base_url, f"/rules/{rule_number}/") # Construct URL
                rule_links.append(rule_url)
                print(f"Found rule link: {rule_url}")

        if not rule_links:
            return "# Error: No rule links found on index page.\n"

        # --- Set up Selenium (for individual rule pages) ---
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("window-size=1920,1080")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception as e:
            return f"# Error: Could not initialize ChromeDriver: {e}\n"

        # --- Scrape Each Rule Page (using Selenium) ---
        for rule_url in rule_links:
            markdown_document += scrape_rule_page(driver, rule_url, base_url)
            time.sleep(1)

    except requests.exceptions.RequestException as e:
        return f"Error fetching index page: {e}\n"
    finally:
        if 'driver' in locals():
            driver.quit()

    return markdown_document

def scrape_rule_page(driver, rule_url, base_url):
    """Scrapes a single rule page (now combined with chapter)."""
    rule_content = ""
    print(f"--- Scraping rule: {rule_url} ---")

    try:
        driver.get(rule_url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # --- Flexible Title Extraction ---
        rule_number = rule_url.split('/')[-2]  # Get rule number from URL
        title_tag = None
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if rule_number in tag.get_text():
                title_tag = tag
                break

        if title_tag:
            rule_title = title_tag.get_text().strip()
            rule_content += f"\n## {rule_title}\n\n"
            print(f"  Found rule title: {rule_title}")
        else:
            print(f"  No rule title found for {rule_number}. Using URL segment as title.")
            rule_title = rule_number  # Fallback title
            rule_content += f"\n## {rule_title}\n\n"

        rule_content += f"**Source:** {rule_url}\n\n"

        # --- Flexible Rule Content Extraction ---
        for section_div in soup.find_all('div', class_='section'):
            section_id = section_div.get('id', '')
            match = re.match(r'(\d+\.\d+)', section_id)
            if match:
                rule_number = match.group(1)
                # Find the link within this section, if it exists
                rule_link = section_div.find('a', href=True)
                if rule_link:
                    rule_url = urljoin(base_url, rule_link['href'])
                else:
                    # If no explicit link, use the section ID to construct URL
                    rule_url = urljoin(base_url, f"/rules/{rule_number}")
                print(f"    Found rule: {rule_number} - {rule_url}")
                rule_content += f"### {rule_number}\n\n"
                # Extract content directly from the section div
                rule_content += f"{section_div.get_text().strip()}\n\n"
                time.sleep(1)

    except Exception as e:
        print(f"    Error scraping rule {rule_url}: {e}")
        return f"Error scraping rule {rule_url}: {e}\n"

    return rule_content

# --- Main Execution ---
if __name__ == "__main__":
    index_url = "https://www.revisor.mn.gov/index/rule/topic/fire_code?year=null"  # Use the original index URL
    document = scrape_fire_code_rules(index_url)
    print(document)

    with open("mn_fire_code_rules.md", "w", encoding="utf-8") as f:
        f.write(document)