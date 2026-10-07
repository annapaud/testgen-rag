# TestGen-RAG

A containerized, two-stage Retrieval-Augmented Generation (RAG) system that automatically turns software requirements into structured QA test scenarios and JSON test cases.

Built using Python 3.11, LlamaIndex, Qdrant, and Ollama

---

## Why This Architecture?

Instead of generating unstructured text in a single prompt, TestGen-RAG uses a modular two-stage workflow:
1. Stage 1 (Scenario Extraction): Queries Qdrant vector storage to extract high-level scenarios across Positive, Negative, Boundary, and Security types.
2. Stage 2 (Step Builder): Expands identified scenarios into atomic, step-by-step JSON test execution scripts with expected outcomes and test data.

Prompts are externalized in prompts to allow model tuning without changing application code.

---

## Stack Overview

* *Orchestration:* LlamaIndex
* *Vector DB:* Qdrant (Dockerized)
* *LLM & Embeddings:* Ollama (\llama3\, \omic-embed-text\)
* *Environment:* Docker & Docker Compose

---

## Project Structure

testgen-rag/
├── data/
│   └── docs/
├── prompts/
│   ├── scenario_prompt.txt
│   └── detailed_case_prompt.txt
├── src/
│   ├── ingest.py
│   └── query.py
├── tests/
│   ├── scenarios.json
│   └── detailed_test_cases.json
├── docker-compose.yml
├── Dockerfile
└── requirements.txt

---


## Output Artifacts

Test outputs are written directly to \	ests/\:
* \	ests/scenarios.json\: High-level scenario mapping.
* \	ests/detailed_test_cases.json\: Complete step-by-step test execution scripts.
