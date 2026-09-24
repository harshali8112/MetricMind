---

## 🧠 Key Features

### 1. Natural Language Understanding

MetricMind understands business terminology and common synonyms.

Examples:

- `sales` → Revenue
- `profitability` → Margin
- `expenses` → Cost
- `customer attrition` → Churn

---

### 2. Intent Extraction

The AI Orchestrator identifies:

- Region
- Business metric
- Previous period
- Current period
- Query type

Example:

```text
Question:
Why did European margins drop from Q2 to Q3?

Intent:
Region: Europe
Metric: Margin
Previous Period: Q2
Current Period: Q3
Intent Type: Comparison

---

### 3. Query Planning

The Query Planner converts the extracted intent into a structured analytical query.

Example:

```text
Operation: Multi-step
Primary Metric: Margin
Region: Europe
Previous Period: Q2
Current Period: Q3

---

### 4. Query Validation & Guardrails

Before executing a query, MetricMind validates it against the supported business operations.

The validator checks:

- Supported metrics
- Supported regions
- Supported quarters
- Supported operations
- Required parameters
- Invalid period comparisons

Unsupported questions are safely rejected instead of being answered using assumptions.

Example:

```text
Question:
What is the weather in Delhi?

Response:
I could not create a valid business query plan.

Reason:
No supported business metric identified.

---

### 5. Multi-Step Business Reasoning

MetricMind can break complex business questions into multiple analytical steps.

Example:

```text
Why did European margins drop from Q2 to Q3?

###The Orchestrator evaluates:

Margin Change
      ↓
Revenue Growth
      ↓
Cost Growth
      ↓
Growth Relationship
      ↓
Business Explanation

Example result:

European margins decreased by 6 percentage points
from Q2 to Q3.

Revenue: +10.0%
Cost: +18.68%
Margin: -6 percentage points

Reason:
Cost grew faster than revenue.

###🏗️ Architecture
                 ┌─────────────────────┐
                 │    Streamlit UI     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  AI Orchestrator    │
                 │      LangGraph      │
                 └──────────┬──────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      ┌──────────────┐             ┌──────────────┐
      │    Intent    │             │  Validator   │
      │  Extraction  │             │ & Guardrails │
      └──────┬───────┘             └──────┬───────┘
             │                            │
             └─────────────┬──────────────┘
                           ▼
                 ┌─────────────────────┐
                 │    Query Planner     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Semantic API      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Semantic Layer    │
                 │  Mock / Future API  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Verified Business   │
                 │       Results       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Explainable Answer  │
                 └─────────────────────┘
🛠️ Technology Stack
Technology	Purpose
Python	Core application
LangGraph	Agent orchestration
LangChain	LLM framework
Ollama	Local LLM runtime
Llama 3.2 3B	Local language model
Streamlit	User interface
Git & GitHub	Version control

###📁 Project Structure
MetricMind/
│
├── agent/
│   ├── __init__.py
│   ├── graph.py
│   ├── intent.py
│   ├── query_planner.py
│   ├── semantic_api.py
│   ├── tools.py
│   └── validator.py
│
├── app.py
├── main.py
├── requirements.txt
├── .env
└── .gitignore
###Core Modules
graph.py — Main AI Orchestrator and LangGraph workflow.
intent.py — Extracts structured intent from natural-language questions.
query_planner.py — Converts intent into structured analytical queries.
validator.py — Validates queries and provides safety guardrails.
semantic_api.py — Interface between the Orchestrator and Semantic Layer.
tools.py — Development tools and controlled business data.
app.py — Streamlit conversational BI interface.
main.py — CLI interface for testing the Orchestrator.

###▶️ Running the Project
---

## ▶️ Running the Project

### 1. Create Virtual Environment

```bash
python -m venv .venv
2. Activate Environment

Windows:

.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Start Ollama

Make sure Ollama is installed and the local model is available:

ollama pull llama3.2:3b
5. Run Streamlit Application
streamlit run app.py

For CLI testing:

python main.py
🧪 Example Queries
Revenue Lookup
What is the revenue in Asia Q3?

Result:

The revenue in Asia for Q3 is $900,000.
Metric Definition
What is margin?

Result:

Margin = (Revenue - Cost) / Revenue * 100.
Multi-Step Analysis
Why did European margins drop from Q2 to Q3?

Result:

European margins decreased by 6 percentage points
from Q2 to Q3.

Revenue: +10.0%
Cost: +18.68%
Margin: -6 percentage points

Reason:
Cost grew faster than revenue.
Unsupported Query
What is the weather in Delhi?

Result:

I could not create a valid business query plan.

Reason:
No supported business metric identified.
🔐 Reliability & Guardrails

MetricMind follows a simple principle:

The LLM should explain verified business information, not invent business information.

The architecture separates:

LLM
 ↓
Understanding + Explanation

Semantic Layer
 ↓
Business Facts + Metrics

Validator
 ↓
Query Control

This helps prevent unsupported business answers and keeps business calculations outside the LLM's assumptions.

▶️ Running the Project
---

## ▶️ Running the Project

### 1. Create Virtual Environment

```bash
python -m venv .venv
2. Activate Environment

Windows:

.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Start Ollama

Make sure Ollama is installed and the local model is available:

ollama pull llama3.2:3b
5. Run Streamlit Application
streamlit run app.py

For CLI testing:

python main.py
🧪 Example Queries
Revenue Lookup
What is the revenue in Asia Q3?

Result:

The revenue in Asia for Q3 is $900,000.
Metric Definition
What is margin?

Result:

Margin = (Revenue - Cost) / Revenue * 100.
Multi-Step Analysis
Why did European margins drop from Q2 to Q3?

Result:

European margins decreased by 6 percentage points
from Q2 to Q3.

Revenue: +10.0%
Cost: +18.68%
Margin: -6 percentage points

Reason:
Cost grew faster than revenue.
Unsupported Query
What is the weather in Delhi?

Result:

I could not create a valid business query plan.

Reason:
No supported business metric identified.

###🔮 Future Enhancements
Connect the real Semantic Layer API
Connect enterprise data sources
Add dynamic business visualizations
Add trend and anomaly analysis
Add production API layer
Deploy the complete system
