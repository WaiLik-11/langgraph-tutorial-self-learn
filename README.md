# LangGraph Tutorial

A hands-on learning repository for building stateful AI workflows using [LangGraph](https://github.com/langchain-ai/langgraph) and LangChain.

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd langGraph-tutorial
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your API keys:

```bash
cp .env.example .env
```

Then open `.env` and replace the placeholder values:

| Variable | Where to get it |
|---|---|
| `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `GROQ_API_KEY` | [Groq Console](https://console.groq.com/keys) |

### 5. Launch Jupyter (for notebooks)

```bash
jupyter notebook
```

---

## Project Structure

```
langGraph-tutorial/
├── .env                  # Your local API keys (git-ignored)
├── .env.example          # Template for environment variables
├── .gitignore
├── requirements.txt
├── Agents/
│   ├── agent-bot.py      # Simple chatbot agent
│   ├── ReAct-agent.py    # ReAct pattern agent with tools
│   ├── memory-agent.py   # Stateful agent with conversation memory
│   ├── drafter.py        # Human-in-the-loop document drafting agent
│   └── RAG-agent.py      # RAG agent over a PDF using ChromaDB
├── Graphs/
│   ├── hello-world.ipynb
│   ├── sequential-graph.ipynb
│   ├── conditional-graph.ipynb
│   ├── looping-graph.ipynb
│   └── multiple-input.ipynb
└── Exercise/
    ├── exercise-1.ipynb
    ├── exercise-2.ipynb
    ├── exercise-3.ipynb
    ├── exercise-4.ipynb
    └── exercise-5.ipynb
```

---

## File Reference

### Agents

#### `Agents/agent-bot.py`
A basic interactive chatbot loop. Accepts user input, passes it through a `StateGraph` with a single LLM node, and prints the response. Good starting point for understanding how LangGraph wraps an LLM call.

- **LLM:** Google Gemini 2.5 Flash Lite
- **Concepts:** `StateGraph`, `TypedDict` state, `START`/`END`, input loop

#### `Agents/ReAct-agent.py`
Implements the **ReAct (Reasoning + Acting)** agent pattern. The agent can reason about a task and call tools when needed, then continue reasoning based on the tool result.

- **LLM:** Google Gemini 2.5 Flash Lite
- **Tools:** Custom `add(a, b)` tool via `@tool` decorator
- **Concepts:** `add_messages` reducer, `ToolNode`, `Annotated` types, tool binding, `BaseMessage` hierarchy

#### `Agents/memory-agent.py`
A stateful chatbot that maintains full conversation history across turns using LangGraph state. The agent appends each exchange to the `messages` list so the LLM always has prior context.

- **LLM:** Google Gemini 2.5 Flash Lite
- **Concepts:** persistent message history, `HumanMessage`/`AIMessage`, stateful multi-turn conversation

#### `Agents/drafter.py`
A **Human-in-the-loop** document drafting agent. The AI generates a draft, the human provides feedback, and the cycle continues until the human is satisfied. Supports saving the final draft to a file.

- **LLM:** Google Gemini 2.5 Flash Lite
- **Tools:** `update` (overwrites document content), `save` (writes draft to disk)
- **Concepts:** human feedback loop, `interrupt`, `ToolNode`, global document state

#### `Agents/RAG-agent.py`
A **Retrieval-Augmented Generation (RAG)** agent that answers questions about a PDF document. Loads and chunks the PDF, stores embeddings in a ChromaDB vector store, then uses a retriever tool inside a LangGraph agent loop.

- **LLM:** Google Gemini 2.5 Flash Lite
- **Embeddings:** `gemini-embedding-001` via `GoogleGenerativeAIEmbeddings`
- **Vector Store:** ChromaDB (persisted locally)
- **Tools:** `retriever_tool` — similarity search returning top-5 chunks
- **Concepts:** `PyPDFLoader`, `RecursiveCharacterTextSplitter`, `Chroma`, RAG agent loop, conditional edges

---

### Graphs

#### `Graphs/hello-world.ipynb`
The very first graph — a single node that updates a string in state. Covers creating, compiling, and visualising a `StateGraph` with Mermaid diagrams.

- **Concepts:** `StateGraph`, node functions, `set_entry_point`, `set_finish_point`, graph visualisation

#### `Graphs/sequential-graph.ipynb`
Multiple nodes wired together in a straight line. Each node reads and transforms part of the state before passing it to the next.

- **Concepts:** `add_edge`, multi-node pipelines, linear state transformation

#### `Graphs/conditional-graph.ipynb`
Introduces branching — a router node inspects the state and directs execution to different nodes (e.g. addition vs. subtraction path).

- **Concepts:** `add_conditional_edges`, router functions, multiple execution paths

#### `Graphs/looping-graph.ipynb`
A node that loops back to itself until a counter condition is met. Shows how to build iterative processes inside a graph.

- **Concepts:** self-loop edges, counter-based termination, state accumulation with lists

#### `Graphs/multiple-input.ipynb`
A single node that handles multiple state fields of different types (list and string) simultaneously.

- **Concepts:** complex `AgentState`, list aggregation, multi-field state processing

---

### Exercises

#### `Exercise/exercise-1.ipynb`
Build a compliment agent that **concatenates** strings into state rather than replacing them.

- **Challenge:** String accumulation in state

#### `Exercise/exercise-2.ipynb`
Create a conditional node that either **sums** or **multiplies** a list of integers depending on an `operation` field in state.

- **Challenge:** Conditional logic inside a node, `math.prod`

#### `Exercise/exercise-3.ipynb`
Build a 3-node sequential pipeline that assembles a formatted user profile (greeting → age description → skills list).

- **Challenge:** Chaining 3 nodes with `add_edge`, string formatting

#### `Exercise/exercise-4.ipynb`
A more complex conditional graph with **two routing stages** and four different math operation paths.

- **Challenge:** Chained conditional routing, nested decision logic

#### `Exercise/exercise-5.ipynb`
Implement a **Higher/Lower guessing game** where the graph acts as an AI player. It tracks bounds, adjusts its search space based on hints, and terminates on a win or after 7 attempts.

- **Challenge:** Game loop architecture, intelligent bound adjustment, win/lose conditions

---

## Learning Path

The content follows a natural progression:

```
Graphs (concepts) → Agents (LLM integration) → Exercises (practice)

hello-world → sequential → conditional → looping → multiple-input
    ↓
agent-bot → ReAct-agent → memory-agent → drafter → RAG-agent
    ↓
exercise-1 → exercise-2 → exercise-3 → exercise-4 → exercise-5
```
