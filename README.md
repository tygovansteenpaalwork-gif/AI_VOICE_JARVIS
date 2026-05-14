# Jarvis Assistance

A spoken conversational AI assistant built with ElevenLabs and Python.

## Overview

`Jarvis Assistance` is a local demo application that connects a Python process to ElevenLabs Conversational AI. It captures microphone audio, sends it to the assistant, and plays back audio responses so the interaction feels like a voice conversation.

This repository is designed as a small, reusable example of how to wire together:

- ElevenLabs audio output
- ElevenLabs conversational agents
- local microphone input
- custom tool execution
- secure configuration with `.env`

## What the project does

When you run the app, it:

- starts a conversation session with ElevenLabs
- records microphone audio and sends it to the assistant
- receives agent responses as audio chunks
- plays the response through the speaker
- exposes simple custom tools the agent can call during the conversation

The application is useful for prototyping voice assistants, experimenting with custom ElevenLabs agents, and showing how to integrate tool calls in a spoken workflow.

## How it works

The core flow is in `main.py`:

1. load configuration from `.env`
2. create an `ElevenLabs` client with the API key
3. start a `Conversation` with the selected `AGENT_ID`
4. start audio capture and output using the custom interface
5. handle incoming agent events and playback audio

The `tools.py` module exposes agent-callable tools:

- `searchweb`: perform a DuckDuckGo search for the given query
- `savetotxt`: save received text to a local file

These tools let the agent enrich the conversation with external actions.

## Key files

- `main.py` — main application and conversation setup
- `tools.py` — custom tool registration for the agent
- `.env` — private configuration values
- `requirements.txt` — Python dependencies
- `.gitignore` — files to exclude from Git
- `.vscode/settings.json` — VS Code terminal environment settings
- `LICENSE` — project license

## What you need

- Python 3.11 installed locally
- ElevenLabs API key
- An ElevenLabs conversational agent with a valid `AGENT_ID`
- A microphone and audio output device

## Configuration

Create a `.env` file in the project root with your credentials:

```text
ELEVENLABS_API_KEY="sk_xxx"
AGENT_ID="agent_xxx"
```

### Where to find `AGENT_ID`

1. Go to your ElevenLabs dashboard.
2. Create or open your conversational agent.
3. Copy the agent's unique ID from the agent settings.
4. Paste it into `.env` as `AGENT_ID`.

If you changed the agent's personality or behavior in ElevenLabs, use the latest agent ID so the local app uses your custom configuration.

## Setup and run

### 1. Create the virtual environment

```powershell
py -3.11 -m venv .venv311
.\.venv311\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### 3. Run the assistant

```powershell
python .\main.py
```

## Expected behavior

Once the app starts:

- it will establish a session with ElevenLabs
- it will listen for microphone input
- the assistant will speak responses back through your speakers
- if your agent decides to use a tool, the tool will run locally

If it feels like the assistant is talking too quickly or restarting, make sure your microphone is not accidentally generating input while the agent is speaking.

## How to customize

### Change agent behavior

- update `AGENT_ID` in `.env` to your own custom agent
- modify the agent settings in ElevenLabs
- restart the app after changing the agent ID

### Add new tools

To add a tool:

1. edit `tools.py`
2. create a new tool function that accepts `parameters`
3. register it with `client_tools.register("tool_name", your_function)`

Example ideas:

- `fetch_weather`
- `calendar_query`
- `translate_text`
- `save_note`

### Add a text-only mode

You can extend the application to support text input by adding a separate message-sending path in `main.py` and bypassing the microphone interface.

## Possible extensions

This project can grow into a more complete assistant by adding:

- richer tool integration with external APIs
- agent state persistence across sessions
- a web or desktop UI
- transcript saving and export
- multiple agent profiles or personas
- offline speech recognition / text fallback

## Troubleshooting

### `.env` not loading

- confirm `.env` exists in the project root
- ensure `ELEVENLABS_API_KEY` and `AGENT_ID` are set
- do not commit `.env` to GitHub

### invalid API key

If the app reports `invalid_api_key`, replace the key with a valid ElevenLabs API key from your account.

### default or wrong agent

If the assistant uses a default agent:

- verify `AGENT_ID` is correct
- use the agent ID from your ElevenLabs conversational agent
- save `.env` and restart the app

## Recommended repository structure

```text
jarvis_assistance/
├── .gitignore
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── tools.py
├── .vscode/settings.json
└── .env (local only)
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
