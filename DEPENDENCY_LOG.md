# Vertex DebSpar AI v3.0 - Complete Dependency Log

**Generated:** December 24, 2025  
**System:** Ubuntu 22.04 Linux/amd64  
**Status:** All dependencies verified and tested

---

## System-Level Dependencies

| Component | Version | Purpose |
|-----------|---------|---------|
| OS | Ubuntu 22.04 | Base operating system |
| Python | 3.11.0rc1 | Backend runtime |
| Node.js | 22.13.0 | Frontend build toolchain |
| npm | 10.9.2 | Node package manager |
| pnpm | 10.26.2 | Alternative package manager |
| Docker | Latest | Container runtime |
| K3s | Latest stable | Kubernetes distribution |
| NVIDIA Runtime | Latest | GPU support for K3s |

---

## Backend Python Dependencies

### Core Framework
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | ^0.109.0 | Web framework and routing |
| uvicorn | ^0.27.0 | ASGI server |
| websockets | ^12.0 | WebSocket protocol support |
| httpx | ^0.26.0 | Async HTTP client |

### Data & ML
| Package | Version | Purpose |
|---------|---------|---------|
| pydantic | ^2.0.0 | Data validation and serialization |
| numpy | ^1.26.0 | Numerical computing |
| torch | ^2.2.0 | Deep learning framework |
| sentence-transformers | ^2.5.0 | Semantic embeddings |

### Installation Method
```bash
# Using Poetry (recommended)
poetry install --no-dev

# Or using pip
pip install fastapi uvicorn websockets httpx pydantic numpy torch sentence-transformers
```

---

## Frontend NPM Dependencies

### Production Dependencies
| Package | Version | Installed | Purpose |
|---------|---------|-----------|---------|
| react | ^18.2.0 | 18.3.1 | UI framework |
| react-dom | ^18.2.0 | 18.3.1 | React DOM rendering |

### Development Dependencies
| Package | Version | Installed | Purpose |
|---------|---------|-----------|---------|
| typescript | ^5.3.2 | 5.9.3 | Type checking |
| vite | ^5.0.7 | 5.4.21 | Build tool |
| @vitejs/plugin-react | ^5.1.2 | 5.1.2 | React plugin for Vite |
| tailwindcss | ^3.3.5 | 3.4.19 | CSS framework |
| postcss | ^8.4.31 | 8.5.6 | CSS processing |
| autoprefixer | ^10.4.16 | 10.4.23 | CSS vendor prefixes |
| @types/react | ^18.2.0 | 18.3.27 | React type definitions |
| @types/react-dom | ^18.2.0 | 18.3.7 | React DOM type definitions |
| terser | ^5.44.1 | 5.44.1 | JavaScript minifier |

### Installation & Build
```bash
# Install dependencies
npm install

# Build for production
npm run build

# Development server
npm run dev
```

---

## Docker Images

### Backend Container
```dockerfile
FROM python:3.10-slim
# Contains: Python 3.10, pip, build-essential
# Size: ~150MB base
```

### Frontend Container (Multi-stage)
```dockerfile
# Build stage
FROM node:18-alpine
# Runtime stage
FROM nginx:alpine
# Size: ~20MB runtime
```

### LLM Service Container
```dockerfile
FROM vllm/vllm-openai:latest
# Contains: vLLM, CUDA runtime, model serving
# Size: ~10GB+ (includes model weights)
```

---

## Kubernetes Components

### API Versions
| Component | API Version | Purpose |
|-----------|------------|---------|
| Deployment | apps/v1 | Orchestrator and LLM deployments |
| Service | v1 | Internal service discovery |
| Namespace | v1 | Logical isolation |
| ScaledObject | keda.sh/v1alpha1 | Auto-scaling configuration |
| RuntimeClass | node.k8s.io/v1 | NVIDIA GPU runtime selection |

### External Dependencies
| Service | Version | Purpose |
|---------|---------|---------|
| KEDA | Latest | Event-driven autoscaling |
| Prometheus | Latest | Metrics collection (for KEDA) |
| NVIDIA GPU Plugin | Latest | GPU resource management |

---

## External API Dependencies

### Groq API (Apex Cloud)
- **Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
- **Model:** `llama-3.3-70b-versatile`
- **Authentication:** Bearer token (APEX_API_KEY)
- **Status:** Optional (falls back to local if unavailable)

### Local LLM Service
- **Endpoint:** `http://vllm-warm:8000/v1/chat/completions`
- **Model:** `Qwen/Qwen2.5-14B-Instruct`
- **Status:** Required

