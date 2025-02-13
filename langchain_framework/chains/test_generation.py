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
import json
from flask import Flask, request, jsonify
import requests
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_setup import get_llm  

# Load environment variables
load_dotenv()
util_path = os.getenv("UTIL_PATH")

if util_path:
    sys.path.append(util_path)
else:
    print("Warning: UTIL_PATH is not set in the .env file.")

app = Flask(__name__)

EXPRESS_BACKEND_URL = "http://localhost:3000/api/github/pulls"
EXPRESS_BACKEND_URL1 = "http://localhost:3000/api/github/test-cases"

def generate_test_cases(patch_data):
    """Generates test cases from the patch using an LLM."""
    print("🔹 Received Patch Data:", patch_data)

    prompt = PromptTemplate.from_template("""
    You are an expert software tester. Given the following **code patch** from a GitHub pull request:

    ```
    {patch_data}
    ```

    - Analyze **only the modified lines of code** in the patch.
    - Generate relevant test cases that **validate the changes**.
    - Ensure coverage of:
        - Functional correctness of modified code.
        - Edge cases and regression tests for affected areas.
        - Styling, UI behavior, or logic changes if applicable.

    Provide test cases in the following format:
    ```
    test_name: Describe what is being tested
    unit_test_code: Generate the Unit test code to test the change
    expected_output: Expected behavior after the change
    ```
    """)

    llm = get_llm()
    chain = prompt | llm

    try:
        response = chain.invoke({"patch_data": patch_data})
        response_content = response.content.strip()

        # Remove Markdown formatting if present
        response_content = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', response_content, flags=re.DOTALL).strip()

        print("\n🔹 Raw LLM Response:\n", response_content)

        # Convert the test cases into structured JSON
        structured_test_cases = jsonify_test_cases(response_content)

        return structured_test_cases

    except Exception as e:
        print(f"\n❌ Error generating test cases: {e}")
        return {"response_code": 500, "error": "Failed to generate test cases", "details": str(e)}

def jsonify_test_cases(test_cases_text):
    """Uses an LLM to structure test cases into valid JSON."""
    print("\n🔹 Converting Test Cases to JSON...")

    prompt = PromptTemplate.from_template("""
    Convert the following test case descriptions into a structured JSON format:

    ```
    {test_cases_text}
    ```

    Output a valid JSON array with the following structure:
    [
        {{
            "test_name": "Descriptive name of the test",
            "unit_test_code": "Code snippet for the test case",
            "expected_output": "Expected result when test runs"
        }}
    ]
    """)

    llm = get_llm()
    chain = prompt | llm

    try:
        response = chain.invoke({"test_cases_text": test_cases_text})
        json_response = response.content.strip()

        # Ensure valid JSON format
        json_response = re.sub(r'```(?:json)?\n?(.*?)\n?```', r'\1', json_response, flags=re.DOTALL).strip()
        structured_data = json.loads(json_response)

        print("\n🔹 Structured JSON Output:\n", json.dumps(structured_data, indent=4))

        return structured_data

    except Exception as e:
        print(f"\n❌ Error structuring test cases into JSON: {e}")
        return {"response_code": 500, "error": "Failed to format test cases", "details": str(e)}

@app.route("/generate-test-cases", methods=["GET"])
def fetch_and_generate_tests():
    """Fetches PR patch data from Express backend, generates test cases, and sends them back."""
    try:
        response = requests.get(EXPRESS_BACKEND_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Express backend"}), 500

        try:
            issue_data = response.json()
        except ValueError:
            return jsonify({"error": "Invalid JSON response from Express backend"}), 500

        # Extract patches from PR files
        files = issue_data.get("data", {}).get("files", [])
        patches = [file.get("patch", "") for file in files if "patch" in file]
        patch_data = "\n".join(patches)

        if not patch_data:
            return jsonify({"error": "No valid patch data found"}), 400

        # Generate test cases
        test_cases = generate_test_cases(patch_data)

        # Debugging: Log what is being sent
        print("\n🔹 Sending Test Cases to Express Backend:\n", json.dumps(test_cases, indent=4))

        express_response = requests.post(
            EXPRESS_BACKEND_URL1,
            json={"test_cases": test_cases},
            headers={"Content-Type": "application/json"}
        )

        if express_response.status_code != 200:
            return jsonify({"error": "Failed to send test cases to Express backend"}), 500

        return jsonify({"message": "Test cases sent successfully"})

    except requests.RequestException as e:
        return jsonify({"error": "Request to Express backend failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
