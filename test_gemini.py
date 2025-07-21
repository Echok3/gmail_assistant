from gmail_api.gmail_utils import get_recent_emails
from gemini_api.gemini_utils import classify_emails_with_gemini

emails = get_recent_emails(days=7, max_results=10)
result = classify_emails_with_gemini(emails)
print(result)
