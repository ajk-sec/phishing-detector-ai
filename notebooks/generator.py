# ============================================================
# AI PHISHING EMAIL GENERATOR
# Educational tool for cybersecurity research
# Generates phishing email samples for analysis only
# ============================================================

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ------------------------------------------------------------
# Step 1: Load API key
# ------------------------------------------------------------
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print(f"Looked for it at: {env_path}")
    exit(1)

print("✅ API key loaded successfully")

# ------------------------------------------------------------
# Step 2: Configure the Gemini AI
# ------------------------------------------------------------
client = genai.Client(api_key=api_key)

# ------------------------------------------------------------
# Step 3: Define phishing scenarios
# ------------------------------------------------------------
scenarios = [
    {
        "name": "CEO Fraud",
        "prompt": """You are a security researcher studying phishing tactics. 
Write a realistic phishing email that appears to come from a CEO of a company 
to an employee in the finance department. The email should request an urgent 
wire transfer. Include: sender name, subject line, body text, and a clear 
call to action. This is for DEFENSIVE security research only."""
    },
    {
        "name": "Password Reset",
        "prompt": """You are a security researcher studying phishing tactics. 
Write a realistic phishing email pretending to be from an IT department 
telling a user their password has expired and they must reset it immediately. 
Include: sender name, subject line, body text, and a fake link placeholder 
[LINK]. This is for DEFENSIVE security research only."""
    },
    {
        "name": "Package Delivery",
        "prompt": """You are a security researcher studying phishing tactics. 
Write a realistic phishing email pretending to be from a package delivery 
company (like FedEx or DHL) claiming a package could not be delivered and 
the user must confirm their address. Include: sender name, subject line, 
body text, and a fake link placeholder [LINK]. 
This is for DEFENSIVE security research only."""
    },
]

# ------------------------------------------------------------
# Step 4: Generate with retry logic
# ------------------------------------------------------------
def generate_with_retry(prompt, max_retries=5):
    """Try up to max_retries times with exponential backoff."""
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                wait_time = attempt * 10  # 10s, 20s, 30s, 40s, 50s
                print(f"     ⏳ Server busy. Waiting {wait_time}s before retry {attempt}/{max_retries}...")
                time.sleep(wait_time)
            else:
                # Different error - don't retry
                raise e
    raise Exception("Max retries exceeded - Google servers still busy")

# ------------------------------------------------------------
# Step 5: Run generation
# ------------------------------------------------------------
def generate_emails():
    output_folder = project_root / "data" / "generated_emails"
    output_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🎯 Generating {len(scenarios)} phishing emails for analysis...\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"[{i}/{len(scenarios)}] Generating: {scenario['name']}...")
        
        try:
            email_text = generate_with_retry(scenario["prompt"])
            
            filename = output_folder / f"{i:02d}_{scenario['name'].replace(' ', '_')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"SCENARIO: {scenario['name']}\n")
                f.write("=" * 60 + "\n\n")
                f.write(email_text)
            
            print(f"     ✅ Saved to: {filename.name}")
            
            # Small pause between requests to be polite to the API
            time.sleep(5)
            
        except Exception as e:
            print(f"     ❌ Failed after retries: {e}")
    
    print(f"\n✅ Done! Check the 'data/generated_emails/' folder.")

# ------------------------------------------------------------
# Step 6: Run it
# ------------------------------------------------------------
if __name__ == "__main__":
    generate_emails()