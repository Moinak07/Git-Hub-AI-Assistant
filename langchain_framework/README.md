# LangChain Framework

This repository provides a framework for analyzing GitHub issues and generating solutions using LangChain and the Gemini API.

## Prerequisites

- Python 3.10 or higher
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/langchain_framework.git
    cd langchain_framework
    ```

2. Create and activate a conda environment:

    ```sh
    conda create --name langchain_env python=3.10
    conda activate langchain_env
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Create a [`.env`](.env) file in the root directory of the project and add your Gemini API key:

    ```sh
    GEMINI_API_KEY=your_gemini_api_key
    ```

## Usage

### Analyzing GitHub Issues

1. Place your GitHub issue data in a file named [`github_issue.json`](github_issue.json) in the root directory. The file should follow the structure provided in the example.

2. Run the [`chains/code_review.py`](chains/code_review.py) script to analyze the issue and get a code fix:

    ```sh
    python chains/code_review.py
    ```

### Generating Solutions for GitHub Issues

1. Place your GitHub issue data in a file named [`issue_data.json`](issue_data.json) in the root directory. The file should follow the structure provided in the example.

2. Run the [`chains/issue_solution.py`](chains/issue_solution.py) script to generate a solution for the issue:

    ```sh
    python chains/issue_solution.py
    ```

## Project Structure

```
langchain_framework/
├── chains/
│   ├── code_review.py
│   ├── issue_solution.py
│   ├── test_generation.py
├── utils/
│   ├── langchain_setup.py
├── config.py
├── github_issue.json
├── issue_data.json
├── parallel_execution.py
├── requirements.txt
└── .env
```

- [`chains`](chains): Contains scripts for analyzing and generating solutions for GitHub issues.
- [`utils`](utils): Contains utility scripts, including the LangChain setup.
- [`config.py`](config.py): Configuration file for setting up the Gemini API.
- [`github_issue.json`](github_issue.json): Example GitHub issue data file.
- [`issue_data.json`](issue_data.json): Example GitHub issue data file for solution generation.
- `requirements.txt`: List of required Python packages.
- [`.env`](.env): Environment variables file.

## License

This project is licensed under the MIT License.