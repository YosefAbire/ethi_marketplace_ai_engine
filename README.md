<div align="center">
  <img width="1200" height="400" alt="Ethi Marketplace Banner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" style="border-radius: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.15);" />

  # 🇪🇹 Ethi Marketplace AI Engine
  ### *The Future of Ethiopian E-commerce Intelligence*

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/)
  [![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

---

## 🚀 Project Vision
**Ethi Marketplace AI Engine** is a state-of-the-art multi-agent ecosystem designed to revolutionize how businesses operate within the Ethiopian marketplace. It bridges the gap between traditional commerce and AI-driven intelligence, providing real-time inventory management, strategic seller advice, and autonomous logistics coordination.

---

## 🧠 Core Intelligence: The Multi-Agent System
Our architecture revolves around a specialized multi-agent orchestration layer that routes complex queries to the most qualified "expert" agent.

| Agent | Expertise | Primary Function |
| :--- | :--- | :--- |
| **Workflow Agent** | 🧭 Orchestration | Intelligently routes user prompts to specialized agents based on intent. |
| **SQL Agent** | 📊 Structured Data | Interacts with inventory databases to provide real-time stock and order data. |
| **RAG Agent** | 📚 Knowledge Nexus | Processes unstructured documents (PDFs, policies) using Retrieval Augmented Generation. |
| **Seller Agent** | 📈 Strategic Growth | Analyzes market snapshots to provide tailored business advice for sellers. |
| **Ops Agent** | 🚚 Logistics Lead | Handles supply chain reliability and provides practical Ethiopian delivery guidance. |

---

## ✨ Key Modules

### 🖥️ Intelligent Dashboard
Real-time visualization of marketplace performance, including live order tracking, inventory heatmaps, and seller metrics.

### 💬 AI Chat Hub
A unified interface where users interact with the multi-agent engine. Whether it's "How do I ship to arbaminch?" or "What's my highest selling item?", the engine provides instant, context-aware answers.

### 📂 Knowledge Nexus
Upload and index marketplace policies, regional shipping regulations, or product catalogs. The AI instantly learns and retrieves information from these documents.

---

## 🛠️ Technical Architecture

### **Frontend Stack**
- **Framework**: `React 18` with `Vite` for lightning-fast builds.
- **Language**: `TypeScript` for robust, type-safe development.
- **Styling**: Modern, responsive CSS with a focus on premium aesthetics.
- **Communication**: Seamless WebSocket/HTTP integration with the FastAPI backend.

### **Backend Stack**
- **Core Engine**: `FastAPI` (Python 3.9+).
- **AI Framework**: `LangChain` for agent orchestration and memory.
- **Model**: `Google Gemini 1.5 Flash` for industrial-grade reasoning.
- **Database**: `PostgreSQL` for persistent relational data, `ChromaDB` for vector storage, and `SQLAlchemy` for ORM.

---

## ⚙️ Getting Started

### 1️⃣ Clone and Prepare
```bash
git clone https://github.com/yourusername/ethi-marketplace-ai-engine.git
cd ethi-marketplace-ai-engine
```

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
> [!IMPORTANT]
> Create a `.env` file in the `backend/` directory and add:
> `API_KEY=your_google_gemini_api_key`
> `DATABASE_URL=postgresql://user:password@localhost:5432/ethi_marketplace`

### 3️⃣ Frontend Setup
```bash
cd ../frontend
npm install
```
> [!NOTE]
> Ensure `.env.local` contains your `VITE_GEMINI_API_KEY` if running in direct client mode.

### 4️⃣ Launch the Engine
**Terminal 1 (Backend):**
```bash
cd backend
python api/main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

---

## 🗺️ Roadmap & Features
- [x] **Multi-Agent Routing**: Auto-detection of user intent.
- [x] **RAG Implementation**: Full document indexing support.
- [x] **Email Engine**: Autonomous notification system for operations.
- [ ] **Real-time SMS Integration**: For local Ethiopian carrier notifications.
- [ ] **Multi-language Support**: Introducing Amharic and Oromiffa LLM fine-tuning.

---

<div align="center">
  <p>Built with ❤️ for the Ethiopian E-commerce Ecosystem</p>
  <p><i>Empowering local sellers with world-class AI technology.</i></p>
</div>
