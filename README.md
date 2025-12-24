# Vertex DebSpar AI v3.0

**Advanced Hybrid Debate System with Thermal Tier Optimization**

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE_GPLv3)
[![Commercial License Available](https://img.shields.io/badge/Commercial%20License-Available-green.svg)](LICENSE_COMMERCIAL)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![React 18+](https://img.shields.io/badge/React-18%2B-blue)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-green)](https://fastapi.tiangolo.com/)

---

## Overview

Vertex DebSpar AI v3.0 is a sophisticated hybrid debate system that combines local language models with cloud-based LLM APIs to create dynamic, real-time debate experiences. The system implements a **thermal tier architecture** (HOT, WARM, COLD) to optimize performance and cost across different debate intensities.

### Key Features

- **Hybrid Architecture:** Seamlessly switches between local models and Groq API based on debate intensity
- **Thermal Tier System:** HOT (high-intensity), WARM (moderate), COLD (low-intensity) debate modes
- **Real-time WebSocket Communication:** Live debate streaming and rebuttal timing
- **Pressure Estimation:** Semantic analysis-based debate pressure scoring
- **Kubernetes Ready:** K3s manifests for scalable cloud deployment
- **GPU Optimized:** NVIDIA GPU support for local model inference
- **Production Ready:** Comprehensive testing, monitoring, and error handling

---

## Interactive Demo

🎮 **[Try the Interactive Demo](demo/INTERACTIVE_DEMO.md)** - Experience Vertex DebSpar AI v3.0 in action with a simulated debate session!

The demo showcases:
- Real-time pressure detection (0-10 scale)
- Hybrid routing between local and cloud models
- Rebuttal timer simulation
- Message streaming interface
- Visual architecture diagrams

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (for containerization)
- Kubernetes/K3s (for production deployment)
- Groq API key (for cloud LLM access)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/vertex-debspar-ai-v3.git
cd vertex-debspar-ai-v3

# Install backend dependencies
cd backend
poetry install

# Install frontend dependencies
cd ../frontend
npm install

# Build frontend
npm run build
```

### Running Locally

```bash
# Terminal 1: Start backend
cd backend
poetry run uvicorn src.debate_vertex.main:app --reload --port 8000

# Terminal 2: Start frontend dev server
cd frontend
npm run dev
```

Visit `http://localhost:5173` to access the application.

---

## Architecture

### Backend (FastAPI)

```
backend/src/debate_vertex/
├── main.py                 # FastAPI application entry point
├── models/
│   ├── state.py           # Debate state management (Pydantic models)
│   ├── thermal.py         # Thermal tier enumeration
│   ├── deb8.py            # Core debate loop logic
│   ├── brain_router.py    # Hybrid routing (local vs. Groq)
│   └── cue_extractors.py  # Pressure estimation algorithms
└── routes/
    └── debate.py          # WebSocket and REST endpoints
```

### Frontend (React + TypeScript)

```
frontend/src/
├── main.tsx               # React entry point
├── App.tsx                # Main application component
├── components/
│   ├── DebateInterface.tsx    # Debate UI container
│   ├── MessageStream.tsx      # Real-time message display
│   └── RebuttalTimer.tsx      # Rebuttal countdown timer
└── styles/
    └── index.css          # Tailwind CSS configuration
```

### Infrastructure

```
k3s/
├── namespace.yaml              # Kubernetes namespace
├── deployment-hot.yaml         # HOT tier deployment
├── deployment-warm-llm.yaml    # WARM tier with LLM
└── keda-scaledobject-llm.yaml  # Auto-scaling configuration
```

---

## Thermal Tier System

The system uses three thermal tiers to optimize performance and cost:

### HOT Tier
- **Purpose:** High-intensity debates with rapid exchanges
- **Model:** Local vLLM (optimized for speed)
- **Latency:** <100ms response time
- **Cost:** Minimal (local compute only)
- **Use Case:** Real-time competitive debates

### WARM Tier
- **Purpose:** Moderate-intensity debates with balanced quality
- **Model:** Groq API (fast cloud LLM)
- **Latency:** 100-500ms response time
- **Cost:** Medium (pay-per-API-call)
- **Use Case:** Standard debate sessions

### COLD Tier
- **Purpose:** Low-intensity debates with maximum quality
- **Model:** Groq API with extended context
- **Latency:** 500ms-2s response time
- **Cost:** Higher (more processing)
- **Use Case:** Deep analysis, research debates

---

## Dual Licensing

Vertex DebSpar AI v3.0 is offered under a **dual licensing model** to maximize flexibility and monetization:

### Option 1: GPLv3 Open-Source License (Free)

**License File:** `LICENSE_GPLv3`

**Terms:**
- ✓ Free to use, modify, and distribute
- ✓ Full source code access
- ✗ Must open-source any modifications
- ✗ Cannot use in proprietary products without sharing code
- ✗ No commercial SaaS deployment without open-sourcing

**Best For:**
- Academic research
- Open-source projects
- Community contributions
- Non-commercial use

**How to Use:**
```bash
# Use under GPLv3 terms
# All modifications must be shared with the community
```

### Option 2: Commercial License (Paid)

**License File:** `LICENSE_COMMERCIAL`

**Available Tiers:**

#### Startup License - $2,999/year
- Up to 5 developers
- Single production environment
- Email support (24-hour response)
- All updates included

#### Business License - $9,999/year
- Up to 25 developers
- 3 production environments
- Priority support (4-hour response)
- 8 hours training included

#### Enterprise License - Custom (starting $29,999/year)
- Unlimited developers
- Unlimited deployments
- Dedicated account manager
- 24/7 phone support
- Custom development (40 hours)
- Unlimited training

**Terms:**
- ✓ Proprietary modifications allowed
- ✓ Commercial SaaS deployment permitted
- ✓ Closed-source applications allowed
- ✓ Professional support included
- ✓ Indemnification included

**Best For:**
- Commercial products
- SaaS applications
- Enterprise deployments
- Proprietary modifications

**How to Purchase:**
```bash
# Contact licensing team
Email: licensing@vertex-debspar.ai
Website: https://vertex-debspar.ai/licensing
```

---

## Choosing a License

| Scenario | Recommended License |
|----------|-------------------|
| Academic research project | GPLv3 (Free) |
| Open-source contribution | GPLv3 (Free) |
| Internal company tool | Commercial |
| Commercial SaaS product | Commercial |
| Proprietary modifications | Commercial |
| Community-driven project | GPLv3 (Free) |
| Enterprise deployment | Enterprise Commercial |

---

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration
HOT_MODEL=vllm/vllm-openai:latest
WARM_MODEL=mixtral-8x7b-32768
COLD_MODEL=mixtral-8x7b-32768

# Debate Configuration
DEFAULT_THERMAL_TIER=WARM
MAX_DEBATE_DURATION=3600
PRESSURE_THRESHOLD=0.75

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### Docker Deployment

```bash
# Build backend image
docker build -t vertex-debspar-backend:latest -f Dockerfile.backend .

# Build frontend image
docker build -t vertex-debspar-frontend:latest -f Dockerfile.frontend .

# Run with Docker Compose
docker-compose up -d
```

### Kubernetes Deployment

```bash
# Create namespace
kubectl apply -f k3s/namespace.yaml

# Deploy HOT tier
kubectl apply -f k3s/deployment-hot.yaml

# Deploy WARM tier with LLM
kubectl apply -f k3s/deployment-warm-llm.yaml

# Configure auto-scaling
kubectl apply -f k3s/keda-scaledobject-llm.yaml
```

---

## API Documentation

### WebSocket Endpoint

**URL:** `ws://localhost:8000/ws/debate/{debate_id}`

**Message Format:**

```json
{
  "type": "message",
  "content": "Your debate message here",
  "thermal_tier": "WARM",
  "timestamp": "2025-12-24T10:30:00Z"
}
```

### REST Endpoints

#### Start Debate
```bash
POST /api/debates/start
Content-Type: application/json

{
  "topic": "AI Ethics",
  "thermal_tier": "WARM",
  "duration": 1800
}
```

#### Get Debate Status
```bash
GET /api/debates/{debate_id}
```

#### End Debate
```bash
POST /api/debates/{debate_id}/end
```

---

## Performance Metrics

### Response Times
- **HOT Tier:** <100ms average
- **WARM Tier:** 150-300ms average
- **COLD Tier:** 500-1500ms average

### Throughput
- **HOT Tier:** 100+ debates/minute
- **WARM Tier:** 50+ debates/minute
- **COLD Tier:** 20+ debates/minute

### Resource Usage
- **Backend:** 2-4GB RAM, 2-4 CPU cores
- **Frontend:** <50MB bundle size
- **GPU (optional):** 8GB VRAM for local models

---

## Testing

### Run Backend Tests
```bash
cd backend
poetry run pytest tests/ -v
```

### Run Frontend Tests
```bash
cd frontend
npm run test
```

### Run Integration Tests
```bash
python3 test_step3_backend_smoke.py
python3 test_step4_frontend_integration.py
```

---

## Deployment

### Production Checklist

- [ ] Set environment variables securely
- [ ] Configure HTTPS/TLS certificates
- [ ] Set up monitoring and logging
- [ ] Configure backup and disaster recovery
- [ ] Enable rate limiting and DDoS protection
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling
- [ ] Test failover procedures

### Monitoring

The system includes comprehensive logging and monitoring:

```bash
# View backend logs
kubectl logs -f deployment/vertex-debspar-backend -n vertex-debspar

# View frontend logs
kubectl logs -f deployment/vertex-debspar-frontend -n vertex-debspar

# Monitor metrics
kubectl top pods -n vertex-debspar
```

---

## Support

### For GPLv3 Users
- GitHub Issues: https://github.com/your-username/vertex-debspar-ai-v3/issues
- Community Discussions: https://github.com/your-username/vertex-debspar-ai-v3/discussions
- Documentation: https://docs.vertex-debspar.ai

### For Commercial License Holders
- Email Support: support@vertex-debspar.ai
- Phone Support: +1-XXX-XXX-XXXX (Enterprise tier)
- Dedicated Account Manager (Enterprise tier)
- Priority Bug Fixes: 24-48 hours

---

## Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Note:** All contributions must be compatible with GPLv3 licensing.

---

## Roadmap

### Version 3.1 (Q1 2026)
- [ ] Multi-language support
- [ ] Advanced debate analytics
- [ ] Custom model integration
- [ ] Mobile app

### Version 3.2 (Q2 2026)
- [ ] Real-time collaboration features
- [ ] Advanced visualization
- [ ] API rate limiting improvements
- [ ] Performance optimizations

### Version 4.0 (Q3 2026)
- [ ] Distributed debate system
- [ ] Advanced AI reasoning
- [ ] Enterprise features
- [ ] White-label solution

---

## License Summary

| Aspect | GPLv3 | Commercial |
|--------|-------|-----------|
| Cost | Free | $2,999 - Custom |
| Source Code | Required | Included |
| Modifications | Must Share | Proprietary |
| Commercial Use | Must Open-Source | Allowed |
| Support | Community | Professional |
| Warranty | None | Limited |
| Indemnification | None | Included |

**Choose your license:** [GPLv3](LICENSE_GPLv3) or [Commercial](LICENSE_COMMERCIAL)

---

## Frequently Asked Questions

### Q: Can I use this commercially under GPLv3?
**A:** Yes, but any modifications must be shared with the community. For proprietary use without sharing code, purchase a Commercial License.

### Q: Do I need a Commercial License for internal use?
**A:** No, internal use is allowed under GPLv3. You only need a Commercial License if you want to keep modifications proprietary.

### Q: Can I modify the software?
**A:** Yes, under both licenses. Under GPLv3, modifications must be shared. Under Commercial License, modifications are proprietary.

### Q: What support is included?
**A:** GPLv3 users get community support. Commercial License holders get professional support based on their tier.

### Q: Can I sublicense the software?
**A:** Not under GPLv3. Under Commercial License, sublicensing is available for Enterprise tier customers.

---

## Security

### Reporting Security Issues

Please email security@vertex-debspar.ai with details of any security vulnerabilities. Do not open public issues for security problems.

### Security Best Practices

- Keep dependencies updated
- Use environment variables for secrets
- Enable HTTPS in production
- Implement rate limiting
- Regular security audits
- Monitor logs for suspicious activity

---

## Acknowledgments

- FastAPI team for the excellent web framework
- React team for the UI library
- Groq for the fast LLM API
- Kubernetes community for orchestration
- All contributors and users

---

## Contact

- **Website:** https://vertex-debspar.ai
- **Email:** info@vertex-debspar.ai
- **Licensing:** licensing@vertex-debspar.ai
- **Support:** support@vertex-debspar.ai
- **GitHub:** https://github.com/your-username/vertex-debspar-ai-v3

---

## License

This project is dual-licensed under:

1. **GPLv3** - For open-source use (free)
2. **Commercial License** - For proprietary use (paid)

See [LICENSE_GPLv3](LICENSE_GPLv3) and [LICENSE_COMMERCIAL](LICENSE_COMMERCIAL) for details.

---

**Vertex DebSpar AI v3.0**  
*Advanced Hybrid Debate System*  
**Version:** 3.0.0  
**Last Updated:** December 24, 2025  
**Status:** Production Ready ✓
