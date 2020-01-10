# -*- coding: utf-8 -*-
# -*- filename: Users/views.py

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .form import CustomUserCreationForm
import json
import string
import random
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method != 'POST':
        return render(request, 'users/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            if (authenticated_user.is_superuser == False and authenticated_user.is_pass == False):
                return HttpResponse('Not Pass')
            login(request, authenticated_user)
            return HttpResponse(reverse('Web:index'))
        else:
            return HttpResponse('False')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('Users:login'))


def register(request):
    if request.method != 'POST':
        invite_code = request.GET.get('invite_code')
        form = CustomUserCreationForm(initial={'leadercode': invite_code, 'platform':'抖音'})
        context = {'form': form}
        return render(request, 'users/register.html', context)
    else:       
        ret = {"status": "NG", "msg": None, "loginpage": None}
        form = CustomUserCreationForm(data=request.POST)
        learder_code = request.POST.get('leadercode')
        leader_list = User.objects.filter(invite_code=learder_code)
        if leader_list.count() > 0:
            if form.is_valid():
                new_user = form.save(commit=False)
                invite_code = generate_invite_code(6)
                while is_invite_code_exists(invite_code):
                    invite_code = generate_invite_code(6)
                new_user.invite_code = invite_code
                leader = leader_list.first()
                new_user.leader = leader
                while leader.is_superuser == False and leader.is_mainuser == False:
                    leader = leader.leader
                new_user.usersystem = leader
                true_name = request.POST.get('true_name')
                sex = request.POST.get('sex')
                birthday = request.POST.get('birthday')
                qq = request.POST.get('qq')
                wechat = request.POST.get('wechat')
                wechat_nickname = request.POST.get('wechat_nickname')
                phone = request.POST.get('phone')
                platform = request.POST.get('platform')
                platform_id = request.POST.get('platform_id')
                platform_password = request.POST.get('platform_password')
                platform_is_certification = request.POST.get('platform_is_certification')
                platform_certification_true_name = request.POST.get('platform_certification_true_name')
                platform_certification_id_card = request.POST.get('platform_certification_id_card')                                                                                                                
                new_user.true_name = true_name
                new_user.sex = sex
                if birthday != '':
                    new_user.birthday = birthday
                new_user.qq = qq
                new_user.wechat = wechat
                new_user.wechat_nickname = wechat_nickname      
                new_user.phone = phone      
                new_user.platform = platform      
                new_user.platform_id = platform_id      
                new_user.platform_password = platform_password      
                new_user.platform_is_certification = platform_is_certification      
                new_user.platform_certification_true_name = platform_certification_true_name      
                new_user.platform_certification_id_card = platform_certification_id_card                                                                                                                                                                                                                                                       
                new_user.save()
                ret["status"] = "OK"
                ret["msg"] = { "success": "注册成功，请等待通过审核，5秒后跳转到登陆页面" }
                ret["loginpage"] = reverse('Web:index')
            else:
                ret["msg"] = form.errors
        else:
            ret["msg"] = { "leadercode": "邀请码有误" }
        return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@method_decorator(csrf_exempt, name='dispatch')
@login_required
def changepassword(request):
    if request.method != 'POST':
        change_password_url = request.build_absolute_uri(reverse('Users:changepassword'))
        context = {'change_password_url': change_password_url}
        return render(request, 'users/changepassword.html', context)
    else:
        oldpassword = request.POST.get('oldpassword')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        ret = {"status": "NG", "msg": None}
        user = User.objects.get(id=request.user.id)
        if user:
            if check_password(oldpassword, user.password):
                if password1 == password2:
                    user.password = make_password(password1)
                    user.save()
                    login(request, user)
                    ret["status"] = "OK"
                    ret["msg"] = "修改成功，下次登陆时请使用新密码"
                else:
                    ret["msg"] = "两次输入的新密码不相同，请重新输入"
            else:
                ret["msg"] = "当前密码有误，请重新输入"
        else:
            ret["msg"] = '用户ID有误，找不到该用户'
        return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


def generate_invite_code(num):
    field = string.ascii_letters + string.digits
    code = "".join(random.sample(field, num))
    return code


def is_invite_code_exists(invite_code):
    user = User.objects.filter(invite_code=invite_code)
    if user.count == 0:
        return True
    else:
        return False

