from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from myproject import models as myproject_models  
from . import models

import time

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/' :
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

def adminhome(request):
    #print(request.session["sunm"])
    return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def addtenders(request):
    sclist=models.SubCategory.objects.all()
    if request.method=="GET":
        return render(request,"addtenders.html",{"sunm":request.session["sunm"],"sclist":sclist,"output":""})    
    else:
        title=request.POST.get("title")
        subcatname=request.POST.get("subcatname")
        description=request.POST.get("description")
        ldate=request.POST.get("ldate")
        edate=request.POST.get("edate")

        p=models.Tenders(title=title,subcatname=subcatname,description=description,ldate=ldate,edate=edate,info=time.asctime())

        p.save()

        return render(request,"addtenders.html",{"sunm":request.session["sunm"],"sclist":sclist,"output":"Tender launched....."})                        

def manageusers(request):
    userDetails=myproject_models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})

def manageuserstatus(request):
    email=request.GET.get("email")                
    s=request.GET.get("s")
    if s=="block":
        myproject_models.Register.objects.filter(email=email).update(status=0)
    elif s=="verify":
        myproject_models.Register.objects.filter(email=email).update(status=1)             
    else:
        myproject_models.Register.objects.filter(email=email).delete()        
    return redirect("/myadmin/manageusers/")        

def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{"output":"","sunm":request.session["sunm"]})
    else:
        catname=request.POST.get("catname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.Category(catname=catname,caticonname=filename)
        p.save()
        return render(request,"addcategory.html",{"output":"Category added successfully....","sunm":request.session["sunm"]})

def addsubcategory(request):
    clist=models.Category.objects.all()    
    if request.method=="GET":
        return render(request,"addsubcategory.html",{"output":"","clist":clist,"sunm":request.session["sunm"]})
    else:
        catname=request.POST.get("catname")
        subcatname=request.POST.get("subcatname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticonname=filename)
        p.save()
        return render(request,"addsubcategory.html",{"output":"Sub Category added successfully....","clist":clist,"sunm":request.session["sunm"]})        



