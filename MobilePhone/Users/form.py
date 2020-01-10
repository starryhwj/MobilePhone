# -*- coding: utf-8 -*-
# filename: Users/form.py
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput, DateInput
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    Sex = [('0', '男'), ('1', '女')]
    Platform_Is_Certification = [('0', '否'), ('1', '是')]

    leadercode = forms.CharField(
        label="邀请码"
    )
    true_name = forms.CharField()
    phone = forms.CharField()
    wechat = forms.CharField()
    wechat_nickname = forms.CharField(required=False)
    qq = forms.CharField(required=False)    
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=Sex, label='sex', required=False)
    birthday = forms.DateField(required=False)
    platform = forms.CharField(required=False)
    platform_id = forms.CharField(required=False)
    platform_password = forms.CharField(required=False)
    platform_is_certification = forms.ChoiceField(widget=forms.RadioSelect, choices=Platform_Is_Certification, label='platform_is_certification', required=False)
    platform_certification_true_name = forms.CharField(label='platform_certification_true_name', required=False)
    platform_certification_id_card = forms.CharField(label='platform_certification_id_card', required=False)                        

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（必填）用户名',
                                                                'autocomplete': 'off'})
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control',
                                                               'placeholder': '（必填）输入密码',
                                                               'autocomplete': 'off'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': '（必填）请再次输入密码',
                                                               'autocomplete': 'off'})
        self.fields['leadercode'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（必填）请输入邀请码',
                                                               'autocomplete': 'off'})
        self.fields['true_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（必填）请输入姓名',
                                                               'autocomplete': 'off'})
        self.fields['phone'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（必填）请输入手机号',
                                                               'autocomplete': 'off'})                                                                
        self.fields['wechat'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（必填）请输入微信号',
                                                               'autocomplete': 'off'})         
        self.fields['wechat_nickname'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入微信昵称',
                                                               'autocomplete': 'off'})  
        self.fields['qq'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入QQ号',
                                                               'autocomplete': 'off'})                                                                                                                                                                                                                                       
        self.fields['birthday'].widget = DateInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入出生日期，例如：1949-10-1',
                                                               'autocomplete': 'off'}, format='%Y-%m-%d')       
        self.fields['platform'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入平台',
                                                               'autocomplete': 'off'})                                                                 
        self.fields['platform_id'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入平台账号',
                                                               'autocomplete': 'off'})  
        self.fields['platform_password'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入平台密码',
                                                               'autocomplete': 'off'})      
        self.fields['platform_certification_true_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入实名认证姓名',
                                                               'autocomplete': 'off'})      
        self.fields['platform_certification_id_card'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '（选填）请输入实名认证身份证',
                                                               'autocomplete': 'off'})                                                                                                                                                                                                                                                                                                                                                                                                                                           

                                                                                                                                                                                                                                                                                                                       

                                                               
