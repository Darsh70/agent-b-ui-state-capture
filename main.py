import os
import time
import json
from dotenv import load_dotenv
from browser_manager import BrowserManager
from ai_handler import AIHandler

load_dotenv()

def run_task(task_name, goal, start_url):
    browser = BrowserManager(headless=False)
    ai = AIHandler()
    
    # Create folders to store screenshots and metadata
    base_folder = f"dataset/{task_name}"
    screenshots_folder = os.path.join(base_folder, "screenshots")
    metadata_path = os.path.join(base_folder, "metadata.json")
    
    os.makedirs(screenshots_folder, exist_ok=True)
    
    metadata_log = []
    
    try:
        browser.start()
        browser.navigate(start_url)
        
        history = []
        
        for step in range(1, 100):
            print(f"\nStep {step}")
            
            dom_text = browser.analyze_page()
            screenshot_filename = f"step_{step:02d}.png"
            screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
            browser.capture_screenshot(screenshot_path)
            
            decision = ai.get_next_action(goal, history, dom_text, screenshot_path)
            print(f"Plan: {decision.action} {decision.element_id} -> {decision.reasoning}")
            
            # Save Metadata
            step_data = decision.model_dump() 
            step_data["screenshot_file"] = screenshot_filename
            step_data["step_number"] = step
            metadata_log.append(step_data)
            
            with open(metadata_path, "w") as f:
                json.dump(metadata_log, f, indent=2)

            
            success = browser.execute_action(
                decision.element_id, 
                decision.action, 
                decision.input_text,
                decision.url
            )
            
            target_label = browser.get_element_label(decision.element_id)
            
            if decision.action == "navigate":
                history.append(f"Navigated to {decision.url}")
            elif success:
                history.append(f"{decision.action} on '{target_label}'")
            else:
                history.append(f"FAILED {decision.action} on {decision.element_id}")

            if decision.action == "finish":
                print("Task Finished.")
                break
                
            time.sleep(2)
            
    finally:
        browser.stop()

if __name__ == "__main__":
    # time.sleep(20)
    run_task(
        task_name="google_sheet_delete_project", 
        goal="Delete google sheets project titled SoftLight", 
        start_url="https://docs.google.com/spreadsheets" 
    )