import json
import re
import os
import sys
from dotenv import load_dotenv
load_dotenv()

util_path = os.getenv("UTIL_PATH")

if util_path:
    sys.path.append(util_path)
else:
    print("Warning: PROJECT_PATH is not set in the .env file.")

from flask import Flask, request, jsonify
import requests
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_setup import get_llm


app = Flask(__name__)

EXPRESS_BACKEND_URL = "http://localhost:3000/api/github/issues"  # Replace with actual backend URL

def generate_test_cases(patch_data):
    """Generates test cases from the patch using an LLM."""
    prompt = PromptTemplate.from_template("""
    You are an expert software tester. Given the following patch changes from a GitHub pull request:
    
    {patch_data}
    
    Generate detailed test cases for these changes. Ensure the test cases cover different scenarios, including:
    - Basic functionality
    - Edge cases
    - Regression tests
    - Error handling
    
    Provide the response as valid JSON in the following format:
    {{
        "response_code": 200,
        "test_cases": [
            {{ "test_name": "Test case 1 description", "steps": "Step-by-step instructions", "expected_output": "Expected behavior" }},
            {{ "test_name": "Test case 2 description", "steps": "Step-by-step instructions", "expected_output": "Expected behavior" }}
        ]
    }}
    """)

    llm = get_llm()
    chain = prompt | llm

    try:
        response = chain.invoke({"patch_data": patch_data})
        response_content = response.content.strip()

        # Remove any markdown formatting
        response_content = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', response_content, flags=re.DOTALL)
        response_content = response_content.strip()

        # Parse the JSON response
        return json.loads(response_content)
    except Exception as e:
        print(f"Error generating test cases: {e}")
        return {"response_code": 500, "error": "Failed to generate test cases", "details": str(e)}

@app.route("/generate-test-cases", methods=["GET"])
def fetch_and_generate_tests():
    try:
        response = requests.get(EXPRESS_BACKEND_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Express backend"}), 500

        issue_data = response.json()
        patches = [file.get("patch", "") for file in issue_data.get("files", []) if "patch" in file]
        patch_data = "\n".join(patches)
        
        test_cases = generate_test_cases(patch_data)
        return jsonify(test_cases)
    except requests.RequestException as e:
        return jsonify({"error": "Request to Express backend failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
