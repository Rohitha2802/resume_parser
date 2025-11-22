import pickle
import json
from extractors import *

# Load model + vectorizer
model, vectorizer = pickle.load(open("model.pkl", "rb"))

def classify_line(line):
    vec = vectorizer.transform([line])
    return model.predict(vec)[0]

def parse_resume(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    output = {
        "name": "",
        "email": "",
        "phone": "",
        "about_me": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": []
    }

    for line in lines:
        label = classify_line(line)

        if label == "NAME" and output["name"] == "":
            output["name"] = line

        elif label == "EMAIL":
            emails = extract_email(line)
            if emails:
                output["email"] = emails[0]

        elif label == "PHONE":
            phones = extract_phone(line)
            if phones:
                output["phone"] = phones[0]

        elif label == "ABOUT_ME":
            output["about_me"] += " " + line

        elif label == "SKILLS":
            output["skills"].extend(extract_skills(line))

        elif label == "EXPERIENCE":
            exp = extract_experience(line)
            if exp:
                output["experience"].append(exp)

        elif label == "EDUCATION":
            edu = extract_education(line)
            if edu:
                output["education"].append(edu)

        elif label == "CERTIFICATIONS":
            output["certifications"].append(line)

    return output


# Example
if __name__ == "__main__":
    resume_text = """
    John Doe
    Email: eswaralakshmi@gmail.com
    Phone: 8888855558
    I am a passionate software engineer with interest in AI.
    Skills: Python, Java, SQL 
    Worked at Infosys from 2019 to 2022
    Completed B.Tech in AI&DS from JNTU 2022
    Certified in AWS Cloud Practitioner 
    certified in NLP
    """
    
    structured = parse_resume(resume_text)
    print(json.dumps(structured, indent=4))
