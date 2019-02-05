# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.contrib import messages
import random

# from playsound import playsound
 
# Homepage
def index(request):
    if 'logged_in' not in request.session:
        # playsound('apps/math_app/static/intro.mp3', False)
        return render(request, "index.html")
    else:
        return redirect("/menu")

# Registration page
def register(request):
    # playsound('apps/math_app/static/button.mp3', False)
    return render(request, "register.html")   

# Create new user
def save_user(request):
    message_flag = 0
    if len(request.POST['first_name']) < 1:
        message_flag = 1
        messages.error(request, 'First Name field cannot be blank', extra_tags="first_name")
    elif len(request.POST['first_name']) == 1:
        message_flag = 1
        messages.error(request, 'First Name must be two or more characters', extra_tags="first_name")

    if len(request.POST['last_name']) < 1:
        message_flag = 1
        messages.error(request, 'Last Name field cannot be blank', extra_tags="last_name")
    elif len(request.POST['last_name']) == 1:
        message_flag = 1
        messages.error(request, 'Last Name must be two or more characters', extra_tags="last_name")

    if len(request.POST['email']) < 1:
        message_flag = 1
        messages.error(request, 'Email field cannot be blank', extra_tags="email")
    elif not EMAIL_REGEX.match(request.POST['email']):
        message_flag = 1
        messages.error(request, 'Email must be in email format', extra_tags="email")
    elif User.objects.filter(email__iexact=request.POST['email']).exists():
        message_flag = 1
        messages.error(request, 'This email is already registered', extra_tags="email")

    if len(request.POST['password']) < 1:
        message_flag = 1
        messages.error(request, 'Password field cannot be blank', extra_tags="password")
    elif len(request.POST['password']) < 8:
        message_flag = 1
        messages.error(request, 'Password must be 8 or more characters', extra_tags="password")

    if request.POST['password'] != request.POST['confirm_password']:
        message_flag = 1
        messages.error(request, 'Password confirmation does not match', extra_tags="password_confirm")

    if message_flag == 0:
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'].lower(), user_score_list=[], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['first_name'] = request.POST['first_name']
        request.session['logged_in'] = True
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect("/menu")
    else:
        return redirect("/register")


# Login page
def login(request):
    # playsound('apps/math_app/static/button.mp3', False)
    return render(request, "login.html")

# Login logic
def log_user(request):
    message_flag = 0
    if len(request.POST['email']) < 1:
        message_flag = 1
        messages.error(request, 'Email field cannot be blank', extra_tags="log_email")
    
    if len(request.POST['password']) < 1:
        message_flag = 1
        messages.error(request, 'Password field cannot be blank', extra_tags="log_password")

    if message_flag == 0:
        if User.objects.filter(email__iexact=request.POST['email']).exists():
            user = User.objects.get(email=request.POST['email'].lower())
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
                request.session['email'] = request.POST['email']
                request.session['logged_in'] = True
                request.session['user_id'] = User.objects.get(email=request.POST['email']).id
                return redirect("/menu")
            else:
                messages.error(request, 'Email and Password combo does not match', extra_tags="log_email")
                return redirect("/login")
        else:
            messages.error(request, 'Email and Password combo does not match', extra_tags="log_email")
            return redirect("/menu")
    else:
        return redirect("/login")

# Game menu
def menu(request):
    # playsound('apps/math_app/static/button.mp3', False)
    return render(request, "menu.html")   

# Game - Individual round logic
def game(request):        
    if 'game_counter' not in request.session:
        request.session['game_counter'] = 1
    else:
        request.session['game_counter'] += 1
    
    if request.session['game_counter'] == 11:
        return redirect("/end_of_round")

    request.session['top_num'] = random.randint(0,9)
    request.session['bottom_num'] = random.randint(0,9)

    if request.session['game_type'] == 'add':
        request.session['symbol'] = '+'
        request.session['solution'] = request.session['top_num'] + request.session['bottom_num']
    elif request.session['game_type'] == 'sub':
        request.session['symbol'] = '-'
        if request.session['top_num'] < request.session['bottom_num']:
            request.session['top_num'], request.session['bottom_num'] = request.session['bottom_num'], request.session['top_num']
        request.session['solution'] = request.session['top_num'] - request.session['bottom_num']
    elif request.session['game_type'] == 'mult':
        request.session['symbol'] = 'x'
        request.session['solution'] = request.session['top_num'] * request.session['bottom_num']
    elif request.session['game_type'] == 'div':
        request.session['symbol'] = '/'
        request.session['top_num'] = random.randint(1,9)
        request.session['bottom_num'] = random.randint(1,9)
        request.session['solution'] = request.session['top_num']
        request.session['top_num'] = request.session['bottom_num'] * request.session['solution']

    return render(request, "game.html")   

# Reset game counter for new 10-round game
def clear_counter(request):
    request.session['game_counter'] = 0
    return redirect("/game")

# User submits response logic
def submit_response(request):
    if request.session['game_type'] == 'add':
        if request.session['top_num'] +  request.session['bottom_num'] == int(request.POST['response']):
            request.session['score'] = 1
            # bell()
        else:
            request.session['score'] = 0
            # buzzer()
    elif request.session['game_type'] == 'sub':
        if request.session['top_num'] -  request.session['bottom_num'] == int(request.POST['response']):
            request.session['score'] = 1
            # bell()
        else:
            request.session['score'] = 0
            # buzzer()
    elif request.session['game_type'] == 'mult':
        if request.session['top_num'] *  request.session['bottom_num'] == int(request.POST['response']):
            request.session['score'] = 1
            # bell()
        else:
            request.session['score'] = 0
            # buzzer()
    elif request.session['game_type'] == 'div':
        if request.session['top_num'] /  request.session['bottom_num'] == int(request.POST['response']):
            request.session['score'] = 1
            # bell()
        else:
            request.session['score'] = 0
            # buzzer()

    one_round_list = [request.session['top_num'],request.session['symbol'], request.session['bottom_num'], int(request.POST['response']), request.session['solution'], request.session['score']]
        
    if 'ten_round_list' not in request.session:
        request.session['ten_round_list'] = [one_round_list]
    else:
        ten_round_list = request.session['ten_round_list']
        ten_round_list.append(one_round_list)
        request.session['ten_round_list'] = ten_round_list
    
    request.session['from_game_flag'] = True
    request.session['score_sum'] += request.session['score']
    request.session['round_score'] = int((float(request.session['score_sum']) / float(len(request.session['ten_round_list'])) * 100))
    return redirect("/game")

def rerack(request):
    # playsound('apps/math_app/static/button.mp3', False)
    if 'game_type' in request.POST:
        request.session['game_type'] = request.POST['game_type']
    request.session['game_counter'] = 0
    request.session['ten_round_list'] = []
    request.session['round_score'] = 0
    request.session['score_sum'] = 0
    return redirect("/game")

def guest(request):
    return redirect("/menu")

def end_of_round(request):
    # playsound('apps/math_app/static/end_round.mp3', False)
    ten_round_list = request.session['ten_round_list']
    if request.session['from_game_flag'] == True:
        ten_round_list.append(request.session['round_score'])
        request.session['ten_round_list'] = ten_round_list
        # user = User.objects.get(id=request.session['user_id'])
        # Score.objects.create(ten_round_list = request.session['ten_round_list'], student = user)
    return render(request, "end_of_round.html")

def flush(request):
    request.session.flush()
    return redirect('/')

def records(request):
    # context = {
    #     'scores': User.objects.get(email=request.session['email']).user_score_list
    # }
    # request.session['from_game_flag'] = False
    # return render(request, "records.html", context)
    return redirect("/menu")

# def bell():
#     playsound('apps/math_app/static/bell.mp3', False)

# def buzzer():
#     playsound('apps/math_app/static/buzzer.mp3', False)