import google.generativeai as genai
import re

# 🔑 替换成你的 Gemini API Key
GENAI_API_KEY = "AIzaSyA6wPCOZ654sd9Hb0B6NMqwvAnjkDbvqxo"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

def classify_emails_with_gemini(emails):
    email_chunks = ""
    for i, e in enumerate(emails, 1):
        email_chunks += f"Email{i}:\nSubject: {e['subject']}\nBody: {e['body'][:200]}\n\n"

    prompt = f"""
You are an email classification assistant. Please classify the following emails into one of the following categories: Important, Promotion, Bills, Other. Also provide a brief summary of the emails.

Output format:
Summary: xxx
Email classifications:
Email1: Important
Email2: Promotion
...

Here are the emails:
{email_chunks}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    summary_match = re.search(r"Summary[:：](.*)", text)
    summary = summary_match.group(1).strip() if summary_match else "(None)"

    classifications = {}
    for line in text.splitlines():
        match = re.match(r"Email(\d+)[:：](.*)", line)
        if match:
            idx = int(match.group(1)) - 1
            label = match.group(2).strip()
            classifications[idx] = label

    return summary, classifications


def generate_reply_from_gemini(email, user_prompt):
    prompt = f"""
You are an email reply assistant. Based on the original email content and the user's instruction, generate a concise and polite reply in the **same language as the instruction**.

Original email:
From: {email.get('from')}
Subject: {email.get('subject')}
Body:
{email.get('body')}

Instruction:
{user_prompt}

Output rules:
- Only output the **reply body**, nothing else.
- Do NOT include any explanation, greetings like “Here’s your reply”, or subject lines.
- Do NOT include any placeholder like [Your Name], [Company Name], or similar — directly use the name: Kelvin.
- Your reply must begin immediately with the body text. Do not include any meta-commentary.
"""

    response = model.generate_content(prompt)
    return response.text.strip()

