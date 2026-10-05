import json
import re

from llm.model import model
from graph.state import State


def _parse_json_response(content):
    """
    Convert an LLM response containing JSON text into a Python dictionary.

    Handles:
    - Normal JSON strings
    - JSON wrapped in ```json ... ```
    - Extra text before/after the JSON object
    - Already-parsed dictionaries
    """

    if isinstance(content, dict):
        return content

    if not isinstance(content, str):
        raise TypeError("LLM response content must be a string or dictionary.")

    content = content.strip()

    # Remove markdown code fences if present.
    content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"^```\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    content = content.strip()

    # First attempt: parse the complete response.
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Second attempt: extract the first JSON object from the response.
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1 or start >= end:
        raise ValueError("Could not find a valid JSON object in the LLM response.")

    json_text = content[start : end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON.\nResponse:\n{content}"
        ) from e


def resume_required_skill_node(state: State):
    """Extract skills from the resume and required skills from the job description."""

    prompt = f"""
You are a skill differentiation assistant.

Analyze the candidate's resume and the job description.

Resume content:
{state["resume_text"]}

Job description:
{state["job_description"]}

Identify:

1. Skills mentioned in the candidate's resume.
2. Skills required by the job description.

Normalize similar skill names where appropriate.

Return ONLY valid JSON.

Required format:
{{
    "resume_skills": ["skill1", "skill2"],
    "required_skills": ["skill1", "skill2"]
}}
"""

    response = model.invoke(prompt)

    result = _parse_json_response(response.content)

    return {
        "resume_skills": result.get("resume_skills", []),
        "required_skills": result.get("required_skills", []),
    }


def find_skills_node(state: State):
    """Find matching and missing skills."""

    prompt = f"""
You are a skill-matching assistant.

Compare the candidate's skills with the skills required for the job.

Candidate skills:
{state["resume_skills"]}

Required job skills:
{state["required_skills"]}

Tasks:

1. Identify the skills that appear in both lists or are clearly equivalent.
2. Identify the required skills that are missing from the candidate's skills.

Normalize equivalent skill names where appropriate.

Return ONLY valid JSON.

Required format:
{{
    "matching_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"]
}}
"""

    response = model.invoke(prompt)

    result = _parse_json_response(response.content)

    return {
        "matching_skills": result.get("matching_skills", []),
        "missing_skills": result.get("missing_skills", []),
    }


def suggestion_node(state: State):
    """Generate suggestions for improving the candidate's chances."""

    prompt = f"""
You are a career suggestion assistant.

Analyze the candidate's skills against the required skills for the job.

Candidate skills:
{state["resume_skills"]}

Required skills:
{state["required_skills"]}

Matching skills:
{state["matching_skills"]}

Missing skills:
{state["missing_skills"]}

Provide practical and specific suggestions based on the skill gaps.

Include:

- What the candidate should improve.
- What skills the candidate should learn or strengthen.
- What projects or practical work could improve their chances.
- What the candidate should improve on their resume.
- An estimated ATS compatibility score out of 100 based only on the available skill information.

Do not invent experience or qualifications.

Return the suggestions as plain text.
"""

    response = model.invoke(prompt)

    result = response.content

    if isinstance(result, str):
        result = result.strip()
    else:
        result = str(result).strip()

    return {
        "suggestions": result
    }


def final_output_node(state: State):
    """Generate the final professional report for the user."""

    prompt = f"""
You are a professional resume and career analysis assistant.

Create the final report using the information below.

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

- Include the important matching skills.
- Include the important missing skills.
- Include the ATS score if it is available in the suggestions.
- Include all useful suggestions.
- Clearly explain the candidate's strengths.
- Clearly explain the candidate's skill gaps.
- Provide practical improvement advice.
- Add a separate heading called "Expert Advice".
- Do not invent candidate information.
- Do not remove important information.
- Keep the report focused on the specific job.
"""

    response = model.invoke(prompt)

    result = response.content

    if isinstance(result, str):
        result = result.strip()
    else:
        result = str(result).strip()

    return {
        "final_report": result
    }