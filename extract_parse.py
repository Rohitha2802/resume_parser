import re
import json

def extract_name(text):
    # First line usually contains name
    lines = text.strip().split("\n")
    first_line = lines[0].strip()
    if len(first_line.split()) <= 4:
        return first_line
    return ""

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else ""

def extract_phone(text):
    match = re.search(r"\b[6-9]\d{9}\b", text)
    return match.group() if match else ""
import re

def extract_about(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    about = []

    for line in lines:
        l = line.lower()

        if l.startswith(("skills", "technical skills", "experience", "work experience",
                         "education", "projects", "certifications", "achievements")):
            break

        if "@" in l:
            continue

        if re.search(r"\b[6-9][0-9]{9}\b", l):
            continue

        if re.fullmatch(r"\d{4}", l):
            continue

        if len(line.split()) >= 5:
            about.append(line)

    return " ".join(about).strip()


def extract_skills(text):
    match = re.search(r"Skills:\s*(.*?)(?:Experience:|Education:|Certifications:)", text, re.S)
    if not match:
        return []
    skills_block = match.group(1)
    skills = re.split(r",|\n", skills_block)
    skills = [s.strip().lower() for s in skills if s.strip() and s.strip() != "skills:"]
    return skills

def extract_experience(text):
    exp = []
    pattern = r"(.*?) from (\d{4}) to (\d{4})"
    matches = re.findall(pattern, text)
    for m in matches:
        exp.append({
            "company": m[0].replace("Experience:", "").strip(),
            "start_year": m[1],
            "end_year": m[2]
        })
    return exp

def extract_education(text):
    edu = []
    pattern = r"(.*?),\s*(.*?),\s*(\d{4})"
    matches = re.findall(pattern, text)
    for m in matches:
        stream = m[0].replace("Education:", "").strip()
        university = m[1].strip()
        pass_year = m[2].strip()

        if pass_year.isdigit():
            edu.append({
                "stream": stream,
                "university": university,
                "pass_year": pass_year
            })

    return edu

def extract_certifications(text):
    cert_block = re.search(r"Certifications:(.*)", text, re.S)
    if not cert_block:
        return []

    lines = cert_block.group(1).strip().split("\n")
    certs = [l.strip() for l in lines if l.strip() and ":" not in l]
    return certs

def parse_resume(text):
    result = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "about_me": extract_about(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
        "certifications": extract_certifications(text)
    }

    return json.dumps(result, indent=4)

if __name__ == "__main__":
    with open("resume.txt", "r", encoding="utf-8") as f:
        text = f.read()

    print(parse_resume(text))
