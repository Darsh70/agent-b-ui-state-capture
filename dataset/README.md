# Agent B Dataset Overview

This directory contains the output for **9 tasks** across **Linear** and **Notion**.

Each task folder includes:

1. **Screenshots** — every captured UI state (pages, modals, popovers, dropdowns, typing states).  
2. **`metadata.json`** — a structured log linking each screenshot to the agent’s reasoning and the executed action.

---

## Linear Workflows
*Focus: SPA navigation, modal states, and blind typing.*

1. **How do I create a new project?**  
   - *Goal:* Navigate to the button in left panel and launch the project creation modal.  
   - Captures the modal state (URL does not change). Uses blind typing for the auto-focused title field.

   ```bash
   #main.py
   run_task(
        task_name="notion_new_project", 
        goal="How do I create a new project?", 
        start_url="https://www.notion.so/" 
    )
    ```


2. **How do I create an issue and assign it to a person?**  
   - *Goal:* Open the issue creation modal and assign it using the dropdown.  
   - Handles dropdown filtering and assignee selection.
   ```bash
   #main.py
   run_task(
        task_name="notion_create_assign_issue", 
        goal="How do I create an issue and assign it to a person?", 
        start_url="https://www.notion.so/" 
    )
    ```

3. **How do I move an issue to a different cycle?**  
   - *Goal:* Change the cycle/state of an existing issue.  
   - Handles dropdown navigation and cycle selection.

   ```bash
   #main.py
   run_task(
        task_name="linear_move_issue_to_different_cycle", 
        goal="How do I move an issue to a different cycle?", 
        start_url="https://linear.app" 
    )
    ```

4. **How do I add multiple filterable elements to an issue?**  
   - *Goal:* Apply multiple labels to a single issue.  
   - Demonstrates the agent’s ability to sequentially add more than one filter item.

   ```bash
   #main.py
   run_task(
        task_name="linear_add_filters_to_issue", 
        goal="How do I add multiple filterable elements to an issue in Linear?", 
        start_url="https://linear.app" 
    )
    ```

5. **How do I change the theme to dark mode?**  
   - *Goal:* Navigate user settings to update theme preferences.  
   - Highlights the agent’s ability to locate the settings page even when the settings button isn’t directly visible. It knows the option may be in the dropdown next to the workspace name.

   ```bash
   #main.py
   run_task(
        task_name="linear_change_theme", 
        goal="How do I change interface theme to dark?", 
        start_url="https://linear.app" 
    )
    ```

---

## Notion Workflows
*Focus: Non-semantic HTML (`div` buttons), transient popovers, and context menus.*

1. **How do I filter a To Do List by "Done"?**  
   - *Goal:* Access database filter controls and apply a status filter.  
   - Navigates multi-level popovers and transient menu states.

   ```bash
   #main.py
   run_task(
        task_name="notion_filter_todo_by_done", 
        goal="How do I filter a To Do List by tasks that are done?", 
        start_url="https://www.notion.so/" 
    )
    ```

2. **How do I duplicate and move a page?**  
   - *Goal:* Perform a multi-step file operation.  
   - Handles UI latency and wait states during duplication.

   ```bash
   #main.py
   run_task(
        task_name="notion_move_duplicated_page", 
        goal="How do I duplicate To Do List and move it to Weekly To Do List?", 
        start_url="https://www.notion.so/" 
    )
    ```

3. **How do I add a property to a database?**  
   - *Goal:* Modify the schema of a Notion database.  
   - Interacts with the property-creation popover.

   ```bash
   #main.py
   run_task(
        task_name="notion_add_property", 
        goal="How do I add a status property in my database?", 
        start_url="https://www.notion.so/" 
    )
    ```

4. **How do I change the database to Board view?**  
   - *Goal:* Switch the database layout to Board view.  
   - Demonstrates the agent’s ability to handle view options and layout transitions.

   ```bash
   #main.py
   run_task(
        task_name="notion_add_board_view_database", 
        goal="How do I convert a table database into a board view?", 
        start_url="https://www.notion.so/" 
    )
    ```
