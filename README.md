# Final Project by Saima Usman
# 🤖 AI Study Buddy - Your Smart Study Partner
#### Video Demo: https://youtu.be/hLJ6vtoMfrs

#### Description:
AI Study Buddy is your smart virtual study companion powered by Google Gemini. 
It helps you **chat**, **summarize notes**, and **generate quizzes** — all in one place.

AI Study Buddy is an intelligent, interactive Streamlit application designed to help students and lifelong learners study more effectively using the power of artificial intelligence. By integrating Google’s Gemini API, the app assists users in chatting about study topics, summarizing notes, and generating customized multiple-choice quizzes — all in one intuitive interface. It acts as a virtual study companion that enhances comprehension, retention, and active recall through AI-powered interactions.

---

## 🎯 Project Overview

The AI Study Buddy is built with Python and Streamlit, offering a seamless web interface that does not require any technical setup from end users. Users can chat directly with an AI model to ask questions, summarize their uploaded notes (PDF or text), or test their understanding through automatically generated quizzes. The app is designed for accessibility, simplicity, and performance, ensuring a productive and engaging learning experience.

This project demonstrates the integration of frontend interactivity (Streamlit) with AI backend processing (Gemini API) and document parsing (PyPDF2). It showcases how artificial intelligence can be embedded into education tools to make studying smarter, faster, and more enjoyable.

---

## ⚙️ Features - Built with Streamlit + Gemini AI

### 💬 Chat with AI
Ask the AI assistant any study-related question and receive structured, well-formatted answers with headings, bullet points, and explanations. Perfect for clarifying concepts and understanding complex topics.

### 🧾 Summarize Notes
Upload your lecture notes or textbooks in PDF or TXT format, and the app automatically extracts and summarizes key information concisely. The text is cleaned, processed, and summarized by the Gemini model for quick review.

### 🎯 Quiz Me
Generate quizzes instantly from your notes or on any given topic. The AI creates five multiple-choice questions (A–D options), and once you answer, it checks your responses, calculates your score, and highlights correct and incorrect answers. This feature promotes active recall and self-assessment.

### ✅ Testable Backend
Core functions such as `clean_text()`, `normalize_answer()`, `calculate_score()`, and `extract_json()` are modular and independently testable using **pytest**, ensuring the app’s logic is reliable and maintainable.

### ✅ To hide external library warnings, RUN:
pytest test_project.py -p no:warnings

---

## 🧩 Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **AI Backend**: Google Gemini API (`google.genai`) - ***model="gemini-2.5-flash"***
- **PDF Processing**: PyPDF2
- **Language**: Python 3.10+
- **Testing Framework**: pytest
- **Data Handling**: JSON, Regex

---

## 🚀 Installation and Setup Guide

1️⃣ **Clone the Repository**
Open your terminal or command prompt.

git clone https://github.com/Saim2026/ai-study-buddy.git
cd ai-study-buddy

2️⃣ **Create a Virtual Environment**
Create an isolated environment for dependencies:
Run: python -m venv venv

Activate the virtual environment:
Windows: venv\Scripts\activate
**If you get a PowerShell security warning, run this first:**
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
(OR grant access as an administrator)

macOS/Linux: **source venv/bin/activate**

3️⃣ **Install Required Dependencies**
Install all the required Python packages using:
pip install -r requirements.txt

4️⃣ **Configure your Gemini API Key**
Inside your project directory, create a folder named .streamlit.
Inside .streamlit, create a file named secrets.toml.
Add your Google Gemini API key like this: 
GEMINI_API_KEY = "your_api_key_here"

5️⃣ **Run the Streamlit App**
Once everything is set up, start the app with:
**streamlit run project.py**

Wait a few seconds for Streamlit to start the local server.

6️⃣ **Access the Application**
When the server starts, Streamlit will open the app in your default web browser.


7️⃣ **Explore the Features**
💬 **Chat Tab:** Ask study questions and get AI-generated explanations.
🧾 **Summarize Notes Tab:** Upload a .pdf or .txt file and generate summaries.
🎯 **Quiz Me Tab:** Paste your notes, generate AI-based quizzes, and test yourself.


8️⃣ **Run Tests** (Optional) 
Verify that helper functions work correctly using pytest:
Run: pytest -v

All tests in test_project.py should pass successfully.

Thank you!

by Saima Usman
Final Project:**CS50’s Introduction to Programming with Python by Harvard**