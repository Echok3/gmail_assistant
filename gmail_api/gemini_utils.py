import google.generativeai as genai
import re

# 🔑 Change for your Gemini API Key
GENAI_API_KEY = "xxxxxxxxxxxxxxx"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

def classify_emails_with_gemini(emails):
    email_chunks = ""
    for i, e in enumerate(emails, 1):
        email_chunks += f"邮件{i}：\n主题：{e['subject']}\n正文：{e['body'][:200]}\n\n"

    prompt = f"""
你是一个邮件分类助手。请按照以下格式对邮件进行分类（重要、广告、金融、其他）并给出一个详细总结。

输出格式如下：
总结：xxx
邮件分类：
邮件1：重要
邮件2：广告
...

以下是邮件内容：
{email_chunks}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    # 解析
    summary_match = re.search(r"总结[:：](.*)", text)
    summary = summary_match.group(1).strip() if summary_match else "（无）"

    classifications = {}
    for line in text.splitlines():
        match = re.match(r"邮件(\d+)[:：](.*)", line)
        if match:
            idx = int(match.group(1)) - 1
            label = match.group(2).strip()
            classifications[idx] = label

    return summary, classifications


def generate_reply_from_gemini(email, user_prompt):
    prompt = f"""
你是一个邮件写作助手。请根据以下原始邮件内容和我的要求，帮我写一封回复邮件。

原始邮件内容：
发件人：{email.get('from')}
主题：{email.get('subject')}
正文：
{email.get('body')}

我的要求：
{user_prompt}

请帮我写一封得体、简洁的中文回复，直接给出正文内容即可。
"""

    response = model.generate_content(prompt)
    return response.text.strip()



# # 🔑 替换成你的 Gemini API Key
# GENAI_API_KEY = "AIzaSyA6wPCOZ654sd9Hb0B6NMqwvAnjkDbvqxo"
