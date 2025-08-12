# 🤖 Agentic AI Autonomous Governance Swarm

A comprehensive multi-agent system for end-to-end architecture governance and validation, built with FastAPI backend and React frontend.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)               │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   Dashboard     │ │ Agent Management│ │ Governance      │ │
│  │   - System      │ │ - Agent Status  │ │ Validation      │ │
│  │   Overview      │ │ - Controls      │ │ - Multi-step    │ │
│  │   - Quick       │ │ - Configuration │ │   Wizard        │ │
│  │   Actions       │ │ - Monitoring    │ │ - Results       │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 Core Brain Agent                        │ │
│  │  - Orchestration & Task Routing                        │ │
│  │  - Result Synthesis & Monitoring                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Solution    │ │ Technical   │ │ Security    │ │ Data    │ │
│  │ Architecture│ │ Architecture│ │ Architecture│ │Architect│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Integration │ │Infrastructure│ │ Costing     │ │Portfolio│ │
│  │ Architecture│ │ Architecture │ │ Agent       │ │ Agent   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 🎯 **Multi-Agent Collaboration**
- **Core Brain Agent**: Central orchestrator managing specialized agents
- **9 Specialized Agents**: Solution, Technical, Security, Data, Integration, Infrastructure, Costing, Application Portfolio, and Generic
- **Autonomous Task Distribution**: Intelligent routing based on governance scope
- **Real-time Communication**: Inter-agent messaging and coordination

### 🛡️ **Comprehensive Governance**
- **End-to-End Validation**: Complete architecture assessment pipeline
- **Multi-Domain Coverage**: Solution, technical, security, data, integration, infrastructure
- **Compliance Frameworks**: TOGAF, ISO 42010, AWS Well-Architected, Azure Architecture, GCP Architecture
- **Risk Assessment**: Automated risk scoring and mitigation recommendations

