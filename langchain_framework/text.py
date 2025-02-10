import requests

PR_FILES_URL = "https://api.github.com/repos/octocat/Hello-World/pulls/42/files"
response = requests.get(PR_FILES_URL)

if response.status_code == 200:
    print("Success! Here's the data:")
    print(response.json())
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")
