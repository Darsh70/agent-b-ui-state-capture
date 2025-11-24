import os
import time
from dotenv import load_dotenv
from browser_manager import BrowserManager
from ai_handler import AIHandler

load_dotenv()

def run_task(task_name, goal, start_url):

    browser = BrowserManager(headless=False)
    ai = AIHandler()
    
    # Create dataset folder to store screenshots
    folder = f"dataset/{task_name}"
    os.makedirs(folder, exist_ok=True)
    
    try:
        browser.start()
        browser.navigate(start_url)
        
        history = []
        for step in range(1, 100):
            print(f"\nStep {step}")
            
            # Analyze UI State
            dom_text = browser.analyze_page()
            screenshot_path = f"{folder}/step_{step:02d}.png"
            browser.capture_screenshot(screenshot_path)
            
            # Ask AI
            decision = ai.get_next_action(goal, history, dom_text, screenshot_path)
            print(f"Plan: {decision.action} {decision.element_id} -> {decision.reasoning}")
            
            # Run browser automation script using Playwright
            success = browser.execute_action(
                decision.element_id, 
                decision.action, 
                decision.input_text
            )
            
            # Log History
            target_label = browser.get_element_label(decision.element_id)
            if success:
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
        task_name="linear_new_project", 
        goal="How do I create a new project in Linear?", 
        start_url="https://linear.app"
    )