### 🎨 **Modern React Frontend**
- **Dark Theme UI**: Professional, modern interface with Material-UI components
- **Real-time Dashboard**: Live system monitoring and agent status
- **Interactive Validation Wizard**: Multi-step governance validation process
- **Agent Management**: Complete agent monitoring and control interface
- **File Upload System**: Drag-and-drop architecture file upload with processing
- **Reports & Analytics**: Comprehensive reporting and visualization
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 🔧 **Advanced Capabilities**
- **Human-in-Loop Oversight**: Manual review and approval workflows
- **Continuous Improvement**: Learning from validation results
- **Performance Monitoring**: Real-time metrics and SLA tracking
- **Security & Compliance**: Zero-trust architecture with encrypted communication
- **Scalable Architecture**: Horizontal scaling and load balancing

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/pikvik/Agentic_architecture_Governance.git
cd Architecture_Agent
```

### 2. Backend Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-simple.txt

# Create environment configuration
cp config.env.example .env
# Edit .env with your API keys and configuration

# Create required directories
mkdir -p logs data reports

# Start the backend server
python main.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

### 4. Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 Frontend Features

### 🏠 **Dashboard**
- **System Overview**: Active agents, total validations, success rate, response time
- **Quick Actions**: Start validation, generate report, manage agents, settings
- **Agent Status Grid**: Real-time monitoring with start/stop controls
- **System Health Alerts**: Live status updates and notifications

### 🤖 **Agent Management**
- **Agent Overview**: Total agents, active count, health metrics, performance
- **Individual Controls**: Start, stop, restart, configure each agent
- **Configuration Dialogs**: Performance settings, capabilities, timeouts
- **Add New Agents**: Wizard for creating custom specialized agents
- **Health Monitoring**: Real-time health and performance bars

### 🛡️ **Governance Validation**
- **Multi-Step Wizard**: Define scope → Configure → Execute → Review
- **Scope Selection**: Visual cards for all architecture domains
- **Real-time Progress**: Live progress bars and status updates
- **Results Dashboard**: Risk scores, compliance metrics, recommendations
- **Action Buttons**: Start, stop, view results, download reports

### 📊 **Reports & Analytics**
- **Metrics Dashboard**: Total reports, monthly count, average scores
- **Report Table**: View, download, filter reports by type and date
- **Generate Reports**: Custom report creation with multiple formats (PDF, HTML, JSON)
- **Analytics Charts**: Performance trends and compliance metrics

### 📁 **File Upload & Processing**
- **Multi-Format Support**: PDF, DOCX, PPTX, PNG, JPG, SVG, and more
- **Drag-and-Drop Interface**: Easy file upload with visual feedback
- **Architecture Domain Classification**: Automatic categorization by domain
- **Content Extraction**: Text, images, and diagrams extraction
- **Architecture Element Detection**: Automatic identification of components, patterns, and decisions
- **File Validation**: Compliance and quality assessment
- **Processing Status**: Real-time upload and processing progress
- **Metadata Extraction**: Document properties and creation information

### 🤖 **LLM Integration**
- **Dify Platform Integration**: Connect to hosted Dify applications and workflows
- **Ollama Local LLM**: Run local language models with Ollama
- **Multi-Model Support**: Switch between different LLM providers
- **Chat Interface**: Interactive chat with both Dify and Ollama models
- **Model Management**: Pull, list, and manage Ollama models
- **Health Monitoring**: Real-time status monitoring of LLM services
- **Workflow Execution**: Execute Dify workflows for complex AI tasks

### ⚙️ **Settings**
- **System Configuration**: Agent limits, timeouts, batch sizes, debug mode
- **Security Settings**: Encryption, audit logging, session management
- **Notification Preferences**: Email, Slack, validation alerts
- **Storage Management**: Retention policies, backup settings, compression

## 🔌 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with system information
- `GET /health` - Health check
- `GET /agents` - List all agents
- `GET /swarm/status` - Overall swarm status

### Governance Endpoints
- `POST /governance/validate` - Start governance validation
- `GET /governance/status/{validation_id}` - Check validation status
- `GET /governance/results/{validation_id}` - Get validation results

### Agent Endpoints
- `GET /agents/{agent_id}` - Get agent details
- `POST /agents/{agent_id}/start` - Start agent
- `POST /agents/{agent_id}/stop` - Stop agent
- `POST /agents/{agent_id}/restart` - Restart agent

### File Upload Endpoints
- `POST /files/upload` - Upload architecture file
- `GET /files` - List all uploaded files
- `GET /files/{file_id}` - Get file details
- `POST /files/{file_id}/validate` - Validate architecture file
- `DELETE /files/{file_id}` - Delete file

### LLM Integration Endpoints
- `GET /llm/health` - Check LLM services health
- `GET /llm/ollama/models` - List Ollama models
- `POST /llm/ollama/generate` - Generate text with Ollama
- `POST /llm/ollama/chat` - Chat completion with Ollama
- `POST /llm/ollama/embed` - Generate embeddings with Ollama
- `POST /llm/ollama/pull` - Pull Ollama model
- `GET /llm/dify/workspaces` - List Dify workspaces
- `GET /llm/dify/applications` - List Dify applications
- `POST /llm/dify/chat` - Chat completion with Dify
- `POST /llm/dify/completion` - Text completion with Dify
- `GET /llm/dify/conversations/{id}` - Get conversation history

## 🏗️ Architecture Domains

### **Solution Architecture Agent**
- Business alignment validation
- Solution pattern assessment
- Stakeholder requirement analysis
- Cost-benefit evaluation

### **Technical Architecture Agent**
- Code quality analysis
- Technology stack validation
- Performance assessment
- Technical debt evaluation

### **Security Architecture Agent**
- Security control validation
- Compliance framework checking
- Vulnerability assessment
- Risk mitigation analysis

### **Data Architecture Agent**
- Data quality assessment
- Governance policy validation
- Data flow analysis
- Privacy compliance checking

### **Integration Architecture Agent**
- API design validation
- Service interoperability
- Integration pattern assessment
- Message flow analysis

### **Infrastructure Architecture Agent**
- Cloud infrastructure validation
- Scalability assessment
- Resource optimization
- Disaster recovery planning

### **Costing Agent**
- Cost analysis and optimization
- Resource utilization assessment
- Budget planning and forecasting
- ROI calculation

### **Application Portfolio Agent**
- Portfolio management
- Application lifecycle tracking
- Dependency mapping
- Modernization planning

## 🔧 Configuration

### Environment Variables
```bash
# Dify Platform
DIFY_API_KEY=your_dify_api_key
DIFY_BASE_URL=https://api.dify.ai/v1

# LLM Providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Database
DATABASE_URL=sqlite:///./architecture_governance.db
REDIS_URL=redis://localhost:6379/0
MONGODB_URL=mongodb://localhost:27017/architecture_governance

# Security
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
ENCRYPTION_KEY=your_encryption_key

# Application
DEBUG=True
LOG_LEVEL=INFO
PORT=8000
HOST=0.0.0.0
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Production Deployment
```bash
# Build frontend for production
cd frontend
npm run build

# Start backend with production settings
python main.py --production
```

## 📊 Performance SLAs

- **Response Time**: < 5 seconds for validation requests
- **Throughput**: 100+ concurrent validations
- **Availability**: 99.9% uptime
- **Accuracy**: > 95% validation accuracy
- **Scalability**: Horizontal scaling support

## 🔒 Security & Compliance

- **Zero-Trust Architecture**: All communications encrypted
- **RBAC**: Role-based access control
- **Audit Logging**: Complete audit trail
- **Data Encryption**: At-rest and in-transit encryption
- **Compliance**: ISO 42010, TOGAF, GDPR, SOX, HIPAA

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/pikvik/Agentic_architecture_Governance/wiki)
- **Issues**: [GitHub Issues](https://github.com/pikvik/Agentic_architecture_Governance/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pikvik/Agentic_architecture_Governance/discussions)

## 🎯 Roadmap

- [ ] Advanced ML model integration
- [ ] Real-time collaboration features
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Integration with more cloud providers
- [ ] Automated remediation capabilities
- [ ] Advanced reporting templates
- [ ] Multi-tenant support

---

**Built with ❤️ using FastAPI, React, and Material-UI**
