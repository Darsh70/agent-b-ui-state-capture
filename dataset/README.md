# Agent B Dataset Overview

This directory contains the output for **9 tasks** across **Linear** and **Notion**.

Each task folder includes:

1. **Screenshots** — every captured UI state (pages, modals, popovers, dropdowns, typing states).  
2. **`metadata.json`** — a structured log linking each screenshot to the agent’s reasoning and the executed action.

---

## Linear Workflows
*Focus: SPA navigation, modal states, and blind typing.*

1. **Create a project**  
   - *Goal:* Navigate to the button in left panel and launch the project creation modal.  
   - Captures the modal state (URL does not change). Uses blind typing for the auto-focused title field.

2. **Create an issue and assign it to a person**  
   - *Goal:* Open the issue creation modal and assign it using the dropdown.  
   - Handles dropdown filtering and assignee selection.

3. **Move an issue to a different cycle**  
   - *Goal:* Change the cycle/state of an existing issue.  
   - Handles dropdown navigation and cycle selection.

4. **Add multiple filterable elements to an issue**  
   - *Goal:* Apply multiple labels to a single issue.  
   - Demonstrates the agent’s ability to sequentially add more than one filter item.

5. **Change the theme to dark mode**  
   - *Goal:* Navigate user settings to update theme preferences.  
   - Highlights the agent’s ability to locate the settings page even when the settings button isn’t directly visible. It knows the option may be in the dropdown next to the workspace name.

---

## Notion Workflows
*Focus: Non-semantic HTML (`div` buttons), transient popovers, and context menus.*

1. **Filter a database by "Done"**  
   - *Goal:* Access database filter controls and apply a status filter.  
   - Navigates multi-level popovers and transient menu states.

2. **Duplicate and move a page**  
   - *Goal:* Perform a multi-step file operation.  
   - Handles UI latency and wait states during duplication.

3. **Add a property to a database**  
   - *Goal:* Modify the schema of a Notion database.  
   - Interacts with the property-creation popover.

4. **Change the database to Board view**  
   - *Goal:* Switch the database layout to Board view.  
   - Demonstrates the agent’s ability to handle view options and layout transitions.
