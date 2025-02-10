import sys
sys.path.append("C:/Users/rohit/OneDrive/Desktop/AI Assistant/langchain_framework/utils")
import json
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_setup import get_llm

# Add the utils directory to the Python path


def analyze_github_issue(issue_data):
    """Analyzes GitHub issue data and returns a structured JSON response with a code fix."""

    # Extract issue details
    issue_title = issue_data.get("title", "No title provided")
    issue_body = issue_data.get("body", "No description provided")
    issue_labels = ", ".join(label["name"] for label in issue_data.get("labels", [])) or "No labels"
    issue_priority = issue_data.get("priority", "Not specified")

    # Define the prompt template
    prompt = PromptTemplate.from_template("""
    You are an expert software engineer. Carefully analyze the following GitHub Issue step by step:

    - **Title**: {issue_title}
    - **Description**: {issue_body}
    - **Labels**: {issue_labels}
    - **Priority**: {issue_priority}

    **Task**: Provide a code fix to mitigate the issue described above. Ensure the code is complete, functional, and well-formatted.

    **Output only the JSON response containing the required code fix.**  
    Do not include any explanations, only return valid JSON.

    Example format:
    {{
        "response_code": 200,
        "issue_title": "{issue_title}",
        "code_fix": "```python\\n<Your fixed code here>\\n```"
    }}

    **Important**: Your response must be valid JSON and must not contain any additional text or explanations.
    """)

    # Initialize the LLM and chain
    llm = get_llm()
    chain = prompt | llm

    # Invoke the chain with issue details
    response = chain.invoke({
        "issue_title": issue_title,
        "issue_body": issue_body,
        "issue_labels": issue_labels,
        "issue_priority": issue_priority
    })

    # Preprocess the response to extract valid JSON
    response_content = response.content.strip()

    # Try to extract JSON from the response using regex (in case the LLM adds extra text)
    json_match = re.search(r"\{.*\}", response_content, re.DOTALL)
    if json_match:
        response_content = json_match.group(0)

    # Ensure response is valid JSON
    try:
        response_json = json.loads(response_content)
    except json.JSONDecodeError as e:
        print("Error: Received invalid JSON from the LLM response.")
        print("Raw Response:", response_content)
        print("JSONDecodeError:", str(e))
        response_json = {"response_code": 500, "error": "Invalid JSON received from LLM"}

    return json.dumps(response_json, indent=4)


if __name__ == "__main__":
    try:
        # Load GitHub issue data from a JSON file
        with open("../github_issue.json") as f:
            issue_data = json.load(f)

        # Analyze the issue and print the response
        print(analyze_github_issue(issue_data))
    except FileNotFoundError:
        print("Error: github_issue.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in github_issue.json.")