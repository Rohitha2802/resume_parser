import re

def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)

def extract_phone(text):
    pattern = r"\b[6-9]\d{9}\b"
    return re.findall(pattern, text)

def extract_skills(text):
    return [skill.strip() for skill in re.split(r",|/|•|-", text) if skill.strip()]

def extract_experience(text):
    pattern = r"(.*?)(?:\s+from\s+)(\d{4})(?:\s+to\s+)(\d{4}|present)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return {
            "company": match.group(1).strip(),
            "start_year": match.group(2),
            "end_year": match.group(3)
        }
    return None

def extract_education(text):
    pattern = r"(.*?)(\d{4})"
    match = re.search(pattern, text)
    if match:
        return {
            "stream_university": match.group(1).strip(),
            "pass_year": match.group(2)
        }
    return None

def extract_certifications(text):
    return [text.strip()]
