---
title: Vertex DebSpar AI v3.0 Demo
emoji: 🎯
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: gpl-3.0
---

# Vertex DebSpar AI v3.0 - Interactive Demo

This is a **mock demo** of the Vertex DebSpar AI v3.0 hybrid debate system.

## Features

- **Real-time Pressure Detection**: Analyzes debate intensity (0-10 scale) based on assertive language, tension words, and debate progression
- **Hybrid Routing Simulation**: Routes to APEX_CLOUD (high pressure >7.2) or LOCAL_WARM (low pressure ≤7.2)
- **Adaptive Responses**: Mock responses that adapt to debate pressure and intensity
- **Message Streaming**: Character-by-character response streaming for realistic experience

## How It Works

1. **Enter your argument** in the chat input
2. **System analyzes** your message for debate pressure
3. **Routing decision** is made based on pressure threshold
4. **Mock response** is generated and streamed back

## Try It!

Make increasingly assertive arguments to see the pressure rise and routing switch from LOCAL_WARM to APEX_CLOUD!

**Example arguments:**
- "AI is dangerous because it could lead to job loss and loss of control."
- "But this time is different! AI can replace cognitive work, not just physical labor."
- "What about AI weapons? Autonomous drones? We're creating tools we can't control!"

## Full System

This is a simplified demo. The full Vertex DebSpar AI v3.0 system includes:

- **Local vLLM models** for low-latency responses
- **Groq API integration** for high-intensity debates
- **Kubernetes deployment** with auto-scaling
- **GPU optimization** for local model inference
- **WebSocket real-time communication**

## Repository

Full source code and deployment instructions: [GitHub](https://github.com/brian95240/vertex-debspar-ai-v3)

## License

GPLv3 (Open Source) + Commercial License available

---

**Vertex DebSpar AI v3.0** | Advanced Hybrid Debate System
