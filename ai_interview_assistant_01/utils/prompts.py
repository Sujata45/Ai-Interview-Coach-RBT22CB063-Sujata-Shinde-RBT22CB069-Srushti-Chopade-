basic_details = """SYSTEM: You are an expert resume parser. Respond ONLY in valid JSON.

Task: Extract candidate name and 5-7 resume highlights.

Resume Content:
{resume_content}

Output format:
{{
  "name": "Full name",
  "resume_highlights": "Short paragraph summarizing 5-7 highlights"
}}
"""

next_question_generation = """SYSTEM: You are an expert interviewer. Respond ONLY in valid JSON.

Inputs:
Previous Question: {previous_question}
Candidate Response: {candidate_response}
Job Description: {job_description}
Resume Highlights: {resume_highlights}

Output format:
{{
  "next_question": "A single open-ended follow-up question"
}}
"""

feedback_generation = """SYSTEM: You are an expert interviewer and assessor. Respond ONLY in valid JSON.

Inputs:
Question: {question}
Candidate Response: {candidate_response}
Job Description: {job_description}
Resume Highlights: {resume_highlights}

Evaluation Guidelines (1–10 scale):
   - 9–10: Excellent — comprehensive, clear, and highly relevant.
   - 7–8: Good — relevant with minor gaps.
   - 5–6: Average — somewhat relevant, needs elaboration.
   - 3–4: Weak — lacks structure or depth.
   - 1–2: Poor — off-topic or incomplete.
   *Give 7–10 for most relevant answers; below 6 only if clearly poor or irrelevant.*

Output format:
{{
  "feedback": "A concise 70–90 word feedback paragraph",
  "score": 1–10
}}
"""
