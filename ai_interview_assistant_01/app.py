import streamlit as st
from utils.llm_call import get_response_from_llm, parse_json_response
from utils.prompts import basic_details, next_question_generation, feedback_generation
from utils.analysis import generate_next_question, generate_feedback
from utils.save_utils import save_interview_log
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="AI Interview Assistant", layout="wide")
st.title("AI Interview Assistant")

MAX_QUESTIONS = 5

def sidebar_inputs():
    uploaded_resume = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_description = st.sidebar.text_area("Paste Job Description")
    role = st.sidebar.selectbox("Select Role", ["Software Developer","Tester","DevOps Engineer"])
    max_q = st.sidebar.number_input("Max Questions", min_value=1, max_value=10, value=MAX_QUESTIONS)
    st.session_state['max_questions'] = max_q
    submit = st.sidebar.button("Submit")
    return uploaded_resume, job_description, role, submit

def parse_resume(uploaded_resume):
    if uploaded_resume is None:
        return None
    raw = None
    try:
        raw = uploaded_resume.read()
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8', errors='ignore')
    except Exception:
        raw = str(uploaded_resume)
    return raw

def main():
    if 'initialized' not in st.session_state:
        st.session_state.update({
            "initialized": True,
            "name": "",
            "resume_highlights": "",
            "job_description": "",
            "role": "",
            "qa_index": 1,
            "conversations": [],
            "current_question": "",
            "interview_started": False,
            "interview_completed": False,
            "messages": [],
            "max_questions": MAX_QUESTIONS,
        })

    uploaded_resume, job_description, role, submit = sidebar_inputs()

    if submit and uploaded_resume and job_description:
        resume_text = parse_resume(uploaded_resume)
        prompt = basic_details.format(resume_content=resume_text)
        resp_text = get_response_from_llm(prompt)
        parsed = parse_json_response(resp_text)
        name = parsed.get("name", "Candidate")
        highlights = parsed.get("resume_highlights", "")
        st.session_state["name"] = name
        st.session_state["resume_highlights"] = highlights
        st.session_state["job_description"] = job_description
        st.session_state["role"] = role
        st.success(f"Parsed resume for {name}. Role: {role}")
        st.session_state["current_question"] = "Tell me about yourself and your experience."
        st.session_state["messages"] = [{"role":"assistant","content":st.session_state["current_question"]}]
        st.session_state["interview_started"] = True

    if not st.session_state["interview_started"]:
        st.info("Upload resume and paste job description, then click Submit in the sidebar to start.")
        return

    st.subheader(f"Interviewing: {st.session_state['name']} — Role: {st.session_state['role']}")
    st.markdown(f"**Question {st.session_state['qa_index']} of {st.session_state['max_questions']}**")
    for m in st.session_state["messages"]:
        if m["role"] == "assistant":
            st.markdown(f"**AI:** {m['content']}")
        else:
            st.markdown(f"**You:** {m['content']}")

    if not st.session_state["interview_completed"]:
        user_input = st.text_area("Your Answer:", key=f"ans_{st.session_state['qa_index']}")
        if st.button("Submit Answer"):
            # append user message
            st.session_state["messages"].append({"role":"user","content":user_input})
            # generate feedback and next question
            feedback, score = generate_feedback(
                st.session_state["current_question"],
                user_input,
                st.session_state["resume_highlights"],
                st.session_state["job_description"],
            )
            next_q = generate_next_question(
                st.session_state["current_question"],
                user_input,
                st.session_state["resume_highlights"],
                st.session_state["job_description"],
            )
            st.session_state["conversations"].append({
                "Question": st.session_state["current_question"],
                "Candidate Answer": user_input,
                "Evaluation": score,
                "Feedback": feedback,
            })
            st.session_state["qa_index"] += 1
            if st.session_state["qa_index"] <= st.session_state["max_questions"]:
                st.session_state["current_question"] = next_q or "Can you elaborate further?"
                st.session_state["messages"].append({"role":"assistant","content":st.session_state["current_question"]})
            else:
                st.session_state["interview_completed"] = True
                st.session_state["messages"].append({"role":"assistant","content":"Thank you. The interview is complete."})
            st.rerun()

    else:
        st.success("Interview completed")
        score = sum([c.get("Evaluation",0) for c in st.session_state["conversations"]]) / max(len(st.session_state["conversations"]),1)
        st.markdown(f"**Overall score:** {score:.2f}/10")
        if st.button("Save Interview Log"):
            save_interview_log(st.session_state["conversations"], filename=f"interview_{st.session_state['name']}.json")
            st.success("Saved interview log.")
if __name__ == '__main__':
    main()
