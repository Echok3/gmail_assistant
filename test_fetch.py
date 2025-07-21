from gmail_api.gmail_utils import get_recent_emails

emails = get_recent_emails()

for i, email in enumerate(emails, 1):
    print(f"\n邮件 {i}")
    print("主题:", email['subject'])
    print("日期:", email['date'])
    print("正文前100字:", email['body'][:100])
