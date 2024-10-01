# AI PR Review GitHub Action

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This GitHub Action uses AI to summarize Pull Request changes and review the code based on a set of user-defined standards. It leverages OpenAI's GPT models to provide insightful code reviews and can be customized to fit your project's specific needs.

## Features

- Automated code review for Pull Requests
- Customizable review standards
- Support for both OpenAI and Azure OpenAI
- Generates summaries of code changes
- Provides actionable feedback categorized as must-have and nice-to-have changes
- Generates Claude 3.5 Sonnet-compatible prompts for must-have fixes

## Installation and Setup

Follow these steps to install and configure the AI PR Review GitHub Action:

1. **Create the necessary directories and files:**

   Create the following directory structure in your repository:

   ```
   .github/
   ├── workflows/
   │   └── ai-pr-review.yml
   ├── scripts/
   │   └── ai_pr_review.py
   └── config/
       ├── review_standards.json
       └── prompts.json
   ```

2. **Copy the provided code:**

   Copy the contents of each file provided in this repository into their respective files in your repository.

3. **Set up GitHub Secrets:**

   - Go to your GitHub repository's settings.
   - Navigate to "Secrets and variables" > "Actions" in the left sidebar.
   - Click on "New repository secret".
   - Add a secret named `OPENAI_API_KEY` with your OpenAI API key as the value.
   - (Optional) If you're using Azure OpenAI, add a secret named `OPENAI_API_ENDPOINT` with your Azure OpenAI endpoint URL.

4. **Customize the review standards:**

   Edit the `.github/config/review_standards.json` file to include your specific coding standards and best practices.

5. **Customize the AI prompts (optional):**

   Edit the `.github/config/prompts.json` file to customize the AI's behavior and focus areas.

6. **Commit and push the changes:**

   Add, commit, and push the new files to your repository:

   ```
   git add .github
   git commit -m "Add AI PR Review GitHub Action"
   git push
   ```

7. **Enable GitHub Actions:**

   If you haven't already, make sure GitHub Actions are enabled for your repository:
   - Go to your repository's settings.
   - Navigate to "Actions" > "General" in the left sidebar.
   - Ensure that "Allow all actions and reusable workflows" is selected.

## Usage

Once installed and configured, the AI PR Review Action will automatically run whenever a pull request is opened or updated in your repository. It will:

1. Summarize the changes in the pull request.
2. Review the code based on the standards defined in `review_standards.json`.
3. Post a comment on the pull request with the summary and review.

## Customization

You can customize the behavior of the AI PR Review Action by:

- Modifying the standards in `.github/config/review_standards.json`.
- Selecting different AI models for summarization and code review by updating the `summary_model` and `review_model` fields in `review_standards.json`. Available models include:
  - `gpt-4o`: GPT-4 Optimized - The most advanced and capable model.
  - `gpt-4o-mini`: GPT-4 Optimized Mini - A smaller, faster version of GPT-4 Optimized.
  - `gpt-4-turbo`: GPT-4 Turbo - A faster version of GPT-4 with improved capabilities.
  - `gpt-4`: GPT-4 - Highly capable but may be slower than the Turbo version.
  - `gpt-3.5-turbo`: GPT-3.5 Turbo - Fast and cost-effective, good for most tasks.
- Customizing the prompts used for the AI review by editing the `.github/config/prompts.json` file. This file contains:
  - `system_role`: A detailed description of the AI reviewer's role, objectives, and responsibilities.
  - `summarize_prompt`: The prompt used to summarize changes.
  - `review_prompt`: A comprehensive prompt for reviewing code changes, including specific criteria and feedback structure.
- Adjusting the Python script in `.github/scripts/ai_pr_review.py` to change how the summary and review are generated or presented.
- Updating the GitHub Action workflow in `.github/workflows/ai-pr-review.yml` to add additional steps or change the trigger conditions.

### Customizing the AI Prompts

The `prompts.json` file allows you to fine-tune the AI's behavior:

- The `system_role` sets the overall context and objectives for the AI reviewer.
- The `summarize_prompt` guides the AI in creating a concise summary of the changes.
- The `review_prompt` provides detailed instructions for the code review process, including specific criteria to consider and how to structure the feedback.

By customizing these prompts, you can adjust the focus areas, tone, and depth of the AI's review to best suit your project's needs.

## Azure OpenAI Support

This action supports both standard OpenAI and Azure OpenAI. To use Azure OpenAI:

1. Set the `OPENAI_API_ENDPOINT` secret in your repository with your Azure OpenAI endpoint URL.
2. Ensure your `OPENAI_API_KEY` secret contains the appropriate API key for Azure OpenAI.
3. Update the model names in `review_standards.json` to match your Azure OpenAI deployment names.

The action will automatically use Azure OpenAI if an `OPENAI_API_ENDPOINT` is provided.

## Troubleshooting

If you encounter any issues:

1. Check that all files are in the correct locations and have the correct content.
2. Ensure that the `OPENAI_API_KEY` secret is set correctly in your repository settings.
3. If using Azure OpenAI, verify that the `OPENAI_API_ENDPOINT` secret is set correctly.
4. Verify that GitHub Actions are enabled for your repository.
5. Check the Action logs in the "Actions" tab of your repository for any error messages.
6. Ensure the model names in `review_standards.json` match the available models for your OpenAI or Azure OpenAI account.
7. If you've customized the `prompts.json` file, make sure it's valid JSON and doesn't contain any syntax errors.

## Contributing

Contributions to improve the AI PR Review Action are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run the tests (`python -m unittest .github/scripts/test_ai_pr_review.py`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT models
- The GitHub Actions team for their excellent documentation and examples
