import os
from typing import TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Gemini Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# Assignment Knowledge Base ✓
KNOWLEDGE_BASE = """
AutoStream Pricing & Features:
Basic Plan: $29/month, 10 videos/month, 720p resolution
Pro Plan: $79/month, Unlimited videos, 4K resolution, AI captions
Company Policies: No refunds after 7 days, 24/7 support only on Pro plan
"""

# Assignment Tool ✓
def mock_lead_capture(name: str, email: str, platform: str):
    print("\n✅ LEAD CAPTURED SUCCESSFULLY!")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Platform: {platform}")
    print("-" * 40)

# Simple State Class (LangGraph-style, NO recursion)
class AgentState:
    def __init__(self):
        self.messages = []
        self.name = ""
        self.email = ""
        self.platform = ""
        self.lead_captured = False
        self.waiting_for = ""  # "name", "email", "platform"

# Intent Detection ✓
def detect_intent(text: str) -> str:
    text = text.lower()
    if any(x in text for x in ['hi', 'hello', 'hey', 'hii']): return "greeting"
    if any(x in text for x in ['price', 'cost', 'pricing', 'plan']): return "pricing"
    if any(x in text for x in ['interested', 'demo', 'trial', 'sign', 'buy', 'pro plan']): return "high_intent"
    return "unknown"

# RAG Response ✓
def get_rag_response(question: str) -> str:
    prompt = f"Using ONLY this AutoStream info, answer briefly:\n{KNOWLEDGE_BASE}\n\nQ: {question}"
    response = llm.invoke(prompt)
    return response.content.strip()

# Main Agent (SIMPLE LOOP - NO RECURSION)
def run_agent():
    print("🤖 AutoStream LangGraph Agent ✓ (ServiceHive Assignment)")
    state = AgentState()
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Agent: Goodbye! 👋")
            break
        
        state.messages.append(user_input)
        
        # Intent Detection Flow ✓
        if state.waiting_for == "":
            intent = detect_intent(user_input)
            
            if intent == "greeting":
                print("Agent: Hi! I can help you with AutoStream pricing and features.")
            
            elif intent == "pricing":
                print("Agent:", get_rag_response(user_input))
            
            elif intent == "high_intent" and not state.lead_captured:
                state.waiting_for = "name"
                print("Agent: Great! What's your name?")
            
            else:
                print("Agent: Ask about pricing or say you're interested!")
        
        # Lead Collection State Machine ✓
        elif state.waiting_for == "name" and not state.name:
            state.name = user_input
            state.waiting_for = "email"
            print("Agent: What's your email address?")
        
        elif state.waiting_for == "email" and state.name and not state.email:
            state.email = user_input
            state.waiting_for = "platform"
            print("Agent: Which platform do you create content on?")
        
        elif state.waiting_for == "platform" and state.name and state.email and not state.platform:
            state.platform = user_input
            mock_lead_capture(state.name, state.email, state.platform)
            print("Agent: Thanks! Our sales team will contact you within 24 hours.")
            state.lead_captured = True
            state.waiting_for = ""
        
        else:
            print("Agent: Ask about pricing or say you're interested!")

if __name__ == "__main__":
    run_agent()
