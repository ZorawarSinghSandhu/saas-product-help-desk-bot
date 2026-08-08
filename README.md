# 🤖 SaaS Help-Desk RAG Bot

An AI-powered customer support chatbot that answers user questions using a company's own help documentation through a Retrieval-Augmented Generation (RAG) pipeline.

Instead of relying solely on an LLM's training data, the chatbot retrieves relevant documentation from a vector database and generates responses grounded in the company's knowledge base. Every response includes source citations, making the system reliable, transparent, and suitable for real-world customer support.

Built with **Python**, **FastAPI**, **ChromaDB**, **Sentence Transformers**, **Groq LLaMA**, **React**, **Docker**, **Railway**, and **Vercel**.

---

## 📸 Preview

> *Replace the placeholders below with your actual media.*

### 🖥️ Chat Interface
*(Add a high-quality static screenshot of the UI here)*

### 🎥 Live Interaction & Citations
*(Add a GIF demonstrating typing a question, streaming the answer, and clicking a source citation here)*

---

## ✨ Features & Highlights

- 🤖 **AI-Powered RAG Chatbot:** Answers questions using your company's own documentation instead of relying on an LLM's general knowledge.
- 🔍 **Local Semantic Search:** Uses Sentence Transformers to convert docs into embeddings and ChromaDB for fast similarity searches—zero embedding API costs.
- 📖 **Source Citations:** Every response includes verifiable links and article titles from the original documentation.
- 🚫 **Hallucination Reduction:** Politely informs the user if the answer isn't in the indexed documentation instead of fabricating a response.
- ⚡ **Fast REST API:** Built with FastAPI, automatic Pydantic validation, and Swagger UI.
- 💻 **Modern Chat Interface:** Responsive React frontend built with Tailwind CSS and Framer Motion.
- 🐳 **Automated Vector Indexing:** Docker automatically builds the ChromaDB index during container creation—keeping the repo lightweight and ensuring a fresh index on every deployment.
- ☁️ **Cloud Deployment:** Production-ready with Railway (FastAPI backend) and Vercel (React frontend).
- 🔧 **Easily Adaptable:** Works with virtually any SaaS help center by simply updating the scraper configuration.

---

## 🎯 Why This Project?

Many SaaS companies maintain extensive help centers, but finding relevant information can still be frustrating for users. Traditional chatbots often rely solely on an LLM's general knowledge, which leads to inaccurate or hallucinated responses.

This project addresses that problem by implementing a Retrieval-Augmented Generation (RAG) pipeline that intentionally separates document indexing from question answering. Instead of answering from memory, the chatbot retrieves the most relevant documentation and uses it as context. The result is a support assistant that provides accurate, context-aware answers while drastically reducing hallucinations.

---

## 📖 System Architecture

```text
                    DOCUMENT INDEXING PIPELINE (Runs Once)

        SaaS Help Center Documentation
                    │
                    ▼
          BeautifulSoup Web Scraper
                    │
                    ▼
             Raw Text Extraction
                    │
                    ▼
         Text Chunking (500 / 100 overlap)
                    │
                    ▼
   Sentence Transformers Embedding Model
                    │
                    ▼
        ChromaDB Vector Database
                    │
────────────────────┼────────────────────────────────────────────
                    │
                    ▼
             QUERY PIPELINE (Runs Per Request)

            User Question (React UI)
                    │
                    ▼
            FastAPI Backend (/ask)
                    │
                    ▼
      Generate Question Embedding
                    │
                    ▼
      Retrieve Top-K Relevant Chunks
                    │
                    ▼
         Groq LLaMA 3.3 70B Model
                    │
                    ▼
          AI Response + Citations
                    │
                    ▼
            React Chat Interface
```

## ⚙️ Indexing Pipeline

The indexing pipeline prepares the documentation before the chatbot can answer questions:

