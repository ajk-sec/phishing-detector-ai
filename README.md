# AI Phishing Detector & Generator

**An AI-powered cybersecurity tool for generating and analyzing phishing email samples**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)]()

---

## Overview

This project is an educational cybersecurity tool that uses Google's Gemini AI to generate realistic phishing email samples for defensive research and awareness training.

Modern phishing attacks increasingly leverage AI to craft highly convincing, personalized emails. This project studies these tactics to help security professionals and students build better defenses.

> **Educational Use Only** — All generated content is for defensive security research. No emails are ever sent to real users.

---

## Features

- **AI-Powered Generation** — Uses Google Gemini API to create realistic phishing samples
- **Multiple Scenarios** — CEO Fraud, Password Reset, Package Delivery, and more
- **Annotated Analysis** — Each sample includes red flags and psychological techniques
- **Secure Architecture** — API keys protected with `.env` and `.gitignore`
- **Reliable** — Automatic retry logic for API rate limits and server issues

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Core programming language |
| Google Gemini API | AI-powered email generation |
| google-genai | Official Google GenAI SDK |
| python-dotenv | Secure environment variable management |
| Git & GitHub | Version control and hosting |

---

## Project Structure

    phishing-detector-ai/
    ├── data/
    │   └── generated_emails/     # AI-generated phishing samples
    ├── notebooks/
    │   └── generator.py          # Main generator script
    ├── src/                      # Detector model (in development)
    ├── images/                   # Documentation assets
    ├── .env                      # API keys (not tracked)
    ├── .gitignore                # Protects sensitive files
    └── README.md                 # This file

---

## Installation

### Prerequisites

- Python 3.13 or higher
- A free Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Setup Steps

**1. Clone the repository**

    git clone https://github.com/ajk-sec/phishing-detector-ai.git
    cd phishing-detector-ai

**2. Install dependencies**

    pip install google-genai python-dotenv

**3. Create a `.env` file in the project root**

    GEMINI_API_KEY=your_api_key_here

**4. Run the generator**

    python notebooks/generator.py

Generated emails will be saved in `data/generated_emails/`.

---

## Usage

The generator produces annotated analysis of common phishing scenarios:

| Scenario | Description |
|----------|-------------|
| CEO Fraud | Business Email Compromise targeting finance teams |
| Password Reset | Fake IT department password expiration alerts |
| Package Delivery | Fake delivery notifications from shipping companies |

Each generated sample includes:
- The email structure (sender, subject, body)
- Psychological manipulation techniques used
- Defensive countermeasures

---

## Roadmap

- [x] AI email generator with Gemini API
- [x] Retry logic for API reliability
- [x] Secure API key handling
- [ ] Machine learning phishing detector
- [ ] Streamlit web application
- [ ] Live demo deployment
- [ ] Gmail integration (optional)

---

## Ethical Notice

This project is **strictly for educational and defensive security research**. It is designed to help security professionals and students understand phishing tactics to build better defenses.

**Do NOT use this tool to:**
- Send phishing emails to real people
- Deceive or harm anyone
- Conduct unauthorized security testing

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

**ajk-sec**

- GitHub: [@ajk-sec](https://github.com/ajk-sec)
- Project: [phishing-detector-ai](https://github.com/ajk-sec/phishing-detector-ai)

---

⭐If you find this project useful for cybersecurity research, please give it a star.
