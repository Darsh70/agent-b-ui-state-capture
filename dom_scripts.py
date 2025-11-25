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

    // 1. Standard Interactive Elements
    const standardSelectors = [
        'button', 'a', 'input', 'textarea', 'select',
        '[role="button"]', '[role="link"]', '[role="menuitem"]', 
        '[role="option"]', '[role="tab"]', '[contenteditable="true"]'
    ];
    
    const candidates = new Set(Array.from(document.querySelectorAll(standardSelectors.join(','))));

    // 2. Capture DIVs and SPANs that look clickable (cursor: pointer)
    // This fixes the Notion/React issue where buttons are just divs.
    document.querySelectorAll('div, span, svg').forEach(el => {
        if (window.getComputedStyle(el).cursor === 'pointer') {
            candidates.add(el);
        }
    });

    candidates.forEach(el => {
        if (!isVisible(el)) return;
        const rect = el.getBoundingClientRect();
        
        let text = "";
        
        // Capture Value, Placeholder, Name, or InnerText
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            text = el.value || el.placeholder || el.getAttribute('name') || "";
            if (!text) text = "[INPUT FIELD]"; 
        } else {
            text = el.innerText || el.getAttribute('aria-label') || "";
        }
        
        // Clean text
        text = text.replace(/\\s+/g, ' ').trim().substring(0, 50);
        
        // Only keep elements that have text OR are inputs
        // (This prevents capturing thousands of empty clickable divs)
        if (text.length > 0 || el.tagName === 'INPUT' || el.tagName === 'SELECT') {
            elements.push({
                id: idCounter++,
                tag: el.tagName.toLowerCase(),
                text: text,
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            });
        }
    });
    
    return elements;
}
"""