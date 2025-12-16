# Hyperion | AI-Powered Energy Configurator

[![Hyperion Demo](https://img.youtube.com/vi/PkIsMVDxh-Q/maxresdefault.jpg)](https://youtu.be/PkIsMVDxh-Q)

> 📺 **[Watch the full end-to-end demo](https://youtu.be/PkIsMVDxh-Q)** featuring core functionalities.

<br />

![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-Simulation-150458?style=for-the-badge&logo=pandas&logoColor=white)
![LangChain](https://img.shields.io/badge/AI-LangChain-orange?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Passing-green?style=for-the-badge)

**Hyperion** is a full-stack technical sales tool designed for the Energy Industry. It bridges the gap between complex engineering simulations and executive sales proposals.

### Why this exists
Industrial energy sales (e.g., Wärtsilä, Siemens Energy) require complex calculations to prove value. Spreadsheets are error-prone, and static PDFs don't scale. Hyperion solves this by:

1.  **Physics-Based Simulation:** Instead of static estimates, it uses a **Pandas/NumPy engine** to simulate a 24-hour power dispatch cycle (Solar Curves + Engine Baseload + Battery Peak Shifting).
2.  **Instant Financial Feedback:** Calculates **LCOE** (Levelized Cost of Electricity) and CAPEX in real-time.
3.  **GenAI Automation:** Uses **LangChain & GPT-4o** to instantly draft technical proposals based on the specific simulation data, reducing hours of manual writing.

---

## System Architecture

The application is built on a containerized Microservices architecture:

1.  **Frontend (React + TypeScript):** A high-performance dashboard using **Material UI** and **Recharts** for real-time visualization of energy profiles.
2.  **Calculation Engine (Python + Pandas):** A vectorised simulation layer that generates synthetic solar data and optimizes dispatch logic (Solar → Battery → Engine).
3.  **Backend API (FastAPI):** Asynchronous orchestration handling simulation requests and DB transactions.
4.  **Database (PostgreSQL):** Persists hardware specifications (Products) and user configurations.
5.  **AI Service (LangChain):** Chains simulation KPIs into prompt templates to generate context-aware sales pitches.

## Key Features

-   **Dynamic Configurator:** Sliders to adjust Engine Count, Solar MW, and Battery MWh.
-   **Real-Time Physics:** Visualizes the "Duck Curve" phenomenon where engines ramp down as solar peaks.
-   **Financial Modeling:** Automatic calculation of Total CAPEX and CO2 Savings vs Coal baseline.
-   **AI Proposal Agent:** "One-Click" generation of executive summaries citing specific project numbers.

---

## Tech Stack

### Backend & Data
-   **Framework:** FastAPI (Async Python 3.10)
-   **Simulation:** Pandas, NumPy (Vectorized Operations)
-   **AI:** LangChain, OpenAI GPT-4o-mini
-   **Database:** PostgreSQL 15, SQLAlchemy (ORM), Pydantic (Validation)

### Frontend
-   **Core:** React 18, Vite, TypeScript
-   **UI Library:** Material UI (MUI v5)
-   **Visualization:** Recharts (D3-based wrapper)
-   **Networking:** Axios

### DevOps
-   **Containerization:** Docker, Docker Compose
-   **Hot Reloading:** Configured for both Frontend & Backend dev capability.

---

## Getting Started

### Prerequisites

-   Docker Desktop installed
-   OpenAI API Key

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Nibir1/Hyperion.git
    cd Hyperion
    ```

2.  **Set Environment Variables**
    Create a `.env` file in the root or export the key directly:
    ```bash
    export OPENAI_API_KEY=sk-proj-xxxx...
    ```

3.  **Build and Run**
    ```bash
    make build
    ```

Make build command internally runs:

```bash
docker-compose build --no-cache
docker-compose up -d
@echo "Application running at http://localhost:3000"
```

### Testing & Validation

This project includes a comprehensive test suite using **Pytest** that covers **100% of the critical calculation logic** and API endpoints.

The tests run inside the Docker container to ensure environment consistency. We use:
- **In-Memory SQLite:** To perform fast, isolated database integration tests without affecting the persistence layer.
- **Unittest Mocks:** To simulate OpenAI API calls, ensuring the test suite is zero-cost and runs offline.
- **Pytest-Cov:** To verify code coverage metrics.

To run the full test suite and view the coverage report:

```bash
make tests

### Access Points

-  **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
-  **Backend Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## How It Works

### 1. The Physics Simulation (`calculations.py`)
Hyperion doesn't guess; it calculates.
-   **Solar:** Generates a Gaussian bell curve peaking at 12:00 PM.
-   **Battery:** Detects evening peak demand (18:00-21:00) and discharges stored energy.
-   **Engines:** Fill the remaining "Net Load" gap to ensure 100% reliability.

### 2. The AI Workflow (`ai_service.py`)
1.  User clicks "Generate Proposal".
2.  Backend runs the simulation to get final KPIs (e.g., "45,000 Tons CO2 Saved").
3.  LangChain injects these numbers into a prompt template.
4.  LLM returns a cohesive paragraph explaining *why* this specific configuration is profitable.

---

## Project Structure

```text
Hyperion/
├── docker-compose.yml       # Orchestration
├── backend/
│   ├── app/
│   │   ├── api/             # API Routes
│   │   ├── main.py          # Entry Point & Lifespan
│   │   ├── calculations.py  # Pandas Simulation Engine
│   │   ├── ai_service.py    # LangChain Logic
│   │   ├── models.py        # SQLAlchemy Tables
│   │   └── schemas.py       # Pydantic Models
│   └── requirements.txt
├── frontend/
│   ├── public/              # Static Assets (Logo)
│   ├── src/
│   │   ├── components/      # UI Blocks (Chart, Form, KPIs)
│   │   ├── services/        # API Integration
│   │   └── App.tsx          # Main Dashboard Logic
│   └── package.json
└── README.md
```

## Roadmap
- [x] Core Simulation Engine (Solar/Engine/Battery)
- [x] Financial Logic (LCOE/Capex)
- [x] GenAI Proposal Integration
- [ ] User Auth (Save Projects per User)
- [ ] PDF Export of Charts

## License
This project is open-source and available under the MIT License.

Author: Nahasat Nibir - Full Stack Data & AI Engineer