1. **Documentation Scraping:** A web scraper crawls the help center, extracting article titles, content, and URLs, saving them as text files in the `Raw_text` directory.
2. **Text Chunking:** Large articles are split into **500-character chunks with a 100-character overlap** to preserve context between adjacent sections.
3. **Embedding Generation:** Each chunk is converted into a dense vector using **Sentence Transformers** (`all-MiniLM-L6-v2`). Running locally eliminates API costs and allows unlimited indexing.
4. **Vector Storage:** Embeddings are stored in **ChromaDB**, enabling semantic similarity search rather than basic keyword matching.

---

## 💬 Query Pipeline

When a user submits a question, the following executes in real-time:

1. **Question Embedding:** The React frontend sends the question to FastAPI, where the same Sentence Transformer model converts it into a vector.
2. **Similarity Search:** ChromaDB retrieves the most relevant documentation chunks based on semantic similarity.
3. **LLM Generation:** The retrieved context is sent to **Groq's LLaMA 3.3 70B** model, which is instructed strictly to answer *only* using the provided documentation.
4. **Response:** The backend returns the AI-generated answer along with clickable source URLs and article titles for the frontend to display.

---

## ☁️ Deployment Architecture

The application is deployed as two independent services, allowing the UI and the API to be updated and scaled independently:

- **Frontend:** Hosted on **Vercel** (React + Vite)
- **Backend:** Hosted on **Railway** (FastAPI + Docker)

### 🐳 Automated Docker Build & Indexing

The backend is fully containerized. A core design decision of this project is that **the vector database is generated automatically during the Docker build process**. 

Because the index is built during container creation, the Git repository never needs to store heavy, generated embedding files. Every deployment automatically builds a fresh vector index from the latest documentation.

During every deployment, the Docker engine automatically:
1. Installs Python dependencies
2. Downloads the local Sentence Transformer model
3. Copies the scraped documentation files
4. Runs `indexer.py` to generate a fresh **ChromaDB** vector store
5. Packages everything into a production-ready image

### 📦 Continuous Deployment Workflow

Both services support continuous deployment. A push to the `main` branch automatically triggers the following pipeline:

```text
       Local Development (Git Push)
                    │
                    ▼
                  GitHub
                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼
 Railway (Backend)          Vercel (Frontend)
      │                           │
 Docker Build               Build React App
      │                           │
 Run indexer.py                   │
 (Builds ChromaDB)                │
      │                           │
 Launch FastAPI          Connects to Backend API
      │                           │
      └─────────────┬─────────────┘
                    │
                    ▼
                 End User
```

## 📦 Backend

The backend is built with **FastAPI**, providing a fast, asynchronous REST API for the chatbot.

Responsibilities:

- Receives user questions
- Performs vector retrieval
- Sends context to the LLM
- Returns responses with citations
- Handles CORS configuration
- Exposes health monitoring endpoint

---

## 💻 Frontend

The frontend is a modern single-page application built with React.

### Technologies

- React
- Vite
- Tailwind CSS
- Framer Motion

Responsibilities:

- Chat interface
- API communication
- Loading states
- Response rendering
- Source citation display
- Responsive design

---

## 🤖 Artificial Intelligence

The project uses a Retrieval-Augmented Generation (RAG) pipeline.

### Large Language Model

**Provider**

- Groq

**Model**

```
llama-3.3-70b-versatile
```

The LLM is responsible only for generating answers from the retrieved documentation.

---

## 🧠 Embedding Model

Documentation embeddings are generated locally using Sentence Transformers.

Model:

```
sentence-transformers/all-MiniLM-L6-v2
```

Benefits:

- No embedding API costs
- Unlimited indexing
- Fast local inference
- No rate limits

---

## 🗄️ Vector Database

The project uses **ChromaDB** for semantic document retrieval.

Responsibilities:

- Store document embeddings
- Perform similarity search
- Retrieve the most relevant documentation chunks
- Persist vector data locally

---

## 📄 Document Processing

Documentation is automatically collected using:

- BeautifulSoup4
- Requests

The scraper extracts:

- Article titles
- Documentation content
- Source URLs

These articles are later chunked and indexed.

---

## 🐳 Containerization

The backend is fully containerized using Docker.

