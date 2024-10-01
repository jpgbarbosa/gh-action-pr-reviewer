import os
import sys
import json
from openai import OpenAI
from github import Github, GithubException

def load_config():
    try:
        with open('.github/config/review_standards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: review_standards.json not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in review_standards.json.")
        sys.exit(1)

def load_prompts():
    try:
        with open('.github/config/prompts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "system_role": "You are a helpful assistant that reviews pull requests code and its changes.",
            "summarize_prompt": "Summarize the following code changes:\n\n{diff}",
            "review_prompt": (
                "Review the following code changes and give them a note from 0 to 5, "
                "based on these standards:\n{standards}\n\n"
                "Code changes:\n{diff}\n"
                "At the end provide an overall review."
            )
        }
    except json.JSONDecodeError:
        print("Error: Invalid JSON in prompts.json.")
        sys.exit(1)

def get_pr_diff(repo, pr_number):
    try:
        pr = repo.get_pull(pr_number)
        return pr.get_files()
    except GithubException as e:
        print(f"Error fetching PR diff: {str(e)}")
        sys.exit(1)

def ai_request(prompt, model):
    api_key = os.getenv("OPENAI_API_KEY")
    api_endpoint = os.getenv("OPENAI_API_ENDPOINT")
    prompts = load_prompts()

    if api_endpoint:
        client = OpenAI(api_key=api_key, base_url=api_endpoint)
    else:
        client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompts["system_role"]},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"Error when calling OpenAI API: {str(e)}"
        if api_endpoint:
            error_message += f"\nCustom API endpoint used: {api_endpoint}"
        print(error_message)
        sys.exit(1)

def summarize_changes(diff, model):
    prompts = load_prompts()
    prompt = prompts["summarize_prompt"].format(diff=diff)
    return ai_request(prompt, model)

def review_code(diff, standards, model):
    prompts = load_prompts()
    prompt = prompts["review_prompt"].format(standards=json.dumps(standards), diff=diff)
    return ai_request(prompt, model)

def get_pr_number():
    pr_number = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")
    if pr_number:
        return int(pr_number)

    github_ref = os.getenv("GITHUB_REF")
    if github_ref and github_ref.startswith("refs/pull/") and github_ref.endswith("/merge"):
        return int(github_ref.split("/")[2])

    raise ValueError("Unable to determine the Pull Request number.")

def get_available_models():
    return {
        "gpt-4o": "GPT-4 Optimized",
        "gpt-4o-mini": "GPT-4 Optimized Mini",
        "gpt-4-turbo": "GPT-4 Turbo",
        "gpt-4": "GPT-4",
        "gpt-3.5-turbo": "GPT-3.5 Turbo"
    }

def validate_model(model):
    available_models = get_available_models()
    if model not in available_models:
        print(f"Warning: Model '{model}' is not in the list of known models. Using anyway.")
    return model

def main():
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    try:
        pr_number = get_pr_number()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
    except GithubException as e:
        print(f"Error connecting to GitHub: {str(e)}")
        sys.exit(1)

    config = load_config()
    files = get_pr_diff(repo, pr_number)

    diff = ""
    for file in files:
        diff += f"File: {file.filename}\n"
        diff += f"Status: {file.status}\n"
        diff += f"Changes: +{file.additions} -{file.deletions}\n"
        diff += f"Patch:\n{file.patch}\n\n"

    summary_model = validate_model(config.get('summary_model', 'gpt-4-turbo'))
    review_model = validate_model(config.get('review_model', 'gpt-4-turbo'))

    summary = summarize_changes(diff, summary_model)
    review = review_code(diff, config['standards'], review_model)

    comment = f"## AI Pull Request Review\n\n### Summary of Changes (using {summary_model})\n{summary}\n\n### Code Review (using {review_model})\n{review}"

    try:
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)
    except GithubException as e:
        print(f"Error creating PR comment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
