# POE-EDU — Professional Educational AI Chat Proxy

POE-EDU is a professional, educational repository that demonstrates how to proxy Poe.com frontend models for research, classroom experiments, and responsible development. This project is intended for learning and experimentation only and includes an easy-to-run FastAPI-based backend, a streaming example (Server-Sent Events), conversation history, and a clean single-page frontend.

Key features
- FastAPI backend with async HTTP client (httpx)
- SQLite-backed conversation history
- Server-Sent Events (SSE) example for streaming replies
- Professional README, terms, contributing guide, and code of conduct
- Dockerfile and docker-compose for easy deployment

Important: Poe is a third-party service. This repository demonstrates how Poe's frontend endpoints can be used for educational exploration — you must follow Poe's terms of service. The repository does not provide official Poe API access.

Quickstart (local)
1. Copy the example env and set your Poe session token:
   cp .env.example .env
   # Edit .env and set POE_SESSION_TOKEN

2. Install dependencies:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Run locally:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. Open http://127.0.0.1:8000

Docker
- Build and run with docker-compose:
  docker-compose up --build

Educational Purpose & Responsible Use
This repository is designed for educational and research purposes. Do not use extracted tokens or automated access to third-party services in ways that violate their terms. Avoid abusive, illegal, or harmful use cases. See TERMS.md for the full statement.

Files of interest
- main.py — FastAPI app and SSE streaming example
- templates/index.html, static/* — frontend
- data.db — SQLite DB created at runtime (ignored by .gitignore)

License
This project is licensed under the MIT License. See LICENSE in the repo.

Contributing
Please read CONTRIBUTING.md and CODE_OF_CONDUCT.md before opening pull requests.

Acknowledgements
- Poe.com for hosting various models and for inspiration
- Open-source libraries used in this repo: FastAPI, httpx, sse-starlette
