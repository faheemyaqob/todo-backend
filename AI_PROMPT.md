# AI_PROMPT.md

## Note: This project was AI-assisted
This repository was created and iterated with the help of an AI assistant. The exact prompts and instructions used to generate documentation and code are provided below so others (or other agents) can reproduce or extend this work.

---

## Exact Prompt Used (copy-paste)

```
PROJECT DOCUMENTATION GENERATOR

You are a senior software engineer and technical writer.

I already have a fully working Todo Backend project built with:

Python 3.10+

FastAPI

JWT Authentication

Kafka (Redpanda)

Dapr (Pub/Sub)

Docker Compose

Your task is to write professional project documentation for this repository.

🔹 FILES TO GENERATE

You must generate three documentation files:

README.md

ARCHITECTURE.md

AI_PROMPT.md

🔹 README.md REQUIREMENTS

Include the following sections in this order:

Project Overview

What the project does

Why FastAPI, Kafka, and Dapr are used

Tech Stack

Backend, Messaging, Auth, Runtime

Project Structure

Explain major folders briefly

Setup Instructions

Clone repo

Create & activate venv

Install dependencies

Environment Variables

List all required env vars with examples

Running the System

Start Redpanda (Docker)

Start Dapr

Start FastAPI server

Authentication Flow

Login endpoint

JWT token usage

Authorization header example

API Examples

Login

Create Todo

Get Todos

Kafka & Dapr Flow

When messages are published

Who consumes them

Development Notes

Common issues

Ports used

🔹 ARCHITECTURE.md REQUIREMENTS

Explain:

High-level system architecture

Request flow:

Client → Auth → FastAPI → Kafka → Consumer

Role of Dapr in pub/sub abstraction

Why event-driven architecture is used

How this design can scale

Use simple diagrams in ASCII if helpful.

🔹 AI_PROMPT.md REQUIREMENTS

This file must contain:

The exact prompt used to generate this project

Clear note that this project was AI-assisted

Steps explaining how someone can reuse this prompt to regenerate or extend the project

Emphasis on spec-driven, non-vibe coding

🔹 WRITING STYLE

Clear

Professional

Beginner-friendly

No missing steps

No assumptions

🔹 FINAL RULE

The documentation must make it possible for:

A new developer

A reviewer

Or another AI

to understand, run, and extend the project without asking questions.
```

---

## How to reuse this prompt
1. Open a new chat or your AI assistant of choice.
2. Paste the prompt above exactly (including the `PROJECT DOCUMENTATION GENERATOR` header).
3. Attach or reference the repository structure and any additional constraints (e.g., runtime environment, OS).
4. Ask the assistant to generate the three files: `README.md`, `ARCHITECTURE.md`, `AI_PROMPT.md` and to place them in the repo root.

## Why keep the prompt
- Reproducibility: teammates or judges can see the exact instruction used to produce the docs.
- Iteration: reuse the prompt when you want to update docs after code changes.
- Auditing: demonstrates a spec-driven approach for hackathons and evaluations.

---

## Attribution
This project was developed with AI assistance. Use the prompt above to reproduce or extend the documentation generation process.