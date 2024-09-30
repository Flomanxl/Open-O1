import streamlit as st
from ollama import Client
import time
import os
import tempfile
import PyPDF2

# Initialize the Ollama client
client = Client(host='http://127.0.0.1:11434')

# Set up the Streamlit page
st.set_page_config(page_title="Qwen O1", page_icon="🤖", layout="wide")
st.title("Qwen O1")

# Custom CSS for styling
st.markdown("""
    <style>
        .css-1aumxhk {
            background-color: #f9f9f9;
            padding: 20px;
            border-right: 1px solid #eee;
        }
        .sidebar-section-header {
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .toolbox-button {
            display: flex;
            align-items: center;
            justify-content: start;
            padding: 10px 15px;
            margin-bottom: 10px;
            background-color: #e0f7fa;
            border-radius: 8px;
            color: #00796b;
            text-decoration: none;
            font-size: 1rem;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: background-color 0.3s ease;
        }
        .toolbox-button:hover {
            background-color: #b2ebf2;
        }
        .toolbox-icon {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        .stAlert {
            background-color: #e3f2fd;
            color: #0d47a1;
            border-radius: 5px;
            padding: 10px;
        }
        .stFileUploader {
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .st-chat-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .st-chat-message-user {
            background-color: #dcf8c6;
            text-align: left;
        }
        .st-chat-message-assistant {
            background-color: #f1f0f0;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files_content" not in st.session_state:
    st.session_state.uploaded_files_content = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "Your name is Qwen. You are an AI assistant acting as an agent. "
        "First, you create a step-by-step plan and then prepare a system prompt for yourself as the agent. "
        "After that, you execute the task based on this plan."
    )

# Function to process uploaded files
def process_uploaded_file(uploaded_file):
    content = ""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

        if uploaded_file.name.endswith('.pdf'):
            with open(tmp_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text
        else:
            with open(tmp_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

    os.unlink(tmp_file_path)
    
    st.session_state.uploaded_files_content.append((uploaded_file.name, content))
    return f"File '{uploaded_file.name}' uploaded successfully."

# Sidebar for tools
with st.sidebar:
    st.markdown('<div class="sidebar-section-header">Tools</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, type=['pdf', 'txt'], key='uploader')
    if uploaded_files:
        for uploaded_file in uploaded_files:
            result = process_uploaded_file(uploaded_file)
            st.success(result)

    system_prompt_value = st.text_area("System Prompt", value=st.session_state.system_prompt, key="system_prompt_input")
    st.session_state.system_prompt = system_prompt_value

    st.markdown('<div class="sidebar-section-header">Navigation</div>', unsafe_allow_html=True)

    st.markdown('''
        <a href="#" class="toolbox-button">
            <span class="toolbox-icon">🔍</span>
            Web Search (Coming Soon)
        </a>
        <a href="#" class="toolbox-button">
            <span class="toolbox-icon">🖥️</span>
            Code Interpreter (Coming Soon)
        </a>
        <a href="#" class="toolbox-button">
            <span class="toolbox-icon">📄</span>
            Document Analyzer (Coming Soon)
        </a>
    ''', unsafe_allow_html=True)

# Display uploaded files
if st.session_state.uploaded_files_content:
    st.write("**Uploaded Files:**")
    for filename, _ in st.session_state.uploaded_files_content:
        st.write(f"- {filename}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input at the bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare the base prompt with uploaded file contents
    base_prompt = f"{st.session_state.system_prompt}\n\nOriginal User Prompt: {user_input}"
    if st.session_state.uploaded_files_content:
        base_prompt += "\n\nUploaded File Content:"
        for filename, content in st.session_state.uploaded_files_content:
            base_prompt += f"\n\nFile: {filename}\nContent: {content[:1000]}..."  # Limiting content

    # Function to make a single request to the model
    def make_request(prompt, model='qwen2.5:latest'):
        response = ""
        for chunk in client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        ):
            response += chunk['message']['content']
        return response

    # Process thinking steps
    expander = st.expander("🧠 Qwen is thinking... (Click to expand)", expanded=True)
    with expander:
        # Step 1: Refine the prompt
        st.write("**Step 1: Refining the prompt**")
        refined_prompt = make_request(f"{base_prompt}\n\nRefine this prompt to better understand and execute the task. Provide only the refined prompt. Respond in user language.")
        st.write(refined_prompt)

        # Step 2: Create a step-by-step plan
        st.write("**Step 2: Creating a step-by-step plan**")
        step_plan = make_request(f"Given the following refined prompt: {refined_prompt}\n\nCreate a concise step-by-step plan to execute this task. Provide only the steps, without explanations or examples. Respond in user language.")
        st.write(step_plan)

        # Step 3: Create a system prompt
        st.write("**Step 3: Drafting a system prompt**")
        system_prompt = make_request(f"Given the following refined prompt: {refined_prompt}\n\nDraft a system prompt that an AI assistant would use to execute this task. The system prompt should be concise and direct, without including the step-by-step plan. It should always start with 'you are an expert in...'. Respond in user language.")
        st.write(system_prompt)

    # Execute final step (task execution)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        final_prompt = (
            f"System Prompt: {system_prompt}\n\n"
            f"Refined Prompt: {refined_prompt}\n\n"
            f"Step-by-Step Plan: {step_plan}\n\n"
            f"Now execute the task based on the above information. Respond in user language."
        )
        full_response = ""
        for chunk in client.chat(
            model='qwen2.5:latest',
            messages=[{"role": "user", "content": final_prompt}],
            stream=True,
        ):
            full_response += chunk['message']['content']
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
