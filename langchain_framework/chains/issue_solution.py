import sys
sys.path.append("C:/Users/rohit/langchain_framework/utils") 

import json
from langchain.prompts import PromptTemplate
from langchain_setup import get_llm

def generate_solution(issue_data):
    """Generates a possible solution for a GitHub issue."""
    issue_title = issue_data.get("title", "No title provided")
    issue_description = issue_data.get("description", "No description provided")

    prompt = PromptTemplate.from_template("""
    You are a senior software engineer. Analyze the following GitHub issue:

    - **Title**: {issue_title}
    - **Description**: {issue_description}

    Provide:
    1. A clear understanding of the issue.
    2. Possible solutions.
    3. Steps for implementation.
    """)

    llm = get_llm()
    chain = prompt | llm 

    return chain.invoke({"issue_title": issue_title, "issue_description": issue_description})

if __name__ == "__main__":
    with open("../issue_data.json") as f:
        issue_data = json.load(f)
    print(generate_solution(issue_data))
