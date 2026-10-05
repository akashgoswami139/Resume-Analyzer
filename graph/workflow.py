from langgraph.graph import StateGraph, START, END
from graph.state import State
from graph.nodes import suggestion_node, find_skills_node , final_output_node, resume_required_skill_node

work_graph = StateGraph(State)

work_graph.add_node("find_skills", find_skills_node)
work_graph.add_node("required_skills", resume_required_skill_node)
work_graph.add_node("suggestion", suggestion_node)
work_graph.add_node("output", final_output_node)


#connect edge (sequential one by one )


work_graph.add_edge(START, "required_skills")
work_graph.add_edge("required_skills", "find_skills")
work_graph.add_edge("find_skills", "suggestion")
work_graph.add_edge("suggestion", "output")
work_graph.add_edge("output",END)

app_graph = work_graph.compile()