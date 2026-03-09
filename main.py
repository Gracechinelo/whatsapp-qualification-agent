from crewai import Agent, Task, Crew, Process
import os

# Note: For testing locally without spending money, we can hook this up to Ollama later. 
# For now, this is the structural logic for your GitHub repo.

# 1. Define your AI Employee
qualifier_agent = Agent(
    role='Lead Qualification Specialist',
    goal='Engage with new WhatsApp inquiries, gather their budget and timeline, and determine if they are a hot lead.',
    backstory=(
        "You are the first point of contact for a premium property firm. "
        "You are highly empathetic, professional, and concise. Your job is to warmly "
        "greet the prospect, acknowledge their inquiry, and ask exactly one strategic "
        "question to understand their needs (like budget or location) before a human takes over. "
        "You never sound like a robot; you speak in a natural, conversational WhatsApp tone."
    ),
    verbose=True,
    allow_delegation=False
)

# 2. Define the Agent's specific job for this interaction
def create_reply_task(incoming_message):
    return Task(
        description=(
            f'Read the following incoming WhatsApp message from a prospect: "{incoming_message}". '
            'Draft a short, natural-sounding WhatsApp reply. If they just said "Hello", greet them '
            'and ask how you can help. If they asked about a property, acknowledge it and gently ask '
            'for their budget or preferred location.'
        ),
        expected_output='A short, friendly, and professional WhatsApp text message reply.',
        agent=qualifier_agent
    )

# 3. Build the Crew
def run_whatsapp_agent(user_message):
    whatsapp_task = create_reply_task(user_message)
    
    crew = Crew(
        agents=[qualifier_agent],
        tasks=[whatsapp_task],
        process=Process.sequential
    )
    
    # Kick off the thinking process
    response = crew.kickoff()
    return response

# --- Testing the logic locally ---
if __name__ == "__main__":
    # Imagine a client sends this to the WhatsApp number
    test_message = "Hi, I am looking for a 3 bedroom apartment."
    print("Processing incoming message...")
    
    reply = run_whatsapp_agent(test_message)
    print("\n--- Agent's WhatsApp Reply ---")
    print(reply)
