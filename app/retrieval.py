import json
import os

def get_all_schemes():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_schemes.json')
    with open(file_path, 'r', encoding = 'utf-8') as f:
        return json.load(f)

def get_knowledge_context():
    schemes = get_all_schemes()

    if isinstance(schemes, dict) and "schemes" in schemes and isinstance(schemes["schemes"], list):
        schemes = schemes["schemes"]

    elif isinstance(schemes, dict):
        schemes = list(schemes.values())

    if not isinstance(schemes, list):
        print(f"Warning: Expected a list of schemes, got {type(schemes)}")
        return "No valid scheme data available."
    
    context = ""
    for idx, s in enumerate(schemes, 1):
        if isinstance(s, dict):
            name = s.get("name", "Unknown Scheme")
            desc = s.get("description", "No description available.")
            eligibility = s.get("eligibility_criteria", [])
            docs = s.get("documents_required", [])

            if isinstance(eligibility, str): 
                eligibility = [eligibility]
            if isinstance(docs, str): 
                docs = [docs]

            context += f"Scheme {idx}: {name}\n"
            context += f"Description: {desc}\n"
            context += f"Eligibility: {', '.join(eligibility)}\n"
            context += f"Required Documents: {', '.join(docs)}\n\n"
        else:
            context += f"Scheme {idx}: {s}\n\n"
            
    return context
