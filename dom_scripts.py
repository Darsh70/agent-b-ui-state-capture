PAGE_ANALYSIS_SCRIPT = """
() => {
    const elements = [];
    let idCounter = 0;

    function isVisible(el) {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && 
               style.visibility !== 'hidden' && style.display !== 'none';
    }

    const selectors = [
        'button', 'a', 'input', 'textarea', 'select',
        '[role="button"]', '[role="link"]', '[role="menuitem"]', 
        '[role="option"]', '[role="tab"]', '[contenteditable="true"]'
    ];
    
    document.querySelectorAll(selectors.join(',')).forEach(el => {
        if (!isVisible(el)) return;
        const rect = el.getBoundingClientRect();
        
        let text = "";
        // Capture Value or Placeholder or Name or generic Label
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            text = el.value || el.placeholder || el.getAttribute('name') || "";
            if (!text) text = "[INPUT FIELD]"; // Fallback so AI sees it exists
        } else {
            text = el.innerText || el.getAttribute('aria-label') || "";
        }
        
        text = text.replace(/\\s+/g, ' ').trim().substring(0, 50);
        
        elements.push({
            id: idCounter++,
            tag: el.tagName.toLowerCase(),
            text: text,
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2
        });
    });
    return elements;
}
"""