import os.path
import base64
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import re

# 只读 Gmail 权限
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    # Get by your gmail account api
    token_path = 'credentials/token.json'
    cred_path = 'credentials/credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_recent_emails(days=7, max_results=12):
    service = get_gmail_service()
    query_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
    results = service.users().messages().list(
        userId='me', q=f'after:{query_date}', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_detail['payload']
        headers = payload['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        from_value = next((h['value'] for h in headers if h['name'] == 'From'), '')
        snippet = msg_detail.get('snippet', '')

        # 获取正文（简化版）
        body = ''
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('utf-8', errors='ignore')
                    break

        emails.append({
            'subject': subject,
            'from': from_value,
            'date': date,
            'snippet': snippet,
            'body': body
        })
    return emails

def send_reply_email(original_email, reply_text):
    service = get_gmail_service()

    from_email = "me"
    raw_from = original_email.get('from')
    match = re.search(r'[\w\.-]+@[\w\.-]+', raw_from)
    to_email = match.group(0) if match else raw_from

    subject = "Re: " + original_email.get('subject', '（No Subject Title）')

    message = MIMEMultipart()
    message['To'] = to_email
    message['From'] = from_email
    message['Subject'] = Header(subject, 'utf-8')

    message.attach(MIMEText(reply_text.strip(), 'plain', 'utf-8'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {'raw': raw_message}

    thread_id = original_email.get('threadId')
    if thread_id:
        send_message['threadId'] = thread_id

    return service.users().messages().send(userId="me", body=send_message).execute()
