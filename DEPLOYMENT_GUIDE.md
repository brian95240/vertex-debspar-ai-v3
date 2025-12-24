# Vertex DebSpar AI v3.0 - Complete Cascading Deployment Guide

**Version:** 3.0.0  
**Last Updated:** December 24, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Pre-Deployment Requirements](#pre-deployment-requirements)
2. [Account Setup & Prerequisites](#account-setup--prerequisites)
3. [Environment Preparation](#environment-preparation)
4. [Cascading Installation Steps](#cascading-installation-steps)
5. [Verification & Testing](#verification--testing)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Requirements

### Minimum System Requirements
- **OS:** Ubuntu 22.04 LTS or equivalent
- **CPU:** 8 cores (4 minimum for development)
- **RAM:** 32GB (16GB minimum for development)
- **Storage:** 100GB SSD (50GB minimum for development)
- **GPU:** NVIDIA GPU with CUDA 11.0+ (optional but recommended for LLM)
- **Network:** 100Mbps internet connection

### Required Tools (Pre-installed)
- Docker 20.10+
- Docker Compose 2.0+
- kubectl 1.24+
- K3s 1.24+
- Git 2.30+
- curl 7.68+

---

## Account Setup & Prerequisites

### Step 1: Groq API Account (Required for Apex Cloud)

**Purpose:** Provides high-performance LLM inference via `llama-3.3-70b-versatile`

**Setup Instructions:**

1. Visit [Groq Console](https://console.groq.com)
2. Sign up with email or Google account
3. Verify email address
4. Navigate to **API Keys** section
5. Click **Create API Key**
6. Copy the API key (starts with `gsk_`)
7. Store securely in password manager or environment variable
8. **⚠️ IMPORTANT:** Never commit API key to Git

**Verification:**
```bash
# Test API key
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

### Step 2: Docker Hub Account (Recommended for Image Registry)

**Purpose:** Store and distribute custom Docker images

**Setup Instructions:**

1. Visit [Docker Hub](https://hub.docker.com)
2. Click **Sign Up**
3. Create account with email or Google
4. Verify email
5. Create a repository named `vertex-debspar-ai-v3`
6. Set visibility to **Private** (recommended)
7. Generate access token:
   - Go to **Account Settings** → **Security**
   - Click **New Access Token**
   - Name it: `vertex-deployment`
   - Copy token and store securely

**Verification:**
```bash
# Login to Docker Hub
docker login -u YOUR_USERNAME -p YOUR_TOKEN

# Test push (after building images)
docker tag vertex-debspar-backend:latest YOUR_USERNAME/vertex-debspar-backend:latest
docker push YOUR_USERNAME/vertex-debspar-backend:latest
```

### Step 3: GitHub Account (For Version Control)

**Purpose:** Version control and CI/CD integration

**Setup Instructions:**

1. Visit [GitHub](https://github.com)
2. Create account if needed
3. Create new repository: `vertex-debspar-ai-v3`
4. Set visibility to **Private** (recommended)
5. Generate personal access token:
   - Go to **Settings** → **Developer settings** → **Personal access tokens**
   - Click **Generate new token**
   - Select scopes: `repo`, `workflow`
   - Copy token and store securely

**Verification:**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/vertex-debspar-ai-v3.git
cd vertex-debspar-ai-v3
```

### Step 4: Kubernetes Cluster Access (For K3s)

**Purpose:** Deploy to Kubernetes cluster

**Setup Instructions:**

1. Ensure K3s is installed on your system:
   ```bash
   curl -sfL https://get.k3s.io | sh -
   ```

2. Verify K3s is running:
   ```bash
   sudo systemctl status k3s
   ```

3. Configure kubectl:
   ```bash
   mkdir -p ~/.kube
   sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
   sudo chown $USER:$USER ~/.kube/config
   chmod 600 ~/.kube/config
   ```

4. Verify cluster access:
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

### Step 5: NVIDIA GPU Support (Optional but Recommended)

**Purpose:** Accelerate LLM inference

**Setup Instructions:**

1. Install NVIDIA drivers:
   ```bash
   sudo apt-get update
   sudo apt-get install -y nvidia-driver-530
   nvidia-smi  # Verify installation
   ```

2. Install NVIDIA Container Runtime:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
     sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-runtime
   ```

3. Configure Docker to use NVIDIA runtime:
   ```bash
   sudo tee /etc/docker/daemon.json > /dev/null <<EOF
   {
     "runtimes": {
       "nvidia": {
         "path": "nvidia-container-runtime",
         "runtimeArgs": []
       }
     },
     "default-runtime": "runtimes"
   }
   EOF
   sudo systemctl restart docker
   ```

4. Verify GPU access:
   ```bash
   docker run --rm --gpus all nvidia/cuda:11.0-runtime nvidia-smi
   ```

### Step 6: Environment Variables Setup

**Create `.env` file in project root:**

```bash
# Groq API Configuration
APEX_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE
APEX_API_URL=https://api.groq.com/openai/v1/chat/completions

# Local LLM Configuration
VLLM_ENDPOINT=http://vllm-warm:8000/v1/chat/completions
VLLM_MODEL=Qwen/Qwen2.5-14B-Instruct

# Docker Registry (optional)
DOCKER_REGISTRY=YOUR_USERNAME
DOCKER_REGISTRY_TOKEN=YOUR_TOKEN

# Kubernetes Configuration
K3S_NAMESPACE=debate-vertex
K3S_KUBECONFIG=~/.kube/config

# Development Settings
DEBUG=false
LOG_LEVEL=INFO
```

**⚠️ SECURITY WARNING:**
- Never commit `.env` to Git
- Add `.env` to `.gitignore`
- Use secrets management in production (Vault, AWS Secrets Manager, etc.)

---

## Environment Preparation

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/vertex-debspar-ai-v3.git
cd vertex-debspar-ai-v3
```

### Step 2: Verify System Dependencies

```bash
# Check OS
lsb_release -a  # Should show Ubuntu 22.04

# Check Python
python3 --version  # Should be 3.10+
python3.11 --version  # Recommended

# Check Node.js
node --version  # Should be 18+
npm --version

# Check Docker
docker --version
docker ps  # Verify daemon is running

# Check Kubernetes
kubectl version --client
kubectl cluster-info
```

### Step 3: Create Project Directories

```bash
# Create necessary directories
mkdir -p ~/.vertex-debspar/{logs,data,secrets}
mkdir -p /opt/vertex-debspar/{backend,frontend,k3s}

# Set permissions
chmod 700 ~/.vertex-debspar
chmod 700 /opt/vertex-debspar
```

### Step 4: Load Environment Variables

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your values
nano .env

# Source environment variables
source .env

# Verify
echo $APEX_API_KEY  # Should show your key
```

---

## Cascading Installation Steps

### Phase 1: Backend Setup

#### Step 1.1: Install Python Dependencies

```bash
cd backend

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --no-dev

# Verify installation
poetry show  # List all installed packages
```

#### Step 1.2: Run Backend Tests

```bash
# Run smoke tests
python3.11 test_step3_backend_smoke.py

# Expected output: "✓ STEP 3 PASS - All backend smoke tests passed!"
```

#### Step 1.3: Build Backend Docker Image

```bash
cd ..

# Build image
docker build -t vertex-debspar-backend:latest -f Dockerfile.backend .

# Verify build
docker images | grep vertex-debspar-backend

# Test image
docker run --rm vertex-debspar-backend:latest python -c "import debate_vertex; print('✓ Backend image OK')"
```

### Phase 2: Frontend Setup

#### Step 2.1: Install NPM Dependencies

```bash
cd frontend

# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

#### Step 2.2: Run Frontend Tests

```bash
# Run integration tests
cd ..
python3.11 test_step4_frontend_integration.py

# Expected output: "✓ STEP 4 PASS - Frontend integration tests passed!"
```

#### Step 2.3: Build Frontend

```bash
cd frontend

# Production build
npm run build

# Verify build output
ls -la dist/
# Should contain: index.html, assets/

# Test build size
du -sh dist/
# Should be < 200KB
```

#### Step 2.4: Build Frontend Docker Image

```bash
cd ..

# Build image
docker build -t vertex-debspar-frontend:latest -f Dockerfile.frontend .

# Verify build
docker images | grep vertex-debspar-frontend

# Test image
docker run --rm -p 8080:80 vertex-debspar-frontend:latest &
sleep 2
curl -s http://localhost:8080 | head -20
kill %1
```

### Phase 3: Kubernetes Setup

#### Step 3.1: Create Namespace

```bash
# Apply namespace
kubectl apply -f k3s/namespace.yaml

# Verify
kubectl get namespace debate-vertex
```

#### Step 3.2: Create Secrets

```bash
# Create Groq API key secret
kubectl create secret generic apex-secret \
  --from-literal=groq_key=$APEX_API_KEY \
  -n debate-vertex

# Verify secret
kubectl get secrets -n debate-vertex
```

#### Step 3.3: Load Docker Images into K3s

```bash
# For local K3s, import images
docker save vertex-debspar-backend:latest | sudo k3s ctr images import -
docker save vertex-debspar-frontend:latest | sudo k3s ctr images import -

# Or push to registry and update manifests
docker tag vertex-debspar-backend:latest $DOCKER_REGISTRY/vertex-debspar-backend:latest
docker push $DOCKER_REGISTRY/vertex-debspar-backend:latest

# Update deployment manifests with registry URL
sed -i "s|debate-vertex-backend:latest|$DOCKER_REGISTRY/vertex-debspar-backend:latest|g" k3s/deployment-hot.yaml
```

#### Step 3.4: Deploy Backend

```bash
# Apply deployment
kubectl apply -f k3s/deployment-hot.yaml

# Wait for deployment
kubectl rollout status deployment/orchestrator-hot -n debate-vertex

# Verify
kubectl get pods -n debate-vertex
kubectl logs -n debate-vertex deployment/orchestrator-hot
```

#### Step 3.5: Deploy LLM Service

```bash
# Apply deployment
kubectl apply -f k3s/deployment-warm-llm.yaml

# Wait for deployment (may take several minutes for model download)
kubectl rollout status deployment/vllm-warm -n debate-vertex

# Monitor progress
kubectl logs -n debate-vertex deployment/vllm-warm -f

# Verify
kubectl get pods -n debate-vertex
```

#### Step 3.6: Configure Auto-scaling

```bash
# Install KEDA (if not already installed)
kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.13.0/keda-2.13.0.yaml

# Wait for KEDA to be ready
kubectl wait --for=condition=ready pod -l app=keda-operator -n keda --timeout=300s

# Apply scaling configuration
kubectl apply -f k3s/keda-scaledobject-llm.yaml

# Verify
kubectl get scaledobjects -n debate-vertex
```

### Phase 4: Service Exposure

#### Step 4.1: Expose Backend Service

```bash
# Get service info
kubectl get svc -n debate-vertex

# Port-forward for testing (development)
kubectl port-forward -n debate-vertex svc/orchestrator-hot 8000:80 &

# Or create ingress for production
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vertex-ingress
  namespace: debate-vertex
spec:
  rules:
  - host: debate.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: orchestrator-hot
            port:
              number: 80
EOF
```

#### Step 4.2: Expose Frontend Service

```bash
# Create NodePort service for frontend
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: debate-vertex
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
EOF

# Get access URL
kubectl get svc -n debate-vertex frontend-service
```

---

## Verification & Testing

### Step 1: Health Checks

```bash
# Backend health
curl -s http://localhost:8000/health | jq .

# Expected response:
# {
#   "status": "vertex_active",
#   "mode": "hybrid"
# }
```

### Step 2: WebSocket Connection Test

```bash
# Install wscat (if not already installed)
npm install -g wscat

# Test WebSocket connection
wscat -c ws://localhost:8000/ws/debate

# Send test message
> {"text": "Hello, Vertex!", "timer": 30}

# Expected response:
# {"type": "status", "pressure": 2.0, "tier": "LOCAL_WARM"}
# {"type": "response", "text": "...response text..."}
```

### Step 3: Frontend Accessibility

```bash
# Test frontend
curl -s http://localhost:30080 | head -20

# Should return HTML with React app
```

### Step 4: Full Integration Test

```bash
# Run comprehensive test
python3.11 << 'EOF'
import asyncio
import json
import websockets

async def test_system():
    print("Testing Vertex DebSpar AI v3.0...")
    
    # Test 1: Backend health
    print("\n[1] Testing backend health...")
    import urllib.request
    try:
        response = urllib.request.urlopen('http://localhost:8000/health')
        data = json.loads(response.read())
        assert data['status'] == 'vertex_active'
        print("✓ Backend is healthy")
    except Exception as e:
        print(f"✗ Backend health check failed: {e}")
        return False
    
    # Test 2: WebSocket connection
    print("\n[2] Testing WebSocket connection...")
    try:
        async with websockets.connect('ws://localhost:8000/ws/debate') as ws:
            # Send message
            await ws.send(json.dumps({
                "text": "This is a test argument",
                "timer": 30.0
            }))
            
            # Receive responses
            responses = []
            for _ in range(2):  # Expect status and response
                msg = await asyncio.wait_for(ws.recv(), timeout=10)
                responses.append(json.loads(msg))
            
            # Verify responses
            assert any(r['type'] == 'status' for r in responses)
            assert any(r['type'] == 'response' for r in responses)
            print("✓ WebSocket communication successful")
            print(f"  Received {len(responses)} messages")
    except Exception as e:
        print(f"✗ WebSocket test failed: {e}")
        return False
    
    print("\n✓ All integration tests passed!")
    return True

asyncio.run(test_system())
EOF
```

---

## Production Deployment

### Step 1: Pre-Production Checklist

- [ ] All tests pass (Step 3 and Step 4)
- [ ] Groq API key is valid and has sufficient quota
- [ ] Docker images are built and tested
- [ ] Kubernetes cluster is healthy
- [ ] GPU support is verified (if using GPU)
- [ ] Network connectivity is confirmed
- [ ] Monitoring is configured
- [ ] Backups are in place
- [ ] Security policies are reviewed
- [ ] Load testing is completed

### Step 2: Deploy to Production

```bash
# Set production environment
export ENVIRONMENT=production
export LOG_LEVEL=WARNING

# Update manifests with production settings
sed -i 's/replicas: 1/replicas: 3/g' k3s/deployment-hot.yaml
sed -i 's/replicas: 1/replicas: 2/g' k3s/deployment-warm-llm.yaml

# Apply production manifests
kubectl apply -f k3s/

# Verify deployment
kubectl get all -n debate-vertex

# Monitor logs
kubectl logs -n debate-vertex -l app=orchestrator -f
```

### Step 3: Configure Monitoring

```bash
# Install Prometheus
kubectl apply -f https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.68.0/bundle.yaml

# Create ServiceMonitor for Vertex
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: vertex-monitor
  namespace: debate-vertex
spec:
  selector:
    matchLabels:
      app: orchestrator
  endpoints:
  - port: metrics
    interval: 30s
EOF
```

### Step 4: Setup Alerting

```bash
# Configure alerts for critical metrics
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: vertex-alerts
  namespace: debate-vertex
spec:
  groups:
  - name: vertex
    rules:
    - alert: HighPressureScore
      expr: debate_pressure_score > 8.0
      for: 5m
      annotations:
        summary: "High debate pressure detected"
    - alert: LLMLatency
      expr: llm_response_time_ms > 5000
      for: 5m
      annotations:
        summary: "LLM response latency is high"
EOF
```

---

## Troubleshooting

### Issue: Backend fails to start

**Symptoms:**
```
Error: ModuleNotFoundError: No module named 'debate_vertex'
```

**Solution:**
```bash
# Verify Python path
export PYTHONPATH=/path/to/backend/src:$PYTHONPATH

# Reinstall dependencies
cd backend
poetry install --no-dev

# Run backend directly
python -m uvicorn debate_vertex.main:app --host 0.0.0.0 --port 8000
```

### Issue: Frontend build fails

**Symptoms:**
```
error during build: [vite:terser] terser not found
```

**Solution:**
```bash
cd frontend
npm install --save-dev terser
npm run build
```

### Issue: WebSocket connection refused

**Symptoms:**
```
WebSocket connection to 'ws://localhost:8000/ws/debate' failed
```

**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check port availability
netstat -tlnp | grep 8000

# Restart backend
kubectl restart deployment orchestrator-hot -n debate-vertex
```

### Issue: GPU not detected in LLM container

**Symptoms:**
```
No NVIDIA GPUs detected
```

**Solution:**
```bash
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.0-runtime nvidia-smi

# Check K3s GPU plugin
kubectl get nodes -o wide
kubectl describe node | grep -A 5 "Allocated resources"

# Update deployment to request GPU
kubectl patch deployment vllm-warm -n debate-vertex --type='json' -p='[
  {"op": "add", "path": "/spec/template/spec/containers/0/resources/limits/nvidia.com~1gpu", "value": "1"}
]'
```

### Issue: Out of memory errors

**Symptoms:**
```
OOMKilled
```

**Solution:**
```bash
# Check memory usage
kubectl top nodes
kubectl top pods -n debate-vertex

# Increase pod memory limits
kubectl set resources deployment vllm-warm -n debate-vertex --limits=memory=16Gi

# Or reduce model size
# Edit deployment-warm-llm.yaml and change model to smaller variant
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor logs for errors
- Check system health
- Verify API quota usage

**Weekly:**
- Review performance metrics
- Check for security updates
- Backup configuration

**Monthly:**
- Update dependencies
- Review and optimize costs
- Test disaster recovery

### Backup Procedure

```bash
# Backup configuration
kubectl get all -n debate-vertex -o yaml > backup-$(date +%Y%m%d).yaml

# Backup secrets (encrypted)
kubectl get secrets -n debate-vertex -o yaml | \
  gpg --encrypt --recipient your-key-id > secrets-backup-$(date +%Y%m%d).gpg

# Backup persistent data
tar -czf data-backup-$(date +%Y%m%d).tar.gz ~/.vertex-debspar/data/
```

### Update Procedure

```bash
# Update dependencies
poetry update
npm update

# Rebuild images
docker build -t vertex-debspar-backend:latest -f Dockerfile.backend .
docker build -t vertex-debspar-frontend:latest -f Dockerfile.frontend .

# Redeploy
kubectl rollout restart deployment/orchestrator-hot -n debate-vertex
kubectl rollout restart deployment/vllm-warm -n debate-vertex

# Verify
kubectl rollout status deployment/orchestrator-hot -n debate-vertex
```

---

## Support & Resources

- **Documentation:** [GitHub Wiki](https://github.com/YOUR_USERNAME/vertex-debspar-ai-v3/wiki)
- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/vertex-debspar-ai-v3/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/vertex-debspar-ai-v3/discussions)
- **Email:** support@vertex-debspar.ai

---

**Version:** 3.0.0  
**Last Updated:** December 24, 2025  
**Status:** Production Ready  
**Maintained By:** Vertex DebSpar AI Team
