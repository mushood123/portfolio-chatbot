AI Resume Chatbot
=================

An interactive Gradio chat experience that answers questions about Muhammad Mushood’s background by grounding responses in his resume and professional summary. The notebook-sized footprint makes it easy to personalize and deploy as a lightweight portfolio assistant.

Contents
--------
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Running the Chatbot](#running-the-chatbot)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

Features
--------
- Loads the latest resume PDF and curated summary to keep responses accurate and consistent.
- Wraps the OpenAI `gpt-4o-mini` model with a purpose-built system prompt so the assistant stays on-topic and forwards contact links when needed.
- Presents a shareable Gradio `ChatInterface`, enabling recruiters or collaborators to explore the profile conversationally.
- Designed to run entirely from a single Jupyter Notebook, simplifying experimentation and iterative prompt tuning.

Project Structure
-----------------
```
.
├── chatbot.ipynb         # Jupyter Notebook with all chatbot logic
├── readme.md             # Documentation (this file)
├── resume/
│   ├── mushood-latest.pdf  # Source of truth for resume content
│   └── summary.txt         # Condensed profile referenced in the prompt
├── .env                  # Stores OPENAI_API_KEY (not tracked in git)
└── .gitignore            # Standard ignores plus virtualenv folders
```

Getting Started
---------------
1. **Clone & enter the project**
   ```bash
   git clone https://github.com/mushood123/portfolio-chatbot.git chatbot
   cd chatbot
   ```
2. **Create a Python environment (3.10+)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install python-dotenv PyPDF2 gradio openai
   ```
   > Optional: freeze these into `requirements.txt` if you plan to share the project.

Configuration
-------------
1. Copy `.env.example` to `.env` (or create `.env`) and add:
   ```
   OPENAI_API_KEY=sk-...
   ```
2. Ensure the files in `resume/` contain the content you want the chatbot to cite:
   - `mushood-latest.pdf` – the resume that will be fully ingested.
   - `summary.txt` – a concise highlight reel to keep the prompt grounded.

Running the Chatbot
-------------------
1. Launch Jupyter:
   ```bash
   jupyter lab chatbot.ipynb
   ```
   or
   ```bash
   jupyter notebook chatbot.ipynb
   ```
2. Execute the cells in order:
   - Load environment variables and initialize the OpenAI client.
   - Parse the resume PDF and summary file.
   - Review or tweak the generated `system_prompt`.
   - Run the `ChatInterface` cell. Gradio will open a local UI and print a share URL if `share=True`.

Customization
-------------
- **Prompt tone:** Update the prose in the `system_prompt` cell (Cell 4) to change how the avatar responds or to include new guardrails.
- **Persona data:** Replace personal info (name, email, phone, social links) in the same cell to represent a different professional profile.
- **Knowledge sources:** Swap in a different PDF or add extra context (e.g., portfolio blurbs) before the prompt is composed.
- **Model settings:** Adjust `temperature`, `max_tokens`, or `model` inside the `chat` function (Cell 5) to balance creativity vs. fidelity.
- **Deployment:** Convert the notebook to a Python script (`jupyter nbconvert --to script`) and host the Gradio app on a service like Hugging Face Spaces or Render for wider access.

Troubleshooting
---------------
- **Missing API key:** The notebook prints `OPENAI_API_KEY not found` if the environment variable is absent. Confirm `.env` is loaded and the key is valid.
- **PDF parse issues:** Ensure the resume PDF is text-based. If extraction fails, consider exporting the resume as a searchable PDF.
- **Model errors:** OpenAI API errors will surface in the notebook output. Most often they are due to invalid keys, quota limits, or network blocks.
- **Gradio not launching:** Make sure no other service occupies the default port (7860) or pass `launch(share=True, server_port=XXXX)` with a free port.

With these steps the notebook becomes a ready-to-share AI avatar that keeps recruiters and collaborators engaged while you focus on other work. Feel free to adapt the prompt, assets, or hosting setup to match future career updates.
