# 🤖 LLM Integration Setup Guide

This guide will help you set up the LLM integration with Dify and Ollama for the Agentic AI Swarm system.

## 📋 Prerequisites

### 1. Ollama Installation

**macOS:**
```bash
# Install using Homebrew
brew install ollama

# Start Ollama service
ollama serve
```

**Linux:**
```bash
# Install using curl
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

**Windows:**
```bash
# Download from https://ollama.ai/download
# Run the installer and start Ollama
```

### 2. Dify Platform Access

1. **Create a Dify Account:**
   - Visit [Dify.ai](https://dify.ai)
   - Sign up for an account
   - Create a new workspace

2. **Get API Key:**
   - Go to your workspace settings
   - Navigate to API Keys section
   - Create a new API key
   - Copy the API key for configuration

3. **Create an Application:**
   - Create a new application in Dify
   - Note down the Application ID
   - Configure the application as needed

## ⚙️ Configuration

### 1. Environment Variables

Add the following variables to your `.env` file:

```bash
# Dify Configuration
DIFY_API_KEY=your_dify_api_key_here
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_WORKSPACE_ID=your_workspace_id
DIFY_APP_ID=your_application_id

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT=120
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=4096
```

### 2. Ollama Model Setup

Pull some common models for testing:

```bash
# Pull Llama 2 (7B parameters)
ollama pull llama2

# Pull Code Llama (for code analysis)
ollama pull codellama

# Pull Mistral (good performance/size ratio)
ollama pull mistral

# Pull Phi-2 (small, fast model)
ollama pull phi
```

## 🚀 Quick Start

### 1. Start Ollama Service

```bash
# Start Ollama in the background
ollama serve

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### 2. Start the Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Start the backend
python main.py
```

### 3. Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Start React development server
npm start
```

### 4. Test the Integration

Run the LLM integration test:

```bash
python test_llm_integration.py
```

## 🎯 Usage

### 1. Access LLM Management

1. Open your browser and go to `http://localhost:3000`
2. Navigate to "LLM Management" in the sidebar
3. Check the health status of both Dify and Ollama services

### 2. Ollama Features

- **Model Management**: View and manage local Ollama models
- **Text Generation**: Generate text using any available model
- **Chat Interface**: Interactive chat with models
- **Model Pulling**: Download new models from Ollama library

### 3. Dify Features

- **Application Management**: View and manage Dify applications
- **Workflow Execution**: Execute complex AI workflows
- **Chat Interface**: Chat with Dify applications
- **Conversation History**: View and manage conversation history

## 🔧 Advanced Configuration

### 1. Custom Ollama Models

Create custom models with specific configurations:

```bash
# Create a custom model file
cat > custom-model.modelfile << EOF
FROM llama2
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
SYSTEM "You are an architecture governance expert."
EOF

# Create the model
ollama create custom-arch-gov -f custom-model.modelfile
```

### 2. Dify Workflow Integration

Create workflows in Dify for complex architecture governance tasks:

1. **Go to Dify Dashboard**
2. **Create a new Workflow**
3. **Add nodes for:**
   - Architecture analysis
   - Compliance checking
   - Risk assessment
   - Report generation
4. **Configure inputs and outputs**
5. **Deploy the workflow**

### 3. Model Performance Optimization

For better performance with Ollama:

```bash
# Use GPU acceleration (if available)
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# Set environment variables for optimization
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_GPU_LAYERS=35
```

## 🧪 Testing

### 1. Health Check

```bash
curl http://localhost:8000/llm/health
```

Expected response:
```json
{
  "dify": {
    "status": "healthy",
    "base_url": "https://api.dify.ai/v1"
  },
  "ollama": {
    "status": "healthy",
    "base_url": "http://localhost:11434",
    "default_model": "llama2"
  },
  "overall_status": "healthy"
}
```

### 2. Model Listing

```bash
curl http://localhost:8000/llm/ollama/models
```

### 3. Text Generation

```bash
curl -X POST http://localhost:8000/llm/ollama/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain architecture governance",
    "model": "llama2",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   
   # Restart Ollama
   pkill ollama
   ollama serve
   ```

2. **Dify API Errors**
   - Verify API key is correct
   - Check workspace and application IDs
   - Ensure Dify service is accessible

3. **Model Pull Failures**
   ```bash
   # Check available models
   ollama list
   
   # Pull with verbose output
   ollama pull llama2 --verbose
   ```

4. **Memory Issues**
   ```bash
   # Check available memory
   free -h
   
   # Use smaller models
   ollama pull phi
   ```

### Performance Optimization

1. **Use Smaller Models**: Start with `phi` or `mistral` for faster responses
2. **GPU Acceleration**: Enable GPU support if available
3. **Model Quantization**: Use quantized models for better performance
4. **Connection Pooling**: Configure connection pooling for better throughput

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Dify API Documentation](https://docs.dify.ai/)
- [Model Library](https://ollama.ai/library)
- [Performance Tuning Guide](https://ollama.ai/docs/performance)

## 🎉 Next Steps

1. **Explore Models**: Try different models for different use cases
2. **Create Workflows**: Build complex AI workflows in Dify
3. **Integrate with Agents**: Connect LLM services with your AI agents
4. **Custom Training**: Fine-tune models for your specific needs
5. **Production Deployment**: Deploy to production with proper monitoring

---

**Happy LLM Integration! 🚀**
