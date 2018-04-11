from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from models import Signup
from bs4 import BeautifulSoup
from SOD import objdetect,preprocess,analysed,dash,sentiment
# Create your views here.
import urllib, json
def signup(request):
	if request.method == 'GET':
		signup=Signup()
		print signup.name
		return render(request,"signup.html",{})
	elif request.method == 'POST':
		signup=Signup()
		value=0
		print "requesmethod",request.method
		name=request.POST.get("name" or None)
		if name is None or '' or len(name)==0:
			print "name"
			value=1
		print "len name",len(name)
		email=request.POST.get("email" or None)
		if email== None or '@' not in email:
			print "email"
			value=2
		passwd=request.POST.get("passwd" or None)
		if passwd== None or len(passwd)<8:
			print "passwd"
			value=3
		exist=Signup.objects.filter(name=name)
		if len(exist)>0 and value!=1:
			value=4
		print value
		if value==1:
			return render(request,"signup.html",{'noname':True})
		elif value==2:
			return render(request,"signup.html",{'noemail':True})
		elif value==3:
			return render(request,"signup.html",{'nopasswd':True})
		elif value==4:
			return render(request,"signup.html",{'existing':True})
		p=Signup(name=name,email=email,passwd=passwd)
		p.save()
		return render(request,"signup.html",{})

def login(request):
	if request.method=='GET':
		return render(request,"login.html",{})
	elif request.method=='POST':
		username=request.POST.get("name")
		password=request.POST.get("passwd")
		print username,password
		try:
			signedname=Signup.objects.get(name=username)
			print signedname.passwd
			if str(signedname.passwd) == str(password):
				request.session['member_id']=signedname.id
				print "sesion is for",request.session['member_id']
				return HttpResponseRedirect('/wordpress/')
			else:
				return render(request,"login.html",{'invalid':True})# -*- coding: utf-8 -*-
		except:
			return render(request,"login.html",{'there':True})



def userlogin(request):
	if request.method == 'GET':
		userid=request.session['member_id']
		print "userid",userid
		signupobj=Signup.objects.get(id=userid)
		name=signupobj.name
		return render(request,"userlogin.html",{'name':name})

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request,"logout.html",{})

def home(request):
	return render(request,"home.html",{})


def sentiment(request):
	token=request.GET.get("access_token")
	print token
	return HttpResponseRedirect('/sentiment/')

def demo(request):
	return HttpResponse('THANKS')


def post(request):
	try:
		if request.method == 'GET':
			url="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts?pretty=true"
			response=urllib.urlopen(url)
			data=json.load(response)
			global data
			# print "data-----------",data
			found=data['found']
			global found
			# print "found",found
			html_doc=[]
			try:
				for i in range(0,found):
					current_post=data['posts'][i]['ID']
					print "current id is",current_post
					current_content=data['posts'][i]['content']
					current_format=data['posts'][i]['format']
					titlefound=data['posts'][i]['title']
					print "titlefound",titlefound
					if current_format=="image":
						if title_found == title:
							image=data['posts'][i]['content']
							soups = BeautifulSoup(image, 'lxml')
							print "souppppp",soups
							myattr = soups.find('img')
							myimglink=myattr.attrs['data-medium-file']
							print "MYimgLINK IS=",myimglink	
					else:
						continue
				return HttpResponseRedirect(myimglink)
			except:
				return HttpResponse('ERROR OCCURED!')
	except:
		return  HttpResponseRedirect("wordpress.html")
		










































			# if request.method == 'GET':
			# 	return render(request,"module1.html",{})
			# else:
			# 	global sitename
			# 	sitename=request.POST.get("sitename")
			# 	global sitename
			# 	title=request.POST.get("title")
			# 	print "sitename is",sitename
			# 	url="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts?pretty=true"
			# 	response=urllib.urlopen(url)
				
			# 	data=json.load(response)
			# 	global data
			# 	print "data is--------",data
			# 	found=data['found']
			# 	html_doc=[]
			# 	try:
			# 		for i in range(0,found):
			# 			titlefound=data['posts'][i]['title']
			# 			print "title found is",titlefound,"and title given was",title
			# 			if title==titlefound:
			# 				print "i is..........//////////////////////////",0
			# 				html_doc.append(data['posts'][i]['content'])
			# 				print "HTML DOC=**********",html_doc
			# 				mytxt=html_doc[i]
			# 				print "mytext =*****",mytxt
			# 				soup = BeautifulSoup(mytxt, 'lxml')
			# 				print "souppppp",soup
			# 				mylink = soup.find('img')
			# 				print "MYLINK IS=",mylink
			# 				analyse=mylink.attrs['data-medium-file']
			# 			else:
			# 				continue
			# 		return HttpResponseRedirect(analyse)
			# 	except:
			# 		return HttpResponse('ERROR OCCURED!')



