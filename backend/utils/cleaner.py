import re

def clean_text(text: str) -> str:
    """
    Cleans extracted webpage text before sending to LLM.
    Includes:
    - Universal cleaning
    - Wikipedia-specific cleaning
    - Citation removal
    - Header/footer removal
    - TOC removal
    - Removal of menu/tool garbage
    - Truncation for LLM safety
    """

    if not text:
        return ""

    # 1. Remove Wikipedia language sidebar (the huge 88-language block)
    text = re.sub(r"Toggle the table of contents.*?From Wikipedia, the free encyclopedia", 
                  "From Wikipedia, the free encyclopedia", 
                  text, 
                  flags=re.DOTALL)

    # 2. Remove TOC sections entirely
    text = re.sub(r"Contents \[hide\].*?hide", "", text, flags=re.DOTALL)

    # Remove new Wikipedia TOC patterns (mobile layout)
    text = re.sub(r"(Contents|Table of Contents).*?Hide", "", text, flags=re.DOTALL)

    # 3. Remove bracketed citations [1], [23], [citation needed]
    text = re.sub(r"\[\s*\d+\s*\]", "", text)
    text = re.sub(r"\[citation needed\]", "", text, flags=re.IGNORECASE)

    # 4. Remove edit links, Tools menus, View history etc.
    text = re.sub(r"(Edit\s+source|Edit section|View history|Tools|Download as PDF|Printable version)", "", text)

    # 5. Remove unnecessary navigation/metadata lines
    text = re.sub(r"(Read\s+Edit\s+View history|Article\s+Talk)", "", text)

    # 6. Remove super-short garbage lines (< 25 chars)
    cleaned_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if len(stripped) < 25:
            continue
        cleaned_lines.append(stripped)
    text = "\n".join(cleaned_lines)

    # 7. Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # 8. Keep only first 12,000 characters (safe for Groq)
    text = text[:12000]

    return text.strip()

def clean_merge_texts(text_dict):
    """
    Clean multiple texts and merge them into one block.
    Returns: (merged_text, cleaned_dict)
    """
    print("[MultiSource] Cleaning and merging texts...")
    cleaned_dict = {}
    merged_parts = []
    
    for url, raw_text in text_dict.items():
        if not raw_text:
            cleaned_dict[url] = ""
            continue
            
        cleaned = clean_text(raw_text)
        cleaned_dict[url] = cleaned
        
        if cleaned:
            merged_parts.append(f"--- SOURCE: {url} ---\n{cleaned}\n")
            
    merged_text = "\n".join(merged_parts)
    return merged_text, cleaned_dict
