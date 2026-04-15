import os
from dotenv import load_dotenv
from agent import EmailAgent
from emailer import send_email
from colorama import init, Fore

init(autoreset=True)

def main():
    print(Fore.CYAN + "\n==============================================")
    print(Fore.CYAN + "   Automated Email Sender AI Agent Initialized")
    print(Fore.CYAN + "==============================================\n")
    
    # Load environment variables
    load_dotenv()
    
    # Ensure variables exist
    if not os.path.exists(".env"):
        print(Fore.RED + "Error: .env file not found. Please copy .env.example to .env and fill in your credentials.")
        return

    # Initialize the AI Agent
    try:
        agent = EmailAgent()
    except Exception as e:
        print(Fore.RED + f"Failed to initialize AI agent: {e}")
        return

    # A hardcoded list of contacts for demonstration. In a real scenario, this could be loaded from a CSV/DB.
    contacts = [
        {"name": "A.P. Cyc", "role": "Target Contact", "email": "a.p.cyc@outlook.com"}
    ]
    
    # Global context/goal for the outreach campaign
    campaign_goal = "I want to introduce our new AI-driven sneaker resale automation tool that helps scaling businesses seamlessly source limited drops."
    
    for contact in contacts:
        print(Fore.YELLOW + f"Generating personalized email for {contact['name']} ({contact['role']})...")
        
        # 1. AI drafts the email
        draft = agent.generate_personalized_email(
            recipient_name=contact["name"],
            recipient_role=contact["role"],
            context=campaign_goal
        )
        
        print(Fore.MAGENTA + f"--> Subject: {draft['subject']}")
        
        # 2. Actually send the email (Warning: ensure credentials are real before uncommenting)
        # To truly simulate, you can comment out the line below.
        success = send_email(contact["email"], draft["subject"], draft["body"])
        
        if success:
            print(Fore.GREEN + f"--> [SUCCESS] Email sent to {contact['email']}\n")
        else:
            print(Fore.RED + f"--> [FAILED] Could not send to {contact['email']}. Check logs/credentials.\n")
        
    print(Fore.CYAN + "Run complete! To actually send emails, open main.py and uncomment the 'send_email(..)' function call.")

if __name__ == "__main__":
    main()
