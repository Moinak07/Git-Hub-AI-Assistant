# AI Assistant Project

## Overview
This project is an AI-powered assistant designed to automate code review, generate test cases, and interact with GitHub repositories. It integrates Python (Flask, LangChain, Gemini API) and Node.js (Express) microservices to provide an end-to-end solution for analyzing GitHub issues and pull requests, suggesting code fixes, and generating relevant test cases.

---

## Project Structure

```
AI_ASSISTANT/
│
├── client/
│   └── index.js                # (Frontend entry, placeholder)
│
├── langchain_framework/        # Python microservice for LLM-powered logic
│   ├── .env                    # Environment variables (Gemini API, etc.)
│   ├── config.py               # Gemini API config
│   ├── chains/
│   │   ├── code_review.py      # Flask app: analyzes GitHub issues and suggests code fixes
│   │   └── test_generation.py  # Flask app: generates test cases from PR patches
│   ├── utils/
│   │   └── langchain_setup.py  # Loads Gemini LLM for LangChain
│   ├── requirement.txt         # Python dependencies
│   └── README.md               # (Legacy/readme for this module)
│
├── server/                     # Node.js/Express backend for GitHub API integration
│   ├── .env                    # GitHub token, etc.
│   ├── index.js                # Express server entry
│   ├── controllers/
│   │   └── githubController.js # Handles GitHub API logic, PR/issue fetching, test case receipt
│   ├── routes/
│   │   └── githubRoutes.js     # API routes for issues, PRs, test-cases
│   └── utils/
│       ├── ApiError.js         # Standardized API error handling
│       ├── ApiResponse.js      # Standardized API response format
│       └── asyncHandler.js     # Async error handling middleware
│
└── .gitignore
```

---

## Main Features

### 1. GitHub Integration (Node.js/Express)
- Fetches issues and pull requests from a target GitHub repository.
- Sends issue/PR data to the Python microservice for analysis.
- Receives and logs AI-generated test cases.

### 2. Code Review & Fix Suggestions (Python/Flask + LangChain)
- Analyzes GitHub issues and generates structured JSON responses with code fixes (HTML/CSS, etc.).
- Uses Google Gemini LLM via LangChain for intelligent suggestions.

### 3. Automated Test Case Generation (Python/Flask + LangChain)
- Consumes PR patch data and generates relevant unit test cases.
- Converts LLM output into structured JSON and sends it back to the Node.js backend.

---

## Setup & Usage

### Prerequisites
- Node.js (v18+ recommended)
- Python (3.9+ recommended)
- GitHub API Token (for server/.env)
- Google Gemini API Key (for langchain_framework/.env)

### 1. Install Dependencies

#### Python
```
cd langchain_framework
pip install -r requirement.txt
```

#### Node.js
```
cd server
npm install
```

### 2. Environment Variables
- `server/.env`: Set `GITHUB_TOKEN` for GitHub API access.
- `langchain_framework/.env`: Set `GEMINI_API_KEY` for Gemini LLM access.

### 3. Running the Services

#### Start Python Flask Apps
```
cd langchain_framework/chains
# For code review
python code_review.py
# For test generation
python test_generation.py
```

#### Start Node.js Express Server
```
cd server
node index.js
```

---

## API Endpoints

### Node.js (Express)
- `GET /api/github/issues` — Fetches first issue from GitHub
- `GET /api/github/pulls` — Fetches first pull request and patch data
- `POST /api/github/test-cases` — Receives generated test cases from Python service

### Python (Flask)
- `GET /analyze-issues` — Analyzes a GitHub issue and returns a code fix (JSON)
- `GET /generate-test-cases` — Generates test cases for a PR patch and sends them to Node.js

---

## Technologies Used
- **Python**: Flask, LangChain, Google Gemini API
- **JavaScript/Node.js**: Express, Axios
- **GitHub REST API**




