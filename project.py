import streamlit as st
from google import genai
from PyPDF2 import PdfReader
import json
import re
import time
from fpdf import FPDF

# -------------------------------
# Helper Functions
# -------------------------------


def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip())


def normalize_answer(answer: str) -> str:
    if not answer:
        return ""
    match = re.match(r'([A-Da-d])', answer.strip())
    return match.group(1).upper() if match else ""


def calculate_score(user_answers: list, correct_answers: list) -> int:
    return sum(ua == ca for ua, ca in zip(user_answers, correct_answers))


def save_text_as_pdf(text: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# -------------------------------
# Core Functions
# -------------------------------


def call_gemini_api(prompt: str, client) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"API Error: {e}")
        return ""


def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text


def extract_json(ai_response: str):
    try:
        match = re.search(r'\[.*\]', ai_response, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        st.error(f"JSON parsing error: {e}")
    return None

# -------------------------------
# Main Streamlit App
# -------------------------------


def main():
    st.set_page_config(page_title="AI Study Buddy",
                       page_icon="📘", layout="wide")

    # Load API Key
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("⚠️ Gemini API key not found! Add it to .streamlit/secrets.toml")
        st.stop()

    client = genai.Client(api_key=API_KEY)

    # Sidebar
    st.sidebar.image("assets/logo.png", width=140)
    st.sidebar.title("📘 AI Study Buddy")
    page = st.sidebar.radio(
        "Go to:", ["💬 Chat", "🧾 Summarize Notes", "🎯 Quiz Me"])
    st.sidebar.markdown("---")
    st.sidebar.caption("Made with ❤️ by Saima Usman")

    # -------------------------------
    # Chat Page
    # -------------------------------
    if page == "💬 Chat":
        st.title("💬 Chat with Your Study Buddy")

        # Clear Chat Button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for msg in st.session_state.chat_history:
            role_icon = "🧑" if msg["role"] == "user" else "🤖"
            st.markdown(
                f"**{role_icon} {msg['role'].capitalize()}:** {msg['content']}")

        # Chat input
        user_input = st.chat_input("Type your question here...")
        if user_input:
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input})
            st.markdown(f"**🧑 You:** {user_input}")

            # WhatsApp-style typing dots
            placeholder = st.empty()
            dots = ""
            for _ in range(6):
                dots += "."
                if len(dots) > 3:
                    dots = "."
                placeholder.markdown(f"**🤖 AI is typing{dots}**")
                time.sleep(0.5)

            prompt = f"Answer clearly with line breaks, bullets, and bold headings:\n\n{user_input}"
            ai_response = call_gemini_api(prompt, client)
            placeholder.empty()
            st.markdown(f"**🤖 AI:** {ai_response}")
            st.session_state.chat_history.append(
                {"role": "assistant", "content": ai_response})

            pdf_bytes = save_text_as_pdf("\n".join(
                [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history]))
            st.download_button("💾 Save Chat as PDF", data=pdf_bytes,
                               file_name="AI_Study_Buddy_Chat.pdf", mime="application/pdf")

    # -------------------------------
    # Summarize Notes
    # -------------------------------
    elif page == "🧾 Summarize Notes":
        st.title("🧾 Summarize Your Notes")
        uploaded_file = st.file_uploader(
            "Upload file (PDF or TXT)", type=["pdf", "txt"])

        if uploaded_file:
            notes = read_pdf(
                uploaded_file) if uploaded_file.type == "application/pdf" else uploaded_file.read().decode("utf-8")
            notes = clean_text(notes)
            st.text_area("📜 Extracted Text", notes, height=400)

            if st.button("✨ Generate Summary"):
                with st.spinner("Summarizing..."):
                    prompt = f"Summarize the following notes concisely with bullets and headings:\n\n{notes}"
                    summary = call_gemini_api(prompt, client)
                    st.markdown(summary)

                    pdf_bytes = save_text_as_pdf(summary)
                    st.download_button("💾 Save Summary as PDF", data=pdf_bytes,
                                       file_name="AI_Study_Buddy_Summary.pdf", mime="application/pdf")

    # -------------------------------
    # Quiz Page
    # -------------------------------
    elif page == "🎯 Quiz Me":
        st.title("🎯 Quiz Me from Notes")
        quiz_text = st.text_area("Paste your notes below:", height=400)
        generate_clicked = st.button("🧩 Generate Quiz")

        if "quiz_data" not in st.session_state:
            st.session_state.quiz_data = None
            st.session_state.user_answers = []

        if generate_clicked and quiz_text.strip():
            with st.spinner("Generating quiz..."):
                quiz_prompt = f"""
                Create 5 multiple-choice questions from the following notes.
                Each question must have exactly 4 options labeled A-D.
                Do NOT include answers.
                Return the output in JSON format as a list of objects:
                [
                  {{
                    "question": "Question text",
                    "options": ["A) ...", "B) ...", "C) ...", "D) ..."]
                  }}
                ]
                Notes:
                {quiz_text}
                """
                ai_response = call_gemini_api(quiz_prompt, client)
                st.session_state.quiz_data = extract_json(ai_response)
                if st.session_state.quiz_data:
                    st.session_state.user_answers = [
                        ""] * len(st.session_state.quiz_data)
                else:
                    st.error(
                        "Failed to parse AI response. Make sure the AI returns valid JSON.")

        if st.session_state.quiz_data:
            st.subheader("📝 Quiz Questions:")
            for idx, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"**Q{idx+1}. {q['question']}**")
                st.session_state.user_answers[idx] = st.radio(
                    f"Select an answer for Q{idx+1}:",
                    q["options"],
                    key=f"q{idx}"
                )

            if st.button("✅ Submit Quiz"):
                answer_prompt = f"""
                Provide ONLY the correct option letters (A, B, C, or D) in JSON array format:
                {json.dumps(st.session_state.quiz_data)}
                """
                ai_answers = call_gemini_api(answer_prompt, client)
                correct_answers = extract_json(ai_answers)

                if not correct_answers:
                    st.error(
                        "Failed to parse AI answers. Model might have returned invalid JSON.")
                else:
                    if isinstance(correct_answers[0], dict):
                        correct_answers = [list(a.values())[0]
                                           for a in correct_answers]

                    normalized_answers = [normalize_answer(str(a).replace(
                        ")", "").replace(".", "")) for a in correct_answers]
                    user_answers = [normalize_answer(
                        a) for a in st.session_state.user_answers]
                    score = calculate_score(user_answers, normalized_answers)

                    st.subheader("📊 Quiz Results:")

                    for idx, (ua, ca, q) in enumerate(zip(user_answers, normalized_answers, st.session_state.quiz_data)):
                        if ua == ca:
                            st.markdown(
                                f"**Q{idx+1}. {q['question']}** ✅ Correct!\n- Your answer: **{ua}**")
                        else:
                            st.markdown(
                                f"**Q{idx+1}. {q['question']}** ❌ Wrong!\n- Your answer: **{ua or 'No answer'}**\n- Correct: **{ca}**")

                    st.success(
                        f"🎉 Your total score: {score} / {len(normalized_answers)}")

                    if score == len(normalized_answers):
                        st.balloons()
                        st.toast(
                            "🌟 Amazing! You nailed every question!", icon="🎯")
                    elif score >= len(normalized_answers)*0.7:
                        st.toast("🎉 Great job! Keep going!", icon="💡")
                    else:
                        st.toast(
                            "Keep practicing! You'll get there 💪", icon="💡")

    # -------------------------------
    # Footer
    # -------------------------------
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: #999999;
        padding: 5px 0;
        background-color: #f8f9fa;
        border-top: 1px solid #eaeaea;
    }
    </style>
    <div class="footer">
        © 2025 AI Study Buddy — All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