def dashboard(request):
	try:
		if request.method=='GET':
			url="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts?pretty=true"
			response=urllib.urlopen(url)
			
			data=json.load(response)
			# print "dashboard",data['posts']
			POSTS=[]
			IDS=[]
			TITLE=[]
			LIKES=[]
			COMMENT_no=[]
			for i in range(0,found):
				POSTS.append(data['posts'][i]['content'])
				IDS.append(data['posts'][i]['ID'])
				TITLE.append(data['posts'][i]['title'])
				COMMENT_no.append(data['posts'][i]['discussion']['comment_count'])
				LIKES.append(data['posts'][i]['like_count'])

			COMMENT_ALL=[]
			dash={
			"NO_IMG":[]
			}

			for i in range(0,found):
				current_post=data['posts'][i]['ID']
				print "current id is",current_post
				current_content=data['posts'][i]['content']
				current_format=data['posts'][i]['format']
				if current_format=="image":
					image=data['posts'][i]['content']
					soups = BeautifulSoup(image, 'lxml')
					print "souppppp",soups
					myattr = soups.find('img')
					myimglink=myattr.attrs['data-medium-file']
					print "MYimgLINK IS=",myimglink
					urlall="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts/"+str(current_post)+"/replies?pretty=true"
					responseall=urllib.urlopen(urlall)
					dataall=json.load(responseall)
					comment_counter=dataall['found']
					if comment_counter>0:
						dash[myimglink]=[]
						for j in range(0,comment_counter):
							comment_all=dataall['comments'][j]['raw_content']
							print "comment all",comment_all
							dash[myimglink].append(comment_all)
							print "dash[myimglink]",dash[myimglink]
					else:
						dash[myimglink]="NAN"
				else:
					urlall="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts/"+str(current_post)+"/replies?pretty=true"
					responseall=urllib.urlopen(urlall)
					dataall=json.load(responseall)
					comment_counter=dataall['found']
					print "found no img contents",comment_counter
					if comment_counter>0:
						for j in range(0,comment_counter):
							comment_all=dataall['comments'][j]['raw_content']
							print "comment all",comment_all
							dash["NO_IMG"].append(comment_all)
							print "dash[no img]",dash["NO_IMG"]
					else:
						dash["NO_IMG"]="NAN"
				print "final dictionary is",dash




				# print "DASH"
				# print i
				# print IDS[i]
				# urlall="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts/"+str(IDS[i])+"/replies?pretty=true"
				# responseall=urllib.urlopen(urlall)
				# dataall=json.load(responseall)
				# # print dataall
				# comment_counter=dataall['found']
				# if comment_counter>0:
				# 	for j in range(0,comment_counter):
				# 		if dataall['comments'][j]['format']=="image":
				# 			image=dataall['comments'][j]['content']
				# 			print "image is at",image
				# 			soups = BeautifulSoup(image, 'lxml')
				# 			print "souppppp",soups
				# 			myattr = soups.find('img')
				# 			myimglink=mylink.attrs['data-medium-file']
				# 			print "MYimgLINK IS=",myimglink
				# 		comment_all=dataall['comments'][j]['raw_content']
				# 		print "comma ll",comment_all
				# 		COMMENT_ALL.append(comment_all)
				# print COMMENT_ALL
			d={
			"data":data['posts'],
			"range":range(found),
			"POSTS":POSTS,
			"ID":IDS,
			"TITLE":TITLE,
			"COMMENT_NO":COMMENT_no,
			"LIKES":LIKES
			}
			lists=zip(POSTS,IDS,TITLE,COMMENT_no,LIKES)
			# print d['data']
			# print "id is",d['TITLE']
			return render(request,"mod1.html",{'lists':lists})
		# return HttpResponse('DASHBOARD')
	except:
		return  HttpResponseRedirect("/wordpress/")






















def wordpress(request):
	if request.method == 'GET':
		return render(request,"module2.html",{})
	else:
		global sitename
		sitename=request.POST.get("sitename")
		global sitename
		title=request.POST.get("title")
		global title
		print "sitename is",sitename
		url="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts?pretty=true"
		response=urllib.urlopen(url)
		data=json.load(response)
		global data
		found=data['found']
		global found
	return render(request,"userlogin.html",data)

def delete(request):
	code=request.GET['code']
	print "code acheived is",code
	# urlauth=
	return render(request,"delete.html",{"comcode":code,"there":True})

def analyse(request,ids):
	try:
		if request.method == 'GET':
			urlcom="https://public-api.wordpress.com/rest/v1.1/sites/"+sitename+".wordpress.com/posts/"+ids+"/replies?pretty=true"
			# print "urlco is",urlcom
			responsecom=urllib.urlopen(urlcom)
			# print "response com",responsecom
			datacom=json.load(responsecom)
			print "datacom",datacom
			global datacom
			# print "data-----------",data
			foundcom=datacom['found']
			# print "found com",foundcom
			global foundcom
			print "found",foundcom
			COMMENT=[]
			html_doccomc=[]
			try:
				# print "in trysdsdvdsfbfbngfngngfnfgn"
				for i in range(0,foundcom):
					print "i is..........//////////////////////////",i
					# print "**********************",data['posts'][i]['title']
					com=datacom['comments'][i]['raw_content']
					# print "com is",com
					# comm=BeautifulSoup(com,"lxml")
					# print "comm is",comm
					COMMENT.append(com)
					print "comment found is",COMMENT[i]
					analysed_list=analysed(COMMENT)
					print "result from func",analysed_list

				return HttpResponse('analysed')
			except:
				return HttpResponse('ERROR OCCURED!')
	except:
		return  HttpResponseRedirect("/wordpress/")
			# if request.method == 'GET':

def delcomment(request):
	comcode=request.GET['comcode']
	print "code acheived is",comcode
	dic={
	"valid":True,
	"comcode":comcode
	}
	return render(request,"delete.html",dic)
