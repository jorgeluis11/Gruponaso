from django.shortcuts import render, HttpResponse
import requests
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import time
 

def index(request):
	d = pq(url="http://www.groopanda.com/todos", parser="html")
	x = d(".list_products").html()
	#print x
	return render(request, "index.html", {"products":x})

def groopanda():
	d = pq(url="http://www.groopanda.com/todos", parser="html")
	x = d(".list_products").html()
	return x

from push_notifications.models import APNSDevice, GCMDevice

def registration(request):
	if request.GET:
		name = request.GET.get("name")
		regid = request.GET.get("regID")
		print regid
		try:
			device = GCMDevice.objects.get(registration_id=regid)
		except GCMDevice.DoesNotExist:
			device = None
		if(device == None):
			print "iffff"
			device = GCMDevice(name=name, registration_id=regid).save()
			# The first argument will be sent as "message" to the intent extras Bundle
			# Retrieve it with intent.getExtras().getString("message")
			print "stored"
			return HttpResponse("Si Guardo!!!!!")
		else:
			return HttpResponse("Existe!")
		
	return HttpResponse("Stored!!!")

def pushExample(request):
	if request.GET:
		regid = request.GET.get("regID")
		try:
			device = GCMDevice.objects.get(registration_id=regid)
			time.sleep(10)
			device.send_message("Weeeepaleee")
			print "mail send"
			return HttpResponse("Sendend")
		except GCMDevice.DoesNotExist:
			device = None
			return HttpResponse("Push not send")
 
		# The first argument will be sent as "message" to the intent extras Bundle
		# Retrieve it with intent.getExtras().getString("message")
		
	return HttpResponse("Send!!!")

def pushInstant(request):
	if request.GET:
		regid = request.GET.get("regID")
		try:
			device = GCMDevice.objects.get(registration_id=regid)
			device.send_message("Weeeepaleee")
			print "mail send"
			return HttpResponse("Sendend")
		except GCMDevice.DoesNotExist:
			device = None
			return HttpResponse("Push not send")
 
		# The first argument will be sent as "message" to the intent extras Bundle
		# Retrieve it with intent.getExtras().getString("message")
		
	return HttpResponse("Send!!!")
#index("a")