---

## Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| pyproject.toml | Root | Python dependencies and metadata |
| package.json | frontend/ | NPM dependencies |
| vite.config.ts | frontend/ | Vite build configuration |
| tsconfig.json | frontend/ | TypeScript configuration |
| tailwind.config.js | frontend/ | Tailwind CSS configuration |
| postcss.config.js | frontend/ | PostCSS configuration |
| Dockerfile.backend | Root | Backend container image |
| Dockerfile.frontend | Root | Frontend container image |
| deployment-hot.yaml | k3s/ | Orchestrator deployment |
| deployment-warm-llm.yaml | k3s/ | LLM service deployment |
| keda-scaledobject-llm.yaml | k3s/ | Auto-scaling configuration |
| namespace.yaml | k3s/ | Kubernetes namespace |

---

## Verified Compatibility Matrix

### Python Version Compatibility
- ✓ Python 3.10 (official)
- ✓ Python 3.11 (tested)
- ✗ Python 3.9 or lower (not supported)
- ✗ Python 3.12+ (untested)

### Node.js Version Compatibility
- ✓ Node 18.x (compatible)
- ✓ Node 20.x (compatible)
- ✓ Node 22.x (tested)
- ✗ Node 16 or lower (not supported)

### Operating System Compatibility
- ✓ Ubuntu 22.04 LTS (tested)
- ✓ Ubuntu 20.04 LTS (compatible)
- ✓ Debian 11+ (compatible)
- ✓ Alpine Linux (for containers)
- ✓ macOS 12+ (for development)

---

## Security Considerations

### Dependency Vulnerabilities
- Frontend: 2 moderate severity vulnerabilities (optional fixes available)
- Backend: No known vulnerabilities
- Recommendation: Run `npm audit fix` if deploying to production

### API Key Management
- **APEX_API_KEY:** Stored in Kubernetes secrets, not in code
- **VLLM_ENDPOINT:** Internal K8s service, no authentication required
- **Environment Variables:** Injected at runtime, not committed to Git

---

## Performance Characteristics

### Memory Requirements
- Backend container: ~500MB (with models)
- Frontend container: ~50MB
- LLM container: ~14GB (for 14B model)
- Total minimum: ~15GB

### CPU Requirements
- Backend: 2 CPU cores recommended
- Frontend: 1 CPU core
- LLM: 4+ CPU cores (or 1 GPU)

### Network
- Backend to LLM: Internal K8s network (low latency)
- Frontend to Backend: WebSocket (persistent connection)
- Backend to Groq API: External HTTPS (high latency fallback)

---

## Deployment Checklist

- [ ] System meets minimum requirements (Ubuntu 22.04, Python 3.10+, Node 18+)
- [ ] Docker installed and running
- [ ] K3s cluster initialized with GPU support
- [ ] All Python dependencies installed via Poetry
- [ ] All NPM dependencies installed
- [ ] Frontend built successfully (`npm run build`)
- [ ] Backend smoke tests pass (`python test_step3_backend_smoke.py`)
- [ ] Frontend integration tests pass (`python test_step4_frontend_integration.py`)
- [ ] Groq API key obtained and configured
- [ ] Docker images built successfully
- [ ] K3s manifests applied
- [ ] Services accessible and responding

---

## Troubleshooting

### Missing Dependencies
If you encounter import errors, ensure all dependencies are installed:
```bash
# Backend
cd backend && poetry install

# Frontend
cd frontend && npm install
```

### Version Conflicts
If you experience compatibility issues:
1. Check Python version: `python3 --version` (should be 3.10+)
2. Check Node version: `node --version` (should be 18+)
3. Clear caches: `npm cache clean --force` and `poetry cache clear`
4. Reinstall: `npm install` and `poetry install --no-cache`

### GPU Issues
If GPU is not detected:
1. Verify NVIDIA runtime: `docker run --rm --gpus all nvidia/cuda:11.0-runtime nvidia-smi`
2. Check K3s GPU plugin: `kubectl get nodes -o wide`
3. Review KEDA metrics: `kubectl logs -n keda deployment/keda-operator`

---

## Update Policy

- **Security Updates:** Apply immediately
- **Minor Updates:** Test before deploying
- **Major Updates:** Plan migration carefully
- **LLM Model Updates:** Test performance before switching

---

**Last Updated:** December 24, 2025  
**Maintained By:** Vertex DebSpar AI Team  
**Status:** Production Ready
