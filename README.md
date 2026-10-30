# CloudCart Customer Support Agent

A lightweight customer support assistant built with FastAPI and LangChain/OpenAI. The service exposes a REST API that accepts customer questions and returns a support answer using a tool-augmented agent with access to CloudCart's refund policy.

## Overview

This project demonstrates a simple AI-powered support workflow for e-commerce operations. It is designed to answer customer questions about policies, with the first implemented tool specifically covering refund policy details.

The application combines:
- FastAPI for the HTTP API
- LangChain agent tooling for structured reasoning
- OpenAI GPT models for natural language responses
- Python-dotenv for environment configuration

## Key Features

- Customer support chat endpoint via REST API
- Tool-augmented agent pattern
- Refund policy retrieval as a structured tool call
- Health check endpoint for monitoring
- Easy local setup with a `.env` file
- Production-friendly FastAPI app structure

## Architecture

The project is intentionally small and focused:

- `main.py` defines the FastAPI application and routes
- `agent.py` contains the LangChain agent, tool definitions, and reusable `ask_agent()` function
- `requirements.txt` lists all Python dependencies
- `.env` stores secrets such as the OpenAI API key

At a high level:

1. A client sends a message to the `/chat` endpoint.
2. FastAPI validates the request.
3. The agent receives the customer query.
4. The agent decides whether to use a tool such as `get_refund_policy()`.
5. The response is returned to the client as plain text.

## Tech Stack

- Python 3
- FastAPI
- Pydantic
- LangChain
- LangChain OpenAI
- OpenAI GPT models
- Python dotenv

## Project Structure

```text
customer-support-agent/
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── agent.py
├── calibration_cases.json
├── compare_evaluators.py
├── evaluate_agent.py
├── llm_judge.py
├── main.py
├── requirements.txt
├── test_evaluator.py
├── test_llm_judge.py
└── .venv/
```

## Local Setup

1. Clone the repository.
2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_key_here
```

Optional LangSmith tracing configuration is also supported:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=cloudcart-support-dev
```

## Running the API

Start the FastAPI app with Uvicorn:

```bash
uvicorn main:app --reload
```

Then open:
- `http://localhost:8000/health`
- `http://localhost:8000/docs`

## API Usage

### Health check

```bash
curl http://localhost:8000/health
```

Example response:

```json
{"status": "ok"}
```

### Chat endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is your refund policy?"}'
```

Example response:

```json
{"answer":"CloudCart accepts returns within 30 days of delivery. Items must be unused and in original packaging. Refunds are issued to the original payment method within 5-7 business days after return approval."}
```

## Example Agent Behavior

The agent is configured to answer customer support questions professionally and concisely. It relies on a tool called `get_refund_policy()` when a customer asks about returns or refund eligibility.

Example questions:
- What is your refund policy?
- Can I return an unused item?
- How long does it take to get my refund?
- What happens if I have a damaged delivery?

The agent is intentionally conservative: it will not invent policies and will say when it does not have enough information.

## Deployment Notes

The repository includes a `Dockerfile`, making it suitable for containerized deployment.

Build the image:

```bash
docker build -t customer-support-agent .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env customer-support-agent
```

## Security Considerations

This project stores secrets in a local `.env` file. The repository includes `.gitignore` entries to prevent accidental commits of:
- `.env`
- `.env.*`
- private keys
- generated Python cache files

Do not commit real API keys or production credentials to source control.

## Troubleshooting

### Missing OpenAI key

If you see a `RuntimeError` about `OPENAI_API_KEY`, confirm your `.env` file exists and contains a valid key.

### App fails to start

Check the following:
- Dependencies are installed
- The virtual environment is active
- `.env` is present and valid
- The port is not already in use

## License

This project is intended for learning and demonstration purposes unless a repository-specific license is added later.
