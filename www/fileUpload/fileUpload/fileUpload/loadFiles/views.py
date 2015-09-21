from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from models import User

class UserForm(forms.Form):
	username=forms.CharField()
	headImg=forms.FileField()


def register(request):
	if request.method=="POST":
		uf=UserForm(request.POST, request.FILES)
		if uf.is_valid():
			username=uf.cleaned_data['username']
			headImg=uf.cleaned_data['headImg']
			
			user=User()
			user.username=username
			user.headImg=headImg
			user.save()

			return HttpResponse("upload ok")
	else:
		uf=UserForm()
	return render_to_response("register.html",{'uf':uf})

# Create your views here.
