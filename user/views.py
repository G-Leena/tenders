from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings

from . import models
from myadmin import models as myadmin_models
from myproject import models as myproject_models


media_url=settings.MEDIA_URL

import time

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/viewtenders/' or request.path=='/user/viewsubcat/' :
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def viewtenders(request):
    clist=myadmin_models.Category.objects.all() 
    return render(request,"viewtenders.html",{"clist":clist,"media_url":media_url,"sunm":request.session["sunm"]})

def viewsearchtenders(request):
	subcatname=request.GET.get("subcatname")
	sclist=myadmin_models.SubCategory.objects.all() 
	tlist=myadmin_models.Tenders.objects.filter(subcatname=subcatname)
	return render(request,"viewsearchtenders.html",{"subcatname":subcatname,"sclist":sclist,"tlist":tlist,"sunm":request.session["sunm"]})

def viewsubcat(request):
    catname=request.GET.get("catname")
    clist=myadmin_models.Category.objects.all()
    sclist=myadmin_models.SubCategory.objects.filter(catname=catname)
    return render(request,"viewsubcat.html",{"catname":catname,"clist":clist,"sclist":sclist,"media_url":media_url,"sunm":request.session["sunm"]})

def funds(request):
	paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
	paypalID="sb-mf0fq22348299@business.example.com"
	#sb-wnchj23515501@personal.example.com
	amt=100
	return render(request,"funds.html",{"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})

def payment(request):
	uid=request.GET.get("uid")	
	amt=request.GET.get("amt")
	p=models.Payment(uid=uid,amt=amt,info=time.asctime())
	p.save()
	return redirect("/user/success/")

def success(request):
    return render(request,"success.html",{"sunm":request.session["sunm"]})

def cancel(request):
    return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def viewfunds(request):
	fDetails=models.Payment.objects.all()
	return render(request,"viewfunds.html",{"sunm":request.session["sunm"],"fDetails":fDetails})

def cpuser(request):
	if request.method=="GET":
		return render(request,"cpuser.html",{"sunm":request.session["sunm"]})
	else:
		sunm=request.session["sunm"]
		opass=request.POST.get("opass")
		npass=request.POST.get("npass")	
		cnpass=request.POST.get("cnpass")

		userDetails=myproject_models.Register.objects.filter(email=sunm,password=opass)
		if len(userDetails)>0:
			if npass==cnpass:
				myproject_models.Register.objects.filter(email=sunm).update(password=cnpass)
				return render(request,"cpuser.html",{"sunm":sunm,"output":"Password changed successfully...."})
			else:
				return render(request,"cpuser.html",{"sunm":sunm,"output":"New & Confirm new password mismatch"})		
		else:
			return render(request,"cpuser.html",{"sunm":sunm,"output":"Invalid old password"})				
		
def epuser(request):
	sunm=request.session["sunm"]
	if request.method=="GET":
		if request.GET.get("result")==None:
			output=""
		else:
			output="User Details Updated Successfully...."		
		userDetails=myproject_models.Register.objects.filter(email=sunm)
		m,f="",""
		if userDetails[0].gender=="male":
			m="checked"
		else:
			f="checked"			
		return render(request,"epuser.html",{"sunm":sunm,"userDetails":userDetails[0],"output":output,"m":m,"f":f})
	else:
		name=request.POST.get("name")
		email=request.POST.get("email")
		mobile=request.POST.get("mobile")
		address=request.POST.get("address")
		city=request.POST.get("city")
		gender=request.POST.get("gender")
		
		myproject_models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)
		
		return redirect("/user/epuser/?result=1")	