The Docker image automatically:

- Installs dependencies
- Downloads the embedding model
- Copies documentation
- Builds the vector database
- Starts the FastAPI server

This makes deployments reproducible across all environments.

---

## ☁️ Cloud Deployment

### Backend

- Railway
- Docker

### Frontend

- Vercel

Environment variables are used to separate development and production configurations.

---

## 🔧 Development Tools

- Git
- GitHub
- VS Code
- npm
- pip
- Docker Desktop

---

## 📊 Technology Overview

```text
Frontend
├── React
├── Vite
├── Tailwind CSS
└── Framer Motion

Backend
├── FastAPI
├── Pydantic
├── Uvicorn
└── Python

AI
├── Groq
├── LLaMA 3.3
├── Sentence Transformers
└── ChromaDB

Deployment
├── Docker
├── Railway
└── Vercel
```

## 📂 Project Structure

```text
SaaS-HelpDesk-RAG-Bot/
├── 📁 Raw_text/          # Scraped help center articles saved as plain text
├── 📁 Source_Code/
│   ├── Scraper.py        # Crawls documentation and extracts content to Raw_text/
│   ├── chunker.py        # Splits documents into 500-character overlapping chunks
│   ├── indexer.py        # Generates embeddings and builds the ChromaDB vector store
│   ├── query.py          # Handles RAG logic: embedding questions and calling Groq LLM
│   └── main.py           # FastAPI entry point, endpoints (/ask, /health), and CORS
├── 📁 frontend/          # React + Vite frontend application (Tailwind, Framer Motion)
├── Dockerfile            # Automated build instructions for the backend and ChromaDB index
├── requirements.txt      # Python backend dependencies
└── .env                  # Environment variables (API keys, CORS origins)
```

# 🔄 Project Workflow

```text
Scraper.py

↓

Raw_text/

↓

chunker.py

↓

Sentence Transformers

↓

indexer.py

↓

ChromaDB

↓

FastAPI

↓

React Frontend

↓

User
```

---

# 📦 Deployment Workflow

```text
GitHub

│

├──────────────► Railway

│                   │

│              Docker Build

│                   │

│        Install Dependencies

│                   │

│      Download Embedding Model

│                   │

│          Run indexer.py

│                   │

│      Launch FastAPI Backend

│

└──────────────► Vercel

                    │

               React Frontend

                    │

              Connect to Railway

                    │

                  End User
```

---

# 🚀 Installation & Setup

## Prerequisites

Before getting started, ensure you have the following installed:

- Python 3.11 or later
- Node.js 18 or later
- Git
- Docker Desktop (optional, for containerized deployment)
- A free Groq API key

---

# 📥 Clone the Repository

```bash
git clone https://github.com/ZorawarSinghSandhu/saas-product-help-desk-bot.git

cd saas-product-help-desk-bot
```

---

# 🐍 Backend Setup

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

ALLOWED_ORIGINS=http://localhost:5173
```

---

# 📄 Index the Documentation

If you're using a new help center, first scrape the documentation.

```bash
cd Source_Code

python Scraper.py
```

This downloads all help articles into the `Raw_text` directory.

---

Next, build the vector database.

```bash
python indexer.py
```

The indexer will:

- Read all documentation
- Split it into chunks
- Generate embeddings
- Build the ChromaDB vector database

This only needs to be executed whenever the documentation changes.

---

# 🚀 Start the Backend

```bash
uvicorn main:app --reload
```

The API will now be available at

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

Health Check

```
http://localhost:8000/health
```

---

# 💻 Frontend Setup

Open a second terminal.

```bash
cd frontend

npm install
```

Create a `.env` file inside the frontend directory.

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start the development server.

```bash
npm run dev
```

The frontend will be available at

```
http://localhost:5173
```

---

# Why Docker?

Docker provides a reproducible production environment by packaging the application, dependencies, embedding model, and vector database into a single portable image.

Benefits include:

- Consistent environment across machines
- Simplified deployment
- No dependency conflicts
- Faster cloud deployments
- Reproducible builds

---

# Build the Docker Image

From the project root:

```bash
docker build -t helpdesk-bot .
```

The first build may take several minutes because Docker needs to:

- Download the Python base image
- Install Python packages
- Download the embedding model
- Generate document embeddings
- Build the ChromaDB vector database

Subsequent builds are significantly faster due to Docker layer caching.

---

# Run the Container

After the image has been built, start the application using:

```bash
docker run -p 8000:8000 ^
-e GROQ_API_KEY=your_api_key ^
helpdesk-bot
```

For macOS/Linux:

```bash
docker run -p 8000:8000 \
-e GROQ_API_KEY=your_api_key \
helpdesk-bot
```

The API will now be accessible at:

```
http://localhost:8000
```

---

# Verify the Deployment

Health Endpoint

```
http://localhost:8000/health
```

Expected response:

```json
{
    "status": "ok"
}
```

Interactive API Documentation

```
http://localhost:8000/docs
```

You can also connect the React frontend to the running container and verify that questions return answers together with source citations.

---

# Automatic Vector Indexing

One of the key design decisions of this project is generating the vector database during the Docker build.

Instead of committing generated embedding files to GitHub, the Docker image rebuilds the vector store automatically by executing:

```bash
python indexer.py
```

This provides several advantages:

- Smaller Git repository
- No binary database files under version control
- Fresh vector database on every deployment
- Easier onboarding for new developers

---

# Dockerfile Overview

The Dockerfile performs the following tasks:

1. Creates a Python 3.11 environment.
2. Installs backend dependencies.
3. Downloads the Sentence Transformer model.
4. Copies the project source code.
5. Executes `indexer.py` to build the ChromaDB database.
6. Starts the FastAPI server using Uvicorn.

This allows the application to be deployed without any manual indexing steps.

---

# 🌍 Production Architecture

```text
                    GitHub Repository
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
      Railway Backend              Vercel Frontend
            │                             │
      Docker Deployment             React + Vite
            │                             │
      FastAPI REST API            Static Site Hosting
            │                             │
            └──────────────┬──────────────┘
                           │
                           ▼
                        End Users
```

---

# 🚂 Backend Deployment (Railway)

The FastAPI backend is deployed using Railway.

Railway automatically detects the Dockerfile, builds the Docker image, and deploys the application whenever changes are pushed to GitHub.

---

## Required Environment Variables

Configure the following variables inside the Railway dashboard.

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | API key used for generating responses with Groq |
| `ALLOWED_ORIGINS` | URL of the deployed frontend for CORS |


## Production Endpoints

Health Check

```
https://your-backend.up.railway.app/health
```

Swagger Documentation

```
https://your-backend.up.railway.app/docs
```

API Endpoint

```
POST /ask
```

---

# ▲ Frontend Deployment (Vercel)

The React application is deployed independently on Vercel.

Vercel automatically builds the frontend whenever new commits are pushed to GitHub.

---

# 🔄 Continuous Deployment

Both services support automatic deployment.

```text
Developer

↓

Git Commit

↓

GitHub

│

├────────────► Railway

│                 │

│          Docker Build

│                 │

│        Backend Deployment

│

└────────────► Vercel

                  │

           Frontend Build

                  │

            Live Website
```

Every push to the `main` branch automatically updates both services.

---

# 🌱 Environment Variables

## Backend (.env)

```env
GROQ_API_KEY=your_api_key

ALLOWED_ORIGINS=http://localhost:5173
```

Production values are configured through Railway.

---

## Frontend (.env)

```env
VITE_API_URL=http://127.0.0.1:8000
```

Production values are configured through Vercel.

---

# 📦 Deployment Workflow

```text
Local Development

│

├── Backend (.env)

├── Frontend (.env)

│

▼

Git Push

│

▼

GitHub

│

├────────► Railway

│            │

│       Docker Build

│            │

│     Run indexer.py

│            │

│      Start FastAPI

│

└────────► Vercel

             │

      Build React App

             │

      Connect to Railway

             │

             ▼

      Production Application
