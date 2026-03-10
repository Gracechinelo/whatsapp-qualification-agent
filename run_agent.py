import os
import sys

# 1. Tell Python where to find your agent's code
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# 2. Wire up the Gemini Brain (Paste your key between the quotes below!)
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
os.environ["MODEL"] = "gemini-2.5-flash"

# We import the engine you built earlier
from whatsapp_agent.crew import WhatsappAgent

def run():
    # 3. Simulate an incoming WhatsApp message from a client
    inputs = {
        'incoming_message': 'Hi, I saw your ad and I am looking for a 3 bedroom apartment in the city center.'
    }
    
    print("\n--- 🤖 AI Agent is reading the message... ---\n")
    WhatsappAgent().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()