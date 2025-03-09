# Minnesota Fire Code Web Scraper

This Python script scrapes the Minnesota Revisor's Office website to extract the current fire code rules and saves them to a single Markdown file (`mn_fire_code_rules.md`).

## Description

The script uses a combination of `requests` (for the index page) and `selenium` (with ChromeDriver, in headless mode) to handle the dynamic content of the Minnesota Revisor's Office website.  It's designed to be as robust as possible to changes in the website's structure.

The script works in two main stages:

1.  **Index Page Scraping:** It fetches the main fire code index page (`https://www.revisor.mn.gov/index/rule/topic/fire_code?year=null`) and extracts the links to individual rule pages.  The script identifies these links by looking for `<a>` tags whose text matches the pattern "Minn. Rules ####.####".
2.  **Rule Page Scraping:**  For each extracted rule link, it uses Selenium to load the page, extract the rule title and content, and append it to the output Markdown string.  The rule content is extracted from `<div class="section">` tags.

The final output is both printed to the console and saved to `mn_fire_code_rules.md`.

## Prerequisites

*   **Python 3:**  Make sure you have Python 3 installed (preferably Python 3.7 or later). You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
*   **Chrome Browser:** Selenium requires the Chrome browser to be installed.
*   **pip:**  The Python package installer.  This usually comes bundled with Python.

## Installation

1.  **Clone the Repository (or Download):**

    *   **Using Git (Recommended):**
        ```bash
        git clone <your-github-repository-url>
        cd <your-repository-name>
        ```
        Replace `<your-github-repository-url>` and `<your-repository-name>` with the actual URL and name of your GitHub repository.

    *   **Downloading as a ZIP:**
        If you don't use Git, you can download the project as a ZIP file from GitHub (click the green "Code" button, then "Download ZIP").  Extract the ZIP file to a folder.

2.  **Install Dependencies:**
    Open a terminal or command prompt in the project directory (where `requirements.txt` is located) and run:

    ```bash
    pip install -r requirements.txt
    ```
   Or if you're on some Linux distributions or macOS, use `pip3`:
    ```bash
    pip3 install -r requirements.txt
    ```
    This will install the necessary Python libraries: `requests`, `beautifulsoup4`, `selenium`, and `webdriver-manager`.  `webdriver-manager` automatically handles downloading and managing ChromeDriver.

## Usage

1.  **Run the Script:**

    ```bash
    python scrape_mn_fire_code.py
    ```

    The script will print progress messages to the console as it scrapes the website.  The final output (the Markdown content) will also be printed to the console.

2.  **Find the Output:**

    The scraped content will be saved in a file named `mn_fire_code_rules.md` in the same directory as the script.  You can open this file with any text editor or Markdown viewer.

## Important Notes and Considerations

*   **Website Changes:**  Websites change! This script is designed to be robust, but if the Minnesota Revisor's Office website significantly changes its HTML structure, the script might break.  If this happens, you'll need to:
    *   Inspect the website's HTML (using your browser's developer tools).
    *   Identify the new HTML elements and attributes used for the title, rule links, and rule content.
    *   Modify the `scrape_fire_code_rules` and `scrape_rule_page` functions in the Python script accordingly, updating the CSS selectors (e.g., `soup.find('div', class_='section')`) to match the new structure.  The extensive comments in the code will guide you.
*   **Rate Limiting:** The `time.sleep()` calls introduce delays to avoid overwhelming the website.  Do *not* remove these delays.
*   **Error Handling:** The script includes basic error handling, but for production use, you might want to add more comprehensive error handling and logging.
*   **`robots.txt`:** While this script doesn't explicitly check `robots.txt`, it is good practice.
*   **Terms of Service:** Always respect the website's terms of service. Web scraping should be done ethically and responsibly.  The author of this script is not responsible for any misuse.
* **Headless Mode:** The script runs Chrome in "headless" mode (no visible browser window). If you want to *see* the browser while it's running (for debugging, for example), remove the `options.add_argument("--headless")` line in the `scrape_fire_code_rules` function.
* **TensorFlow Lite Messages:** If you see messages related to "TensorFlow Lite XNNPACK delegate", these are likely unrelated to the scraper and can be ignored. They are probably coming from another library or process on your system.

## Contributing

If you find any issues or have suggestions for improvements, feel free to create an issue or submit a pull request on GitHub.

## License
Feel free to add a license. I recommend MIT.