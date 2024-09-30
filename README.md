Here's the updated `README.md` with the name "O1" and without the FloatGPT branding:

```markdown
# O1 - Qwen AI Assistant

O1 is a Streamlit application powered by the Qwen AI model using the Ollama client. This app allows users to upload files (PDF and text), input their queries, and interact with the AI in a chat-like interface. The AI agent refines the prompt, creates a step-by-step plan, drafts a system prompt, and finally executes the task based on the user's input and uploaded file contents.

## Features

- **File Upload**: Users can upload `.pdf` and `.txt` files, which will be processed and used by the AI to assist in answering queries.
- **Customizable System Prompt**: Users can modify the system prompt used by the AI, allowing for customized interactions.
- **AI-Assisted Chat**: The app enables a chat-like interaction where the AI refines the user's query, creates an execution plan, and responds accordingly.
- **Step-by-Step Execution**: The AI performs tasks in three steps: refining the prompt, generating a step-by-step plan, and drafting a system prompt before executing the final task.

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Ollama Client](https://ollama.ai/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/O1.git
   cd O1
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install streamlit ollama
   ```

4. Ensure that the [Ollama client](https://ollama.ai/) is installed and running on your local machine. You can modify the `host` value in the code if needed.

## Usage

1. Start the Streamlit app:

   ```bash
   streamlit run agent2.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Interact with the AI by uploading files and typing messages in the chat input.

## How It Works

- **File Processing**: Upload `.pdf` or `.txt` files. The content is extracted and used as part of the prompt.
- **Custom System Prompt**: Modify the system prompt in the sidebar for different interactions.
- **AI Execution Steps**:
  1. **Refining the Prompt**: The AI refines the user's query based on the uploaded files and input.
  2. **Step-by-Step Plan**: A step-by-step plan is generated for the task.
  3. **System Prompt**: A system prompt is prepared and the task is executed based on the refined input.

## Future Features

- **Web Search Integration** (Coming Soon)
- **Code Interpreter** (Coming Soon)
- **Document Analyzer** (Coming Soon)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Feel free to modify any sections as needed based on your actual project details!
