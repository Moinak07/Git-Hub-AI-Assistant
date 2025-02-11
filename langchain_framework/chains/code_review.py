import sys
import os

from dotenv import load_dotenv
load_dotenv()

util_path = os.getenv("UTIL_PATH")

if util_path:
    sys.path.append(util_path)
else:
    print("Warning: PROJECT_PATH is not set in the .env file.")
import json
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_setup import get_llm

# Add the utils directory to the Python path

from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

EXPRESS_BACKEND_URL = "http://localhost:3000/api/github/issues"
 # Replace with your actual Express backend URL


def analyze_github_issue(issue_data):
    """Analyzes GitHub issue data and returns a structured JSON response with a code fix."""
    # Extract issue data from the nested structure
    if isinstance(issue_data, dict) and 'data' in issue_data:
        issue_data = issue_data['data']
    
    issue_title = issue_data.get("title", "No title provided")
    issue_body = issue_data.get("body", "No description provided")
    issue_labels = [label.get('name', label) if isinstance(label, dict) else label 
                   for label in issue_data.get("labels", [])]
    issue_labels_str = ", ".join(issue_labels) or "No labels"
    issue_priority = issue_data.get("priority", "Not specified")

    prompt = PromptTemplate.from_template("""
    You are an expert software engineer reviewing a GitHub issue. Based on the following issue details:

    - **Title**: {issue_title}
    - **Description**: {issue_body}
    - **Labels**: {issue_labels}

    Provide actual code to fix this issue. Since this is about a logo fix, provide the HTML and CSS code needed.
    Return your response as a valid JSON object with the following structure:
    {{
        "response_code": 200,
        "issue_title": "Logo fix implementation",
        "code_fix": {{
            "html": "the HTML code for the logo",
            "css": "the CSS code for the logo styling",
            "comments": "implementation notes"
        }}
    }}

    Keep the response as a clean JSON without any markdown formatting or code blocks.
    """)

    llm = get_llm()
    chain = prompt | llm

    try:
        response = chain.invoke({
            "issue_title": issue_title,
            "issue_body": issue_body,
            "issue_labels": issue_labels_str,
            "issue_priority": issue_priority
        })

        response_content = response.content.strip()
        
        # Remove any markdown code block markers if present
        response_content = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', 
                                response_content, flags=re.DOTALL)
        
        # Clean up any remaining whitespace and newlines
        response_content = response_content.strip()
        
        # Parse the JSON response
        try:
            response_json = json.loads(response_content)
            
            # Ensure the response has the expected structure
            if not isinstance(response_json, dict):
                raise ValueError("Response is not a dictionary")
                
            # Validate required fields
            required_fields = ["response_code", "issue_title", "code_fix"]
            for field in required_fields:
                if field not in response_json:
                    raise ValueError(f"Missing required field: {field}")
                    
            return response_json
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return {
                "response_code": 500,
                "error": "Invalid JSON structure in LLM response",
                "details": str(e)
            }
            
    except Exception as e:
        print(f"Error during analysis: {e}")
        return {
            "response_code": 500,
            "error": "Failed to analyze issue",
            "details": str(e)
        }

@app.route("/analyze-issues", methods=["GET"])
def fetch_and_analyze_issues():
    try:
        response = requests.get(EXPRESS_BACKEND_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Express backend"}), 500

        # The response is a single issue (dictionary), not a list
        issue_data = response.json()
        print("Issue Data:", issue_data)  # Debug print

        # Analyze the single issue
        analyzed_issue = analyze_github_issue(issue_data)
        return jsonify(analyzed_issue)
    except requests.RequestException as e:
        return jsonify({"error": "Request to Express backend failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)