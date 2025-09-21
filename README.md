<img src="docs/image.png" alt="Agent Force Banner" width="1000">

---

# 🤖 Agent Force

### Revolutionary Multi-Agent AI Research Platform Powered by Collaborative Intelligence

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6+-FF6B35)](https://langchain-ai.github.io/langgraph)
[![Coral Protocol](https://img.shields.io/badge/Coral-Protocol-FF4500)](https://coralprotocol.org)

*Transform how you conduct research with AI agents that collaborate, debate, and deliver insights beyond traditional AI capabilities.*



---

## 🌟 What is Agent Force?

Agent Force is a cutting-edge AI research platform that orchestrates multiple specialized AI agents to conduct comprehensive market research, competitive analysis, and strategic business insights in real-time. Built on the revolutionary Coral Protocol, our platform creates a "Society of AI Agents" that collaborate, communicate securely, and scale their efforts across different frameworks.

### 🎯 Key Features

- **🤝 Multi-Agent Collaboration** - Specialized AI agents work together seamlessly
- **⚡ Real-Time Streaming** - Watch agents collaborate live through WebSocket streaming  
- **🛡️ Enterprise Security** - JWT authentication with enterprise-grade security
- **🎨 Modern UI/UX** - Beautiful React interface with dark theme and animations
- **🔧 Coral Protocol Integration** - Agent communication and orchestration infrastructure
- **📊 Comprehensive Reports** - Executive summaries, strategic insights, and data-driven conclusions
- **🔄 LangGraph Orchestration** - Advanced workflow management for complex agent interactions
- **📱 Responsive Design** - Works perfectly on desktop and mobile devices

### 🚀 Use Cases

- **Market Research** - Deep market analysis and competitive landscape insights
- **Business Strategy** - Strategic recommendations and growth opportunities
- **Innovation Research** - Emerging trends and future predictions
- **Competitive Intelligence** - Competitor strategies and market positioning
- **Industry Analysis** - Comprehensive sector overviews and trend analysis

---

### 🛠️ Tech Stack

#### Frontend
- **React 18** - Modern JavaScript framework
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI** - Accessible component primitives
- **React Query** - Powerful data fetching
- **React Router** - Client-side routing
- **Lucide Icons** - Beautiful icon set

#### Backend
- **FastAPI** - High-performance async web framework
- **LangGraph** - Multi-agent orchestration and workflows
- **SQLAlchemy** - Modern ORM with async support
- **PostgreSQL** - Robust database for data persistence
- **JWT Authentication** - Secure token-based auth
- **WebSockets** - Real-time streaming capabilities
- **Coral Protocol** - Agent communication infrastructure

#### AI/ML
- **OpenAI GPT-4** - Primary LLM for agent intelligence
- **LangChain** - LLM integration and prompt management
- **MCP (Model Context Protocol)** - Agent tooling standard
- **Custom Agent Architectures** - Specialized research agents

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Docker** (optional, for containerized deployment)

### 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agent-force.git
   cd agent-force
   ```

2. **Backend Setup**
   ```bash
   # Navigate to backend
   cd MultiAgents_Workflow
   
   # Install Python dependencies
   poetry install
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API keys and database URL
   
   # Run database migrations
   poetry run alembic upgrade head
   
   # Start the backend server
   poetry run uvicorn core.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup**
   ```bash
   # Navigate to frontend (in new terminal)
   cd ../Frontend
   
   # Install Node dependencies
   npm install
   
   # Start the development server
   npm run dev
   ```

4. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb agentforce_db
   
   # Or use Docker
   docker run --name agentforce-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
   ```

### ⚙️ Configuration

Create a `.env` file in the `MultiAgents_Workflow` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agentforce_db

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
AIML_API_KEY=your-openai-api-key

# Coral Protocol (optional)
CORAL_SERVER_URL=http://localhost:5555

# Environment
ENVIRONMENT=development
DEBUG=True
```

### 🎯 Usage

1. **Access the Application**
   - Frontend: http://localhost:5173 (Built With Lovable)
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

2. **Create an Account**
   - Sign up with email and password
   - Verify your email (if configured)

3. **Start Research**
   - Enter your research topic
   - Choose number of analysts (2-5 recommended)
   - Click "Start Research"
   - Watch agents collaborate in real-time

4. **View Results**
   - Comprehensive reports with executive summaries
   - Strategic recommendations and insights
   - Download reports in multiple formats

### 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual services
docker build -t agentforce-backend ./MultiAgents_Workflow
docker build -t agentforce-frontend ./Frontend
```

## 📚 API Documentation

### Core Endpoints

- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user profile
- `POST /api/v1/run-research` - Initiate research session
- `GET /api/v1/research-stream` - Real-time research streaming
- `GET /api/v1/user-sessions` - Get user research history

### WebSocket Events

- `start` - Research session initialized
- `event` - Agent activity updates
- `complete` - Research completion with results
- `error` - Error handling and notifications

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `npm test && poetry run pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Guidelines

- **Code Style**: Follow PEP 8 for Python, ESLint for JavaScript
- **Testing**: Add tests for new features
- **Documentation**: Update docs for API changes
- **Commits**: Use conventional commit format

### Project Structure

```
agent-force/
├── Frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   └── api/             # API client code
│   └── package.json
├── MultiAgents_Workflow/     # FastAPI backend
│   ├── core/                 # Core application code
│   │   ├── routes/          # API route handlers
│   │   ├── models.py        # Database models
│   │   └── main.py          # FastAPI app
│   ├── agents/              # AI agent implementations
│   │   ├── ResearchAgent/   # Research agent logic
│   │   └── ReportAgent/     # Report generation agent
│   └── pyproject.toml
├── coral-server/            # Coral Protocol server
├── docker-compose.yml       # Docker orchestration
└── README.md
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Coral Protocol** - Revolutionary agent communication infrastructure
- **LangGraph** - Powerful multi-agent orchestration framework
- **FastAPI** - Incredible async web framework
- **React** - Best frontend framework ever
- **AIML API** - Cutting-edge language models


## 🎉 Show Your Support

If you find Agent Force helpful, please give us a ⭐ on GitHub!

---

<div align="center">

**Built with ❤️ by the Agent Force team**

[🌟 Star us on GitHub](https://github.com/HassanMehmood413/AgentMarketing) • [🐛 Report Issues](https://github.com/HassanMehmood413/AgentMarketing/issues)

</div>
