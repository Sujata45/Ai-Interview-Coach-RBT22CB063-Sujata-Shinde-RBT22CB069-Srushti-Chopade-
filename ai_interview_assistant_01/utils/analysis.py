from utils.llm_call import get_response_from_llm, parse_json_response
from utils.prompts import next_question_generation, feedback_generation

def generate_next_question(prev_question, response, resume_highlights, job_desc):
    prompt = next_question_generation.format(
        previous_question=prev_question,
        candidate_response=response,
        resume_highlights=resume_highlights,
        job_description=job_desc,
    )
    raw = get_response_from_llm(prompt)
    parsed = parse_json_response(raw)
    return parsed.get("next_question")

def generate_feedback(question, response, resume_highlights, job_desc):
    prompt = feedback_generation.format(
        question=question,
        candidate_response=response,
        job_description=job_desc,
        resume_highlights=resume_highlights,
    )
    raw = get_response_from_llm(prompt)
    parsed = parse_json_response(raw)
    feedback = parsed.get("feedback", "No feedback available.")
    score = parsed.get("score", 0)
    try:
        score = float(score)
    except Exception:
        score = 0
    return feedback, score
