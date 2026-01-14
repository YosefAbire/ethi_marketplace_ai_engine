README.md
# 🛒 Marketplace AI

**Marketplace AI** is a Direct-to-Consumer (D2C) agricultural retail management system that combines **PostgreSQL-based database management** with **AI-powered natural language querying**.  

The system allows users to manage sellers, products, and orders, while enabling intelligent queries over the database using Google’s Generative AI models.  

---

## 🎯 Features

- **Manage Agricultural Products**: Track products, sellers, and orders in PostgreSQL.
- **AI-Powered SQL Queries**: Use natural language to query the database via LangChain and Google GenAI.
- **Interactive API**: FastAPI backend with automatic Swagger documentation.
- **Secure Configuration**: Secrets and database credentials stored in `.env`.

---

## 🏗️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Database**: PostgreSQL
- **AI Integration**: Google Generative AI via `langchain-google-genai`
- **ORM/Utility**: SQLAlchemy, LangChain Community SQL Agent
- **Environment Management**: `python-dotenv`

---

## 📝 Project Structure



marketplace_ai/
├─ app/
│ ├─ api/
│ │ ├─ main.py # FastAPI app and routes
│ ├─ agents/
│ │ ├─ sql_agent.py # AI-powered SQL agent
│ ├─ core/
│ │ ├─ config.py # Environment variables
├─ migrations/ # (Optional) Alembic migrations
├─ .env # Local secrets (ignored in git)
├─ .env.example # Template for collaborators
├─ requirements.txt # Project dependencies
├─ README.md


---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/YosefAbire/ethi_marketplace_ai_engine.git
cd market

Create a virtual environment

python -m venv env
source env/Scripts/activate       # Windows
# OR
source env/bin/activate           # macOS/Linux


Install dependencies

pip install -r requirements.txt


Set up .env

GOOGLE_API_KEY=your_google_genai_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/marketplace_ai


⚠️ Important: Never commit your .env to GitHub.

Initialize PostgreSQL database

CREATE DATABASE marketplace_ai;


Run the FastAPI server

uvicorn app.api.main:app --reload


Access the API docs at http://127.0.0.1:8000/docs

🧠 Usage Example

POST Request to /ask

{
  "query": "List the first 5 products from the products table."
}


Response

{
  "answer": "The first 5 products are:\n- ID: 1, Name: Maize, Price: 1200.00, Stock: 50\n- ID: 2, Name: Wheat, Price: 1500.00, Stock: 30\n- ID: 3, Name: Tomatoes, Price: 800.00, Stock: 100"
}

🔒 Security Best Practices

Store all API keys and credentials in .env.

Add .env to .gitignore.

Use environment variables for deployment (Heroku, AWS, Docker, etc.) instead of hardcoding secrets.

Limit database access to trusted hosts.

🚀 Deployment

Docker: Create a Dockerfile and .dockerignore to containerize the application.

Cloud: Set DATABASE_URL and GOOGLE_API_KEY as environment variables in your cloud provider.

Production Server: Run Uvicorn behind a reverse proxy (e.g., Nginx).

🤝 Contributing

1. Fork the repository

2. Create a new branch (git checkout -b feature/awesome-feature)

3. Make your changes and commit (git commit -m "Add awesome feature")

4. Push to your branch (git push origin feature/awesome-feature)

5. Open a Pull Request

📜 License

MIT License © 2026 Yosef Abire


---

### **.gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
env/
venv/
ENV/

# PostgreSQL
*.db
*.sqlite3

# Environment variables
.env

# Logs
*.log
*.out

# IDEs
.vscode/
.idea/

# MacOS
.DS_Store
