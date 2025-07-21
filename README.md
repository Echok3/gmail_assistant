# Gmail Assistant 📬

This is an intelligent email assistant built with Python and Gemini LLM, designed to help users classify emails, summarize inbox content, and generate smart replies based on user instructions.

## 🔧 Features

- 📥 **Fetch Emails**: Automatically fetch emails from Gmail using Gmail API.
- 🧠 **Classify Emails**: Use Gemini LLM to classify emails into categories: Important, Promotion, Bills, and Others.
- 📝 **Summarize Inbox**: Automatically generate an overall summary of the inbox.
- 🤖 **Smart Replies**: Generate concise, polite, and language-aware replies based on user instructions.
- 🌐 **Multi-language Support**: Supports generating replies in English, Japanese, French, and more — depending on your input instruction.
- 🔐 **Secure**: OAuth2 authentication for Gmail and local token storage.

## 🖼️ Project Structure

gmail_assistant/

├── credentials/          # OAuth credentials and token storage

├── gemini_api/           # Handles Gemini LLM prompt generation and classification

├── gmail_api/            # Gmail API integration for fetching and sending emails

├── gmail_assistant/      # Django app for frontend and views

├── users/                # User management app

├── manage.py             # Django entrypoint

├── db.sqlite3            # SQLite database

├── test_fetch.py         # Script to test email fetching

├── test_gemini.py        # Script to test Gemini replies

└── venv/                 # Python virtual environment (excluded in .gitignore)

---
## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Echok3/gmail_assistant.git
cd gmail_assistant
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Gmail API credentials

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Enable Gmail API and download `credentials.json`
- Place the file under `credentials/` directory

### 5. Run the Django server

```bash
python manage.py runserver
```

## ✉️ Usage

- Open browser: `http://127.0.0.1:8000/`
- Log in and import Gmail
- Select any email to:
    - View classification
    - Generate smart reply
    - Submit the reply back to Gmail

## 🧪 Testing

```bash
python test_fetch.py       # Test Gmail fetch
python test_gemini.py      # Test Gemini LLM reply
```

## 🔐 Authentication

- The app uses OAuth2 to authenticate Gmail API.
- Tokens are securely stored locally.

## 📌 To Do

- Add email search by keyword/date
- Store reply history in DB
- UI enhancement and mobile support

## 🧑‍💻 Author

**Kelvin.A**

Feel free to fork or contribute to this project.

---

MIT License | © 2025 Kelvin A.
