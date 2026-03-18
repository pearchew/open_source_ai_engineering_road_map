# 🚀 The Local-First AI Engineer Roadmap (6 Months)

This is meant to be a log of me following @DeRonin_'s [twitter article](https://x.com/DeRonin_/status/2033587293064204349), detailing a roadmap to being an AI engineer. This is a more distilled version and focuses on running through all the core topics quickly, just as a personal understanding/passion project to work through

## 📌 @DeRonin_'s Phase Overview (supplemented with Ollama)

| Month | Focus Area | Core Technologies |
| :--- | :--- | :--- |
| **Month 1** | Software Engineering Fundamentals | Python, Git/GitHub, CLI, FastAPI, REST |
| **Month 2** | Local LLM App Development | Ollama, Llama 3, Structured Outputs, Streaming |
| **Month 3** | Local RAG (Retrieval-Augmented Gen) | Local Embeddings (`nomic-embed-text`), Chroma |
| **Month 4** | Agents, Tools & Workflows | LangGraph, Local Tool Calling, DeepEval |
| **Month 5** | Deployment & Reliability | Docker (Ollama + App), vLLM, GPU monitoring |
| **Month 6** | Specialization & Portfolio | AI Product / Applied ML / AI Automation |

---

## 📅 Month 1: Software & API Fundamentals

### Core Focus
* **Python:** Variables, loops, OOP, `async/await`, error handling, and virtual environments (`venv`).
* **Git & CLI:** Branching, merging, `.gitignore`, and navigating the terminal.
* **APIs & Data:** HTTP requests, JSON, and standard REST patterns. Even though we are running locally, Ollama operates via a local REST API (port `11434`).
* **FastAPI:** Building routes, handling requests/responses, and using Pydantic for validation.

### Core Resources
* **Python:** [CS50P (Harvard)](https://cs50.harvard.edu/python/) | [freeCodeCamp Python](https://www.youtube.com/watch?v=rfscVS0vtbw)
* **Git:** [Learn Git Branching](https://learngitbranching.js.org/)
* **FastAPI:** [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

## 📅 Month 2: Master Local LLM App Development
*Swap cloud APIs for Ollama. Learn to prompt local models, get structured JSON out of them, and stream responses to your UI.*

### Core Focus
* **Ollama Basics:** Installing Ollama, pulling models (`ollama run llama3`), and interacting with the local API.
* **Hardware Constraints:** Understanding VRAM, quantization (GGUF), and the difference between 8B and 70B models.
* **Prompting & Structured Outputs:** Forcing local models to return valid JSON (Ollama supports JSON mode and structured schemas). 
* **Streaming & State:** Managing chat history in memory and streaming tokens to a FastAPI endpoint using the Ollama Python library.

### Core Resources
* **Ollama Setup:** [Ollama Official Docs & GitHub](https://github.com/ollama/ollama)
* **Python Client:** [Ollama Python Library](https://github.com/ollama/ollama-python)
* **Prompting:** [Anthropic Interactive Prompt Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) *(Concepts apply universally to local models)*.

---

## 📅 Month 3: Local RAG (Retrieval-Augmented Generation)
*Build systems that let local LLMs answer questions based on your own private documents without sending data to the cloud.*

### Core Focus
* **Local Embeddings:** Using models like `nomic-embed-text` or `bge-m3` via Ollama or HuggingFace sentence-transformers.
* **Chunking Strategy:** Breaking documents down using LangChain's `RecursiveCharacterTextSplitter`.
* **Local Vector DBs:** Storing and retrieving vectors using local, open-source databases like Chroma or Qdrant.
* **Orchestration:** Using LlamaIndex or LangChain to tie the local embedding model, vector DB, and local LLM together.

### Core Resources
* **Vector DB:** [Chroma Docs](https://docs.trychroma.com/) (Runs entirely local/in-memory).
* **RAG Framework:** [LlamaIndex Local Model Docs](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/usage_custom/#local-models)
* **Embeddings:** [HuggingFace Embedding Guide](https://huggingface.co/blog/getting-started-with-embeddings)

---

## 📅 Month 4: Agents, Workflows & Local Evals
*Agents on local models are trickier than on GPT-4. You will learn the limits of smaller open-weights models and how to build resilient workflows to compensate.*

### Core Focus
* **Multi-step Workflows:** Chaining and routing tasks (e.g., extract -> summarize -> draft) instead of relying on autonomous agents, as smaller local models excel at single, focused tasks.
* **Local Tool Calling:** Using models explicitly fine-tuned for tool use (like Llama 3.1) to trigger Python functions.
* **State Management:** Using LangGraph to manage the memory and state of your workflows.
* **Local Evals:** Testing if your prompts/models are actually working systematically using DeepEval or Promptfoo.

### Core Resources
* **Workflows:** [LangGraph Crash Course](https://academy.langchain.com/courses/intro-to-langgraph)
* **Agent Concepts:** [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
* **Evaluation:** [DeepEval Docs](https://deepeval.com/docs/getting-started)

---

## 📅 Month 5: Local Deployment & Reliability
*Taking your local app and making it robust. This means containerizing your stack and managing local compute resources efficiently.*

### Core Focus
* **Dockerization:** Writing a `docker-compose.yml` that spins up your FastAPI app, your Vector DB, and an Ollama container simultaneously.
* **Production Serving:** Transitioning from Ollama (great for dev) to **vLLM** (the standard for high-throughput local production inference). 
* **Hardware/GPU Monitoring:** Keeping an eye on utilization and handling out-of-memory (OOM) errors gracefully.
* **Caching:** Implementing Redis or GPTCache to save compute by caching identical/similar queries.

### Core Resources
* **Docker:** [Docker Official Guide](https://docs.docker.com/get-started/)
* **Production Inference:** [vLLM GitHub / Docs](https://github.com/vllm-project/vllm)
* **Caching:** [GPTCache](https://github.com/zilliztech/GPTCache)

---

## 📅 Month 6: Specialize

* **Direction 1: AI Product Engineer:** Focus on building frontends for your local models using Streamlit, Gradio, or Vercel AI SDK. Build end-to-end apps you can demo.
* **Direction 2: Applied ML / Local Fine-Tuning:** Dive deep into HuggingFace. Learn to fine-tune open-weights models on consumer hardware using tools like [Unsloth](https://github.com/unslothai/unsloth) or [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory). Understand LoRA, QLoRA, and GGUF conversion.
* **Direction 3: AI Automation:** Connect your local models to business workflows. Use open-source tools like [n8n](https://docs.n8n.io/) to trigger local LLM processing on incoming emails, documents, or CRM data.

---

## 💡 The Bottom Line
The demand for engineers who can build *practical, production-ready* AI systems is massive. By learning how to build locally with open-source models, you gain a massive advantage: you understand hardware, you understand inference optimization, and you know how to build secure, private AI systems that enterprises actually want.

**Stop watching tutorials. Start building.**