import time
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright
from dom_scripts import PAGE_ANALYSIS_SCRIPT

class BrowserManager:
    def __init__(self, headless=False, user_data_dir="./browser_data"):
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.playwright = None
        self.browser_context = None
        self.page = None
        self.element_map: Dict[int, Any] = {}

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser_context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )
        self.page = self.browser_context.new_page()

    def stop(self):
        if self.browser_context: self.browser_context.close()
        if self.playwright: self.playwright.stop()

    def navigate(self, url: str):
        try:
            if not url.startswith("http"):
                url = "https://" + url
            self.page.goto(url)
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return False

    def capture_screenshot(self, path):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.screenshot(path=path)

    def analyze_page(self) -> str:
        try:
            raw_elements = self.page.evaluate(PAGE_ANALYSIS_SCRIPT)
            self.element_map = {el['id']: el for el in raw_elements}
            
            llm_view = []
            for el in raw_elements:
                llm_view.append(f"[{el['id']}] <{el['tag']}> {el['text']}")
            return "\n".join(llm_view)
        except Exception as e:
            return f"Error: {e}"

    def execute_action(self, element_id: Optional[int], action_type: str, input_text: str = "", url: str = "") -> bool:
        
        # Navigation
        if action_type == "navigate":
            if url:
                print(f"Navigating to: {url}")
                return self.navigate(url)
            return False

        # Blind Type
        if action_type == "type" and element_id is None:
            print(f"Blind Typing: '{input_text}'")
            try:
                self.page.keyboard.type(input_text)
                time.sleep(0.5)
                self.page.keyboard.press("Enter")
                return True
            except Exception as e:
                print(f"Blind type failed: {e}")
                return False

        # Standard Interaction
        if element_id not in self.element_map:
            print(f"Element ID {element_id} not found.")
            return False
            
        el_data = self.element_map[element_id]
        x, y = el_data['x'], el_data['y']
        
        try:
            if action_type == "type":
                # Click once to focus
                self.page.mouse.click(x, y)
                time.sleep(0.1)
                
                # Triple click to select the text inside the field
                self.page.mouse.click(x, y, click_count=3) 
                
                self.page.keyboard.press("Backspace")
                self.page.keyboard.type(input_text)
                self.page.keyboard.press("Enter")
                return True
            elif action_type == "click":
                self.page.mouse.click(x, y)
                return True
        except Exception as e:
            print(f"Interaction failed: {e}")
            return False
        
        return False
            
    def get_element_label(self, element_id: Optional[int]) -> str:
        if element_id is not None and element_id in self.element_map:
            return self.element_map[element_id].get('text', 'Unknown')
        return "Blind_Action"