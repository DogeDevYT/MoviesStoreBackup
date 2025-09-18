from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import render, redirect

from cart.models import Order
from .forms import CustomUserCreationForm, CustomErrorList, SecurityQuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,
                                      error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})


def forgot_password(request):
    template_data = {}
    template_data['title'] = 'Forgot Password'
    if request.method == 'GET':
        return render(request, 'accounts/forgot_password.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            return redirect('accounts.forgot_password_confirm', username=user.username)
        except User.DoesNotExist:
            template_data['error'] = 'User not found'
            return render(request, 'accounts/forgot_password.html',
                          {'template_data': template_data})


def forgot_password_confirm(request, username):
    template_data = {}
    template_data['title'] = 'Forgot Password'
    user = User.objects.get(username=username)
    security_question = user.securityquestion_set.first()
    if request.method == 'GET':
        template_data['question'] = security_question.question
        return render(request, 'accounts/forgot_password_confirm.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        answer = request.POST['answer']
        if answer == security_question.answer:
            return redirect('accounts.reset_password', username=user.username)
        else:
            template_data['error'] = 'Incorrect answer'
            template_data['question'] = security_question.question
            return render(request, 'accounts/forgot_password_confirm.html',
                          {'template_data': template_data})


def reset_password(request, username):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        return render(request, 'accounts/reset_password.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if password == password_confirm:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect('accounts.login')
        else:
            template_data['error'] = 'Passwords do not match'
            return render(request, 'accounts/reset_password.html',
                          {'template_data': template_data})
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password you entered is incorrect'
            return render(request, 'accounts/login.html',
                          {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})


@login_required
def settings(request):
    template_data = {}
    template_data['title'] = 'Settings'
    if request.method == 'GET':
        template_data['form'] = SecurityQuestionForm()
        return render(request, 'accounts/settings.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            security_question = form.save(commit=False)
            security_question.user = request.user
            security_question.save()
            return redirect('accounts.settings')
        else:
            template_data['form'] = form
            return render(request, 'accounts/settings.html',
                          {'template_data': template_data})