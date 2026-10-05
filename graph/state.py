from typing import TypedDict



class State(TypedDict):
    resume_text: str
    job_description: str

    resume_skills: list
    required_skills: list

    matching_skills: list
    missing_skills: list

    suggestions: str
    final_report: str