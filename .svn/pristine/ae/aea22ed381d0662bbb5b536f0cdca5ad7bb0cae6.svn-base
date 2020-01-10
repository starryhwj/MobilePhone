# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(
        verbose_name='电话', max_length=128, null=True, blank=True)
    head_pic = models.ImageField(
        verbose_name='头像', upload_to='images/Users/%Y/%m/%d/', null=True, blank=True)
    is_pay = models.BooleanField(
        verbose_name='是否是付费用户', null=False, default=False)
    pay_begin_date = models.DateTimeField(
        verbose_name='付费起始日期', null=True, blank=True)
    pay_end_date = models.DateTimeField(
        verbose_name='付费结束日期', null=True, blank=True)
    invite_code = models.TextField(
        verbose_name='邀请码', max_length=150, null=False, default='')
    is_pass = models.BooleanField(
        verbose_name='是否通过审核', null=False, default=False)
    leader = models.ForeignKey('self', verbose_name='上级',  null=True, on_delete=models.SET_NULL, related_name='上级')
    true_name = models.CharField(
        verbose_name='姓名', max_length=128, null=True, blank=True)
    sex = models.IntegerField(verbose_name='性别', null=False, default=0)
    birthday = models.DateField(
        verbose_name='生日', null=True, blank=True)
    qq = models.CharField(
        verbose_name='QQ', max_length=128, null=True, blank=True)
    wechat = models.CharField(
        verbose_name='微信', max_length=128, null=True, blank=True)
    wechat_nickname = models.CharField(
        verbose_name='微信昵称', max_length=128, null=True, blank=True)
    platform = models.CharField(
        verbose_name='平台', max_length=128, null=True, blank=True) 
    platform_id = models.CharField(
        verbose_name='平台账号', max_length=128, null=True, blank=True) 
    platform_password = models.CharField(
        verbose_name='平台密码', max_length=128, null=True, blank=True) 
    platform_is_certification = models.IntegerField(verbose_name='是否实名认证', null=False, default=0)
    platform_certification_true_name = models.CharField(
        verbose_name='实名认证姓名', max_length=128, null=True, blank=True) 
    platform_certification_id_card = models.CharField(
        verbose_name='实名认证身份证', max_length=128, null=True, blank=True)      
    money = models.DecimalField(verbose_name='账户余额',
        max_digits=18, decimal_places=2, null=False, default=0)     
    is_mainuser = models.BooleanField(
        verbose_name='是否是主要用户', null=False, default=False) 
    usersystem = models.ForeignKey('self', verbose_name='顶级用户',  null=True, on_delete=models.SET_NULL, related_name='顶级用户')                                                             