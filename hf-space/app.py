import streamlit as st
import time
import random

# Page configuration
st.set_page_config(
    page_title="Vertex DebSpar AI v3.0 Demo",
    page_icon="🎯",
    layout="wide"
)

# Pressure estimation algorithm
def estimate_pressure(message: str, turn_number: int) -> float:
    """Calculate debate pressure on a 0-10 scale"""
    pressure = 0.0
    
    # Assertive language (+1.5 per instance)
    assertive_words = ["must", "should", "never", "always", "clearly", "obviously", "definitely"]
    pressure += sum(1.5 for word in assertive_words if word.lower() in message.lower())
    
    # Tension anchors (+1.0 per instance)
    tension_words = ["but", "however", "wrong", "dangerous", "threat", "risk", "fear", "disaster"]
    pressure += sum(1.0 for word in tension_words if word.lower() in message.lower())
    
    # Exclamation marks (+0.5 per instance)
    pressure += message.count("!") * 0.5
    
    # Question marks (challenging) (+0.3 per instance)
    pressure += message.count("?") * 0.3
    
    # Turn escalation (debates naturally intensify)
    pressure += turn_number * 0.3
    
    # Message length (longer = more passionate)
    if len(message) > 200:
        pressure += 1.0
    
    # Cap at 10.0
    return min(pressure, 10.0)

# Routing decision
def route_debate(pressure: float) -> tuple:
    """Route debate to appropriate model based on pressure"""
    if pressure > 7.2:
        return "APEX_CLOUD", "🔥 HIGH INTENSITY", "#ff4444"
    elif pressure > 4.0:
        return "LOCAL_WARM", "🌡️ MODERATE", "#ffaa00"
    else:
        return "LOCAL_WARM", "❄️ LOW INTENSITY", "#4444ff"

# Mock response generator
def generate_mock_response(user_message: str, pressure: float, turn_number: int) -> str:
    """Generate contextual mock responses based on pressure and content"""
    
    # Low pressure responses (calm, analytical)
    low_pressure_responses = [
        "While your concern is valid, let's examine the historical context. Technology has consistently created more opportunities than it has eliminated. The key is adaptation and education.",
        "That's an interesting perspective. However, we should consider the broader implications. AI augments human capabilities rather than replacing them entirely.",
        "I understand your viewpoint, but the data suggests a different trend. Let's look at specific examples where AI has enhanced rather than diminished human potential.",
    ]
    
    # Medium pressure responses (engaged, persuasive)
    medium_pressure_responses = [
        "You raise important points, but I must respectfully disagree. The evidence overwhelmingly shows that AI benefits outweigh the risks when properly regulated.",
        "That's a common misconception. In reality, AI has already proven its value in healthcare, education, and scientific research—saving lives and advancing knowledge.",
        "I hear your concerns, but consider this: every major technological shift has faced similar skepticism. The Industrial Revolution, the Internet—all were feared initially, yet all ultimately benefited humanity.",
    ]
    
    # High pressure responses (assertive, urgent)
    high_pressure_responses = [
        "Your urgency is understandable, but fear-driven policy leads to worse outcomes. We cannot halt progress—we must guide it responsibly. Banning AI would hand the advantage to authoritarian regimes with no ethical constraints.",
        "I strongly disagree. The risks you mention are real, but they're manageable through regulation and oversight. The EU AI Act, NIST frameworks, and industry safety research are already addressing these concerns.",
        "This is precisely why we need AI—to solve the complex problems you're describing! Climate change, disease, poverty—these require computational power beyond human capacity. AI is our best tool for survival.",
    ]
    
    # Select response based on pressure
    if pressure > 7.2:
        response = random.choice(high_pressure_responses)
    elif pressure > 4.0:
        response = random.choice(medium_pressure_responses)
    else:
        response = random.choice(low_pressure_responses)
    
    return response

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'turn_number' not in st.session_state:
    st.session_state.turn_number = 0

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
    <h1>🎯 Vertex DebSpar AI v3.0 - Interactive Demo</h1>
    <p><strong>Topic:</strong> Is AI more beneficial or dangerous to humanity?</p>
    <p><strong>System Position:</strong> Pro-AI (Beneficial) | <strong>Your Position:</strong> Anti-AI (Dangerous)</p>
</div>
""", unsafe_allow_html=True)

# Info section
with st.expander("ℹ️ How This Demo Works"):
    st.markdown("""
    This is a **mock demo** that simulates the Vertex DebSpar AI v3.0 hybrid debate system:
    
    - **Pressure Detection:** Analyzes your message for assertive language, tension words, and debate intensity (0-10 scale)
    - **Hybrid Routing:** Routes to APEX_CLOUD (high pressure >7.2) or LOCAL_WARM (low pressure ≤7.2)
    - **Mock Responses:** Pre-programmed responses that adapt to debate pressure
    - **Real-time Analysis:** Shows pressure metrics and routing decisions
    
    **Note:** This demo uses mock responses. The full system requires deployment with a Groq API key and optional GPU.
    
    **Try it:** Make increasingly assertive arguments to see the pressure rise and routing switch!
    """)

# Stats panel
st.markdown("""
<div style="background: #f7fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 20px;">
    <h3>📊 System Features</h3>
    <ul>
        <li><strong>Thermal Tiers:</strong> HOT (local, <100ms) | WARM (local, 150-300ms) | COLD (cloud, 500-1500ms)</li>
        <li><strong>Pressure Threshold:</strong> 7.2/10 triggers APEX_CLOUD routing</li>
        <li><strong>Debate Metrics:</strong> Real-time pressure analysis and routing decisions</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your argument here..."):
    # Increment turn counter
    st.session_state.turn_number += 1
    turn = st.session_state.turn_number
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Calculate pressure
    pressure = estimate_pressure(prompt, turn)
    
    # Route decision
    routing, intensity_label, color = route_debate(pressure)
    
    # Generate response
    response_text = generate_mock_response(prompt, pressure, turn)
    
    # Format system response with metadata
    system_response = f"""**[Turn {turn}] System Analysis:**
- **Pressure:** {pressure:.1f}/10 {intensity_label}
- **Routing:** {routing}
- **Response Time:** {random.randint(80, 400)}ms

**System Response:**
{response_text}
"""
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": system_response})
    
    # Display assistant response with streaming effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in system_response.split():
            full_response += chunk + " "
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(system_response)

# Reset button
if st.button("🔄 Reset Debate"):
    st.session_state.messages = []
    st.session_state.turn_number = 0
    st.rerun()

# Footer
st.markdown("""
---
**Vertex DebSpar AI v3.0** | [GitHub Repository](https://github.com/brian95240/vertex-debspar-ai-v3) | [Documentation](https://github.com/brian95240/vertex-debspar-ai-v3#readme)

*This is a mock demo. For the full system with real LLM integration, see the deployment guide.*
""")
