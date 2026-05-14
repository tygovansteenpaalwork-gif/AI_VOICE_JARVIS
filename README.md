# Jarvis Assistance

A local conversational AI assistant built with ElevenLabs and Python.

## What it does

- Connects to ElevenLabs Conversational AI
- Uses a custom audio interface for speech output
- Supports tool calls like web search and saving results
- Loads secrets from a `.env` file

## Setup

1. Clone the repo:
   ```powershell
   git clone https://github.com/<your-username>/<your-repo>.git
   cd jarvis_assistance
   ```

2. Create a `.env` file in the project root with:
   ```text
   ELEVENLABS_API_KEY="sk_xxx"
   AGENT_ID="agent_xxx"
   ```

3. Create and activate the Python 3.11 environment:
   ```powershell
   py -3.11 -m venv .venv311
   .\.venv311\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip setuptools wheel
   python -m pip install -r requirements.txt
   ```

5. Run the assistant:
   ```powershell
   python .\main.py
   ```

## Make it look like a product

- Add a clear `README.md` with features and setup instructions
- Keep your `.env` out of source control
- Use a descriptive GitHub repo name
- Add screenshots or demo instructions in the README
- Consider adding a project logo or badges later

## Publish to GitHub

1. Initialize Git locally:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   ```

2. Create a GitHub repository on github.com.

3. Add the remote and push:
   ```powershell
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

## Notes

- Keep `.env` private
- If you want to share the project, add a short demo GIF or video to the README
- Use GitHub Pages or the repo description to make the product look polished
