import os
import sys

# --- THE MAP: Tell Python to look inside the 'src' folder ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, request
from whatsapp_agent.crew import WhatsappAgent

app = Flask(__name__)

# --- CONFIGURATION ---
# Plug your actual Gemini API key right here!
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY" 
os.environ["MODEL"] = "gemini-2.5-flash"

VERIFY_TOKEN = "my_secret_token_123"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1. Meta Verifying the Connection
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified by Meta!")
            return challenge, 200
        return "Forbidden", 403

    # 2. Receiving and Processing WhatsApp Messages
    if request.method == "POST":
        data = request.get_json()
        
        try:
            # Digging through Meta's data layers to find the actual text message
            message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
            incoming_msg = message_data['text']['body']
            sender_phone = message_data['from']
            
            print(f"\n📱 New Message from {sender_phone}: {incoming_msg}")
            
            # WAKE UP THE AI!
            print("🧠 AI Employee is analyzing the message...")
            inputs = {'incoming_message': incoming_msg}
            
            # This is where your AI reads the prompt and drafts the perfect reply
            ai_response = WhatsappAgent().crew().kickoff(inputs=inputs)
            
            print(f"✅ AI Reply Drafted: \n{ai_response}")
            
        except KeyError:
            # If it's just a background status update, ignore it quietly
            pass

        return "OK", 200

if __name__ == "__main__":
    print("🎧 Webhook & AI Brain are listening on port 5000...")
    app.run(port=5000)