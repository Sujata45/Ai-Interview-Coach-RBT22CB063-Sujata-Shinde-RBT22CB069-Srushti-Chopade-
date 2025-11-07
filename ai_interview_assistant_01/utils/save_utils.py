import json, os

def save_interview_log(log, filename='interview_log.json'):
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    return filename
