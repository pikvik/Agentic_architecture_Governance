# Deployment Guide - Agentic AI Swarm

## Overview

This guide provides comprehensive instructions for deploying the Agentic AI Swarm system in various environments.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- Git
- At least 4GB RAM and 10GB disk space

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Architecture_Agent
```

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Create a virtual environment
- Install dependencies
- Create configuration files
- Set up directories
- Run initial tests

### 3. Configure Environment

Edit the `.env` file with your API keys and settings:

```bash
# Required API Keys
DIFY_API_KEY=your_dify_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here

# Optional: Other API keys as needed
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### 4. Start the Application

#### Development Mode
```bash
python main.py
```

#### Production Mode (Docker)
```bash
docker-compose up -d
```

### 5. Access the System

- **Web Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Detailed Deployment Options

### Option 1: Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export DIFY_API_KEY="your_key"
   export OPENAI_API_KEY="your_key"
   export SECRET_KEY="your_secret"
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### Option 2: Docker Deployment

1. **Build and Run**
   ```bash
   docker-compose up -d
   ```

2. **Check Status**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

3. **Stop Services**
   ```bash
   docker-compose down
   ```

### Option 3: Production Deployment

#### Using Docker Compose

1. **Create Production Configuration**
   ```bash
   cp docker-compose.yml docker-compose.prod.yml
   ```

2. **Edit Production Settings**
   - Set `DEBUG=False`
   - Configure external databases
   - Set up SSL certificates
   - Configure logging

3. **Deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

#### Using Kubernetes

1. **Create Kubernetes Manifests**
   ```yaml
   # deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: agentic-swarm
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: agentic-swarm
     template:
       metadata:
         labels:
           app: agentic-swarm
       spec:
         containers:
         - name: agentic-swarm
           image: agentic-swarm:latest
           ports:
           - containerPort: 8000
           env:
           - name: DIFY_API_KEY
             valueFrom:
               secretKeyRef:
                 name: api-secrets
                 key: dify-api-key
   ```

2. **Apply Manifests**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f ingress.yaml
   ```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DIFY_API_KEY` | Dify platform API key | Yes | - |
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | No | - |
| `SECRET_KEY` | Application secret key | Yes | - |
| `DATABASE_URL` | Database connection string | No | SQLite |
| `REDIS_URL` | Redis connection string | No | localhost:6379 |
| `DEBUG` | Debug mode | No | False |
| `LOG_LEVEL` | Logging level | No | INFO |
| `PORT` | Application port | No | 8000 |

### Database Configuration

#### PostgreSQL
```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

#### MongoDB
```bash
MONGODB_URL=mongodb://user:password@host:27017/database
```

#### Redis
```bash
REDIS_URL=redis://user:password@host:6379/database
```

## Monitoring and Logging

### Health Checks

- **Application Health**: `GET /health`
- **Agent Status**: `GET /agents`
- **Swarm Status**: `GET /swarm/status`

### Logging

Logs are written to:
- Console (stdout/stderr)
- File: `logs/app.log`
- Docker logs: `docker-compose logs`

### Metrics

The system provides metrics via:
- Prometheus endpoint: `/metrics`
- Custom metrics in health checks
- Performance monitoring in agent status

## Security Considerations

### API Security

1. **Use HTTPS in Production**
   ```bash
   # Configure SSL certificates
   ssl_certfile=/path/to/cert.pem
   ssl_keyfile=/path/to/key.pem
   ```

2. **API Key Management**
   - Store API keys in environment variables
   - Use Kubernetes secrets or Docker secrets
   - Rotate keys regularly

3. **Access Control**
   - Implement authentication if needed
   - Use API rate limiting
   - Configure CORS properly

### Network Security

1. **Firewall Configuration**
   ```bash
   # Allow only necessary ports
   ufw allow 8000/tcp  # Application
   ufw allow 5432/tcp  # PostgreSQL
   ufw allow 6379/tcp  # Redis
   ufw allow 27017/tcp # MongoDB
   ```

2. **Network Isolation**
   - Use Docker networks
   - Implement network policies in Kubernetes
   - Use VPN for remote access

## Troubleshooting

### Common Issues

1. **Agent Initialization Failed**
   ```bash
   # Check logs
   docker-compose logs agentic-swarm
   
   # Verify API keys
   echo $DIFY_API_KEY
   echo $OPENAI_API_KEY
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   docker-compose exec postgres psql -U postgres -d architecture_governance
   
   # Check database status
   docker-compose ps postgres
   ```

3. **Memory Issues**
   ```bash
   # Check memory usage
   docker stats
   
   # Increase memory limits
   docker-compose up -d --scale agentic-swarm=1
   ```

### Performance Optimization

1. **Resource Limits**
   ```yaml
   # docker-compose.yml
   services:
     agentic-swarm:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

2. **Caching**
   - Enable Redis caching
   - Configure agent result caching
   - Use CDN for static assets

3. **Scaling**
   ```bash
   # Scale horizontally
   docker-compose up -d --scale agentic-swarm=3
   
   # Use load balancer
   docker-compose up -d nginx
   ```

## Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U postgres architecture_governance > backup.sql

# MongoDB backup
docker-compose exec mongo mongodump --db architecture_governance --out /backup

# Redis backup
docker-compose exec redis redis-cli BGSAVE
```

### Application Backup

```bash
# Backup configuration
tar -czf config-backup.tar.gz .env config.env.example

# Backup data
tar -czf data-backup.tar.gz logs/ data/ reports/
```

### Recovery

```bash
# Restore database
docker-compose exec -T postgres psql -U postgres architecture_governance < backup.sql

# Restore configuration
tar -xzf config-backup.tar.gz

# Restart services
docker-compose restart
```

## Updates and Maintenance

### Updating the Application

1. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

2. **Rebuild and Restart**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

3. **Run Migrations**
   ```bash
   docker-compose exec agentic-swarm python -m alembic upgrade head
   ```

### Maintenance Schedule

- **Daily**: Check health status and logs
- **Weekly**: Review performance metrics
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Full system backup and recovery test

## Support

For issues and questions:

1. Check the logs: `docker-compose logs`
2. Review this documentation
3. Check the README.md file
4. Open an issue in the repository

## License

This project is licensed under the MIT License - see the LICENSE file for details.
