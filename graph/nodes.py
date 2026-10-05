from pydantic import BaseModel, Field

from llm.model import model
from graph.state import State



class SkillExtraction(BaseModel):
    resume_skills: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)


class SkillComparison(BaseModel):
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)



# Node 1: Extract resume and job skills


def resume_required_skill_node(state: State):
    """Extract skills from the resume and required skills from the job description."""

    prompt = f"""
You are a skill differentiation assistant.

Analyze the candidate's resume and the job description.

Resume:
{state["resume_text"]}

Job Description:
{state["job_description"]}

Identify:

1. Skills mentioned in the candidate's resume.
2. Skills required by the job description.

Normalize similar skill names where appropriate.
Do not invent skills that are not present.
"""

    structured_model = model.with_structured_output(SkillExtraction)

    result = structured_model.invoke(prompt)

    return {
        "resume_skills": result.resume_skills,
        "required_skills": result.required_skills,
    }



# Node 2: Find matching and missing skills

def find_skills_node(state: State):
    """Compare resume skills with required job skills."""

    prompt = f"""
You are a skill-matching assistant.

Candidate skills:
{state["resume_skills"]}

Required job skills:
{state["required_skills"]}

Tasks:

1. Find skills that match or are clearly equivalent.
2. Find required skills that are missing from the candidate's skills.

Normalize equivalent skill names where appropriate.
Do not invent skills.
"""

    structured_model = model.with_structured_output(SkillComparison)

    result = structured_model.invoke(prompt)

    return {
        "matching_skills": result.matching_skills,
        "missing_skills": result.missing_skills,
    }


# Node 3: Generate suggestions


def suggestion_node(state: State):
    """Generate practical suggestions based on skill gaps."""

    prompt = f"""
You are a career suggestion assistant.

Analyze the candidate's skills against the job requirements.

Candidate skills:
{state["resume_skills"]}

Required skills:
{state["required_skills"]}

Matching skills:
{state["matching_skills"]}

Missing skills:
{state["missing_skills"]}

Provide practical and specific suggestions.

Include:

- What the candidate should improve.
- What skills the candidate should learn or strengthen.
- What projects could improve their chances.
- What should be improved on the resume.
- An estimated ATS compatibility score out of 100 based only on the available skill information.

Do not invent experience or qualifications.

Return the answer as plain text.
"""

    response = model.invoke(prompt)

    return {
        "suggestions": response.content.strip()
    }


# Node 4: Generate final report

def final_output_node(state: State):
    """Generate the final professional resume analysis report."""

    prompt = f"""
You are a professional resume and career analysis assistant.

Create a final report using the information below.

Resume skills:
{state["resume_skills"]}

Required job skills:
{state["required_skills"]}

Matching skills:
{state["matching_skills"]}

Missing skills:
{state["missing_skills"]}

Suggestions:
{state["suggestions"]}

Create a clear, professional, and easy-to-understand report.

Requirements:

- Include important matching skills.
- Include important missing skills.
- Include the ATS score if available in the suggestions.
- Include useful suggestions.
- Clearly explain the candidate's strengths.
- Clearly explain the candidate's skill gaps.
- Provide practical improvement advice.
- Add a separate heading called "Expert Advice".
- Do not invent candidate information.
- Keep the report focused on the specific job.

Return the report as plain text.
"""

    response = model.invoke(prompt)

    return {
        "final_report": response.content.strip()
    }