```

---

# 🚀 Updating the Documentation

When documentation changes:

1. Update the scraper configuration (if required).
2. Run the scraper to download the latest articles.
3. Commit and push the updated documentation.
4. Railway automatically rebuilds the Docker image.
5. During the Docker build, `indexer.py` regenerates the ChromaDB vector database.
6. The updated chatbot is deployed automatically.

No manual database migration or vector upload is required.

---

# 📈 Scalability

The current architecture is designed for small to medium-sized documentation websites and can be extended with additional services such as:

- Redis caching
- PostgreSQL
- Authentication
- Background workers
- Analytics
- Admin dashboard
- Multiple documentation collections
- Streaming responses

The modular architecture makes these enhancements straightforward without requiring major changes to the existing codebase.


# 📡 API Reference

The backend exposes a simple REST API built with FastAPI.

Base URL (Local)

```
http://localhost:8000
```

Base URL (Production)

```
https://your-backend.up.railway.app
```

Interactive API Documentation

```
https://your-backend.up.railway.app/docs
```

---

## POST /ask

Answers a user's question using the indexed documentation.

### Request

```http
POST /ask
Content-Type: application/json
```

Request Body

```json
{
    "question": "How does seat billing work?"
}
```

---

### Response

```json
{
    "answer": "Seat billing is based on the number of active users in your organization...",
    "sources": [
        "https://docs.example.com/billing/seat-billing"
    ],
    "file_headings": [
        "Seat Billing"
    ]
}
```

---

## GET /health

Simple endpoint used to verify that the backend is running.

### Request

```http
GET /health
```

### Response

```json
{
    "status": "ok"
}
```

This endpoint is commonly used by Railway and other monitoring systems to confirm the service is healthy.


# 🔄 Adapting the Bot to Another SaaS

The chatbot has been designed to work with virtually any SaaS documentation website.

Most of the application is reusable. Only the documentation source needs to be changed.

---

## Step 1 — Update the Scraper

Open:

```
Source_Code/Scraper.py
```

Replace the starting URL with the new company's documentation.

Example:

```python
url = "https://company.com/help/getting-started"
```

Depending on the website structure, you may also need to update:

- HTML selectors
- Next-page navigation
- Stop conditions

No other backend code needs to change.

---

## Step 2 — Download the Documentation

Run:

```bash
python Scraper.py
```

The scraper downloads all documentation into:

```
Raw_text/
```

---

## Step 3 — Build the Vector Database

Run:

```bash
python indexer.py
```

This automatically:

- Splits the documents into chunks
- Generates embeddings
- Creates a fresh ChromaDB collection

---

## Step 4 — Update the System Prompt

Inside:

```
query.py
```

Replace the company name in the system prompt.

Example:

```text
You are a helpful customer support assistant for Acme Inc.
```

---

## Step 5 — Deploy

Push the updated project to GitHub.

Railway automatically rebuilds the Docker image, regenerates the vector database, and deploys the updated chatbot.

No frontend changes are required.

---

## What Doesn't Change

Everything below remains identical:

- React frontend
- FastAPI backend
- ChromaDB
- Sentence Transformers
- Groq integration
- Docker
- Railway deployment
- Vercel deployment
- API endpoints

This makes the project easy to customize for new clients while keeping the core architecture unchanged.

# 🚀 Future Improvements

Potential enhancements for future versions include:

- 🔐 User authentication
- 📤 Upload PDFs instead of scraping websites
- 🌍 Support multiple documentation collections
- 💬 Conversation history
- ⚡ Streaming AI responses
- 📊 Analytics dashboard
- 🛡️ Rate limiting and API security
- 📁 Admin panel for managing documentation
- 🔎 Hybrid search (keyword + semantic)
- 🧠 Embedding model selection
- 🌐 Multi-language documentation support
- 📱 Progressive Web App (PWA)
- ☁️ AWS or Azure deployment
- 🐳 Docker Compose support
- 📈 Monitoring with Prometheus and Grafana


# 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project in accordance with the terms of the license.
