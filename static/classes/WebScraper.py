from playwright.sync_api import sync_playwright, expect
import pandas as pd
from typing import List, Dict, Optional

class WebScraper:
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper
        Args:
            headless: Whether to run browser in headless mode
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.playwright.stop()

    async def wait_for_load(self):
        """Wait for different load states"""
        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.wait_for_load_state("networkidle")

    def navigate(self, url: str, wait_for_selector: Optional[str] = None):
        """
        Navigate to URL and wait for content
        Args:
            url: Target URL
            wait_for_selector: Optional CSS selector to wait for
        """
        self.page.goto(url, wait_until="networkidle")
        
        if wait_for_selector:
            self.page.wait_for_selector(wait_for_selector)

    def get_elements(self, selector: str) -> List[Dict]:
        """
        Get elements using CSS selector
        Args:
            selector: CSS selector
        Returns:
            List of elements with their properties
        """
        elements = self.page.query_selector_all(selector)
        return [
            {
                'text': elem.inner_text(),
                'html': elem.inner_html(),
                'attrs': elem.evaluate('el => Object.assign({}, el.attributes)')
            }
            for elem in elements
        ]

    def extract_table(self, table_selector: str) -> pd.DataFrame:
        """
        Extract table data into pandas DataFrame
        Args:
            table_selector: CSS selector for table
        Returns:
            DataFrame containing table data
        """
        # Get table headers
        headers = self.page.eval_on_selector_all(
            f"{table_selector} th",
            "elements => elements.map(el => el.innerText)"
        )
        
        # Get table rows
        rows = self.page.eval_on_selector_all(
            f"{table_selector} tbody tr",
            "rows => rows.map(row => Array.from(row.querySelectorAll('td')).map(cell => cell.innerText))"
        )
        
        return pd.DataFrame(rows, columns=headers)

    def click_and_extract(self, click_selector: str, extract_selector: str, 
                         wait_time: int = 1000) -> str:
        """
        Click an element and extract content after click
        Args:
            click_selector: Selector for element to click
            extract_selector: Selector for content to extract after click
            wait_time: Time to wait after click in milliseconds
        Returns:
            Extracted content
        """
        self.page.click(click_selector)
        self.page.wait_for_timeout(wait_time)
        element = self.page.query_selector(extract_selector)
        return element.inner_text() if element else ""

    def scroll_and_extract(self, selector: str, scroll_times: int = 3) -> List[Dict]:
        """
        Scroll page and extract elements
        Args:
            selector: CSS selector for elements
            scroll_times: Number of times to scroll
        Returns:
            List of extracted elements
        """
        results = []
        for _ in range(scroll_times):
            # Scroll to bottom
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(1000)  # Wait for content to load
            
            # Extract elements
            elements = self.get_elements(selector)
            results.extend(elements)
            
        return list({elem['text']: elem for elem in results}.values())  # Remove duplicates