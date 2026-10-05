# 📄 Resume Analyzer

An AI-powered **Resume Analyzer** built with **Python, Streamlit, LangGraph, and Groq**.

The application allows users to upload a resume in **PDF or DOCX format** and provide a **job description**. It then analyzes the candidate's skills against the job requirements, identifies matching and missing skills, and generates practical improvement suggestions and a final report.

---

## 🚀 Features

- 📄 Upload resumes in **PDF** and **DOCX** format
- 📝 Paste any job description
- 🧠 Extract skills from the resume
- 🎯 Extract required skills from the job description
- ✅ Identify matching skills
- ❌ Identify missing skills
- 💡 Generate personalized improvement suggestions
- 📊 Generate an ATS compatibility score
- 📑 Generate a professional final analysis report
- ⚡ Sequential workflow using LangGraph
- 🎨 Interactive Streamlit interface

---

## 🏗️ Architecture

The project uses a sequential workflow where each step performs a specific task.

```text
Resume PDF / DOCX
        │
        ▼
Document Text Extraction
        │
        ▼
┌──────────────────────────────┐
│      LangGraph Workflow      │
├──────────────────────────────┤
│                              │
│  1. Required Skills          │
│             ↓                │
│  2. Find Matching Skills     │
│             ↓                │
│  3. Generate Suggestions     │
│             ↓                │
│  4. Generate Final Report    │
│                              │
└──────────────────────────────┘
        │
        ▼
Streamlit Results
```

---

## 📁 Project Structure

```text
resume-analyzer/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
│
├── document/
│   ├── __init__.py
│   ├── loader.py
│   ├── cleaner.py
│   └── scrap.py
│
├── llm/
│   ├── __init__.py
│   └── model.py
│
├── prompts/
│   ├── resume.py
│   ├── jd.py
│   └── report.py
│
└── utils/
    ├── __init__.py
    └── helpers.py
```

---

## 🔄 Workflow

The current workflow is sequential:

```text
START
  ↓
required_skills
  ↓
find_skills
  ↓
suggestion
  ↓
output
  ↓
END
```

### 1. Required Skills

The first node analyzes:

- Resume text
- Job description

and extracts:

- Candidate skills
- Required job skills

### 2. Find Skills

The second node compares the two skill sets and identifies:

- Matching skills
- Missing skills

### 3. Suggestions

The third node generates:

- Skill improvement suggestions
- Skills to learn
- Resume improvement suggestions
- ATS compatibility score

### 4. Final Output

The final node creates a professional report containing the analysis and an **Expert Advice** section.

---

## 🧰 Technologies Used

- **Python**
- **Streamlit** — Web interface
- **LangGraph** — Workflow orchestration
- **LangChain Core** — LLM integration
- **LangChain Groq** — Groq model integration
- **Groq** — LLM inference
- **PyPDF** — PDF text extraction
- **Unstructured** — DOCX/document processing
- **python-dotenv** — Environment variable management

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-analyzer.git
```

### 2. Open the project directory

```bash
cd resume-analyzer
```

### 3. Create a virtual environment

Using `uv`:

```bash
uv venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not commit your `.env` file or expose your API key publicly.

Make sure `.env` is included in `.gitignore`.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## 🖥️ How to Use

### Step 1 — Upload Resume

Upload your resume in one of the supported formats:

```text
.pdf
.docx
```

### Step 2 — Add Job Description

Paste the complete job description into the job description field.

### Step 3 — Analyze

Click:

```text
🔍 Analyze Resume
```

The application will process the resume and job description through the LangGraph workflow.

### Step 4 — View Results

The application displays:

```text
📝 Resume Skills
🎯 Required Skills
✅ Matching Skills
❌ Missing Skills
💡 Suggestions
📄 Final Report
```

---

## 📊 Example Workflow

Suppose the resume contains:

```text
Python
Machine Learning
SQL
LangChain
Docker
```

and the job description requires:

```text
Python
Machine Learning
SQL
AWS
Docker
FastAPI
```

The analyzer may identify:

### Matching Skills

```text
Python
Machine Learning
SQL
Docker
```

### Missing Skills

```text
AWS
FastAPI
```

The suggestion stage can then recommend practical ways to improve those skill gaps.

---

## 🧠 State

The LangGraph workflow uses shared state to pass information between nodes.

The state contains information such as:

```text
resume_text
job_description
resume_skills
required_skills
matching_skills
missing_skills
suggestions
final_report
```

Each node reads the information it needs and returns the information it produces.

---

## 🎯 Project Goal

The goal of this project is to build a practical AI-based resume analysis system while learning how to design **sequential LangGraph workflows**.

The project focuses on separating:

```text
Document Processing
        ↓
LLM Analysis
        ↓
Skill Matching
        ↓
Recommendations
        ↓
Final Report
```

---

## 🔮 Future Improvements

Possible future improvements include:

- 📊 Overall resume-job match percentage
- 🔍 More advanced ATS analysis
- 🧾 Resume formatting analysis
- 📌 Experience and education matching
- 🌐 Job-search integration
- 📚 Learning-resource recommendations for missing skills
- 💾 Resume history and comparison
- 👤 User profiles and preferences
- 🔄 Conditional LangGraph workflows
- 🧠 RAG-based resume analysis
- 🤖 Agentic workflow with external tools
- 🔌 MCP tool integration

---

## ⚠️ Limitations

The quality of the analysis depends on:

- The quality of the uploaded resume
- The completeness of the job description
- The LLM's interpretation of skills
- Text extraction quality for uploaded documents

Scanned/image-only documents may require OCR for reliable extraction.

The ATS score should be treated as an **AI-generated estimate**, not an actual score used by a company's recruitment system.

---

## 🔒 Security

Never commit API keys to GitHub.

Your `.gitignore` should include:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## 👨‍💻 Author

**Akash Goswami**

AI & Machine Learning Engineer

GitHub: [akashgoswami139](https://github.com/akashgoswami139)

---

## ⭐ Future Vision

This project is being developed as a foundation for building more advanced **AI workflow and agentic applications** using LangGraph, tools, RAG, and MCP.

---

## 📜 License

This project is intended for educational and portfolio purposes.