from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from gmail_api.gmail_utils import get_recent_emails, send_reply_email
from gemini_api.gemini_utils import classify_emails_with_gemini
from gmail_api.gemini_utils import generate_reply_from_gemini

from copy import deepcopy
from datetime import datetime

def root_redirect(request):
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': '用户名或密码错误'})
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    raw_emails = get_recent_emails(days=7, max_results=20)

    emails = []
    for idx, email in enumerate(raw_emails):
        email = deepcopy(email)
        email['index'] = idx
        emails.append(email)

    request.session['emails'] = emails  # 存 session（注意：需要可序列化的 dict，不要包含 bytes）

    summary, classifications = classify_emails_with_gemini(emails)

    categories = {'Important': [], 'Promotion': [], 'Bills': [], 'Other': []}
    for idx, label in classifications.items():
        if idx >= len(emails):
            continue
        label = label if label in categories else 'Other'
        categories[label].append(emails[idx])

    return render(request, 'users/home.html', {
        'summary': summary,
        'categories': categories,
    })


@login_required
@csrf_exempt
def mail_detail(request, index):
    emails = get_recent_emails(days=7, max_results=20)
    email = emails[index]

    # 解析并格式化日期
    if isinstance(email.get('date'), str):
        try:
            email['date'] = datetime.strptime(email['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                email['date'] = datetime.strptime(email['date'], "%Y-%m-%dT%H:%M:%SZ")
            except:
                pass

    gemini_reply = ''

    if request.method == 'POST':
        if 'user_prompt' in request.POST:
            # 用户请求生成回信
            user_prompt = request.POST['user_prompt']
            gemini_reply = generate_reply_from_gemini(email, user_prompt)

        elif 'send_reply' in request.POST:
            # 用户点击“发送”按钮
            reply_text = request.POST['reply_text']
            send_reply_email(email, reply_text)
            return redirect('home')

    return render(request, 'users/mail_detail.html', {
        'email': email,
        'index': index,
        'gemini_reply': gemini_reply,
        'show_back_button': True,
    })