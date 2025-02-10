import os
import json
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Initialize GitHub and Gemini configurations
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize LangChain LLM
llm = ChatGoogleGenerativeAI(model="gemini-1", temperature=0.2, google_api_key=GEMINI_API_KEY)

def extract_github_info(file_path="C:\\Users\\rohit\\OneDrive\\Desktop\\AI Assistant\\langchain_framework\\github_issue.json"):
    """Extract OWNER, REPO, PR_NUMBER, and PR_FILES_URL from the given JSON file."""
    with open(file_path, "r") as file:
        data = json.load(file)
    
    repository_url = data.get("repository_url", "")
    url_parts = repository_url.split("/")
    owner = url_parts[-2]
    repo = url_parts[-1]
    pr_number = data.get("number", 0)
    pr_files_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    return owner, repo, pr_number, pr_files_url

def fetch_pr_files(pr_files_url):
    """Fetch the changed files from the GitHub PR."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(pr_files_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching PR files: {response.status_code}, {response.text}")
        return []

def extract_code_from_pr(files):
    """Extract code snippets from Python files in the PR."""
    code_snippets = [file["patch"] for file in files if file["filename"].endswith(".py")]
    return "\n".join(code_snippets)

def generate_test_cases(code):
    """Generate unittest test cases for the given code using Gemini AI."""
    prompt = f"""
    Generate Python `unittest` test cases for the following code:

    Code:
    ```python
    {code}
    ```

    Requirements:
    - Test core functionality
    - Cover edge cases
    - Handle errors and exceptions
    """
    response = llm.invoke(prompt)
    return response.content if response else "No test cases generated."

def main():
    """Main function to extract info, fetch code, and generate test cases."""
    owner, repo, pr_number, pr_files_url = extract_github_info()
    print(f"OWNER: {owner}, REPO: {repo}, PR_NUMBER: {pr_number}")

    files = fetch_pr_files(pr_files_url)
    if not files:
        print("No files found in the PR.")
        return

    code = extract_code_from_pr(files)
    if not code:
        print("No Python code found.")
        return

    print("\n🔹 Extracted Code Snippet:\n", code[:500], "...\n")
    test_cases = generate_test_cases(code)

    with open("generated_test_cases.py", "w") as file:
        file.write(test_cases)
    print("\n✅ Test cases saved in generated_test_cases.py")

if __name__ == "__main__":
    main()
