from django.shortcuts import render, HttpResponse
import requests
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import time
import simplejson

link = [["groopanda","http://www.groopanda.com/todos","li.list_item_product"],
		["oferta","http://www.ofertadeldia.com/puerto-rico-ofertas/oferta",""]]

def index(request):
	if request.GET:
		start = int(request.GET.get("start"))
		end   = int(request.GET.get("end"))
		list  = ["groopanda","oferta"]
		index = 0
		next  = 0

		groupon = []
		groupon = getGroupon(start, end, index)
		
		length = len(groupon)
		if(length != 10):
			next  = length
			index = index + 1
			nextGroup = getGroupon(0, next, index)
			if nextGroup:
				groupon.append(nextGroup)
			
		
		items = []
		
		for item in groupon:
			itemEl = pq(item)

			items.append({
				"title": itemEl.children(".list_item_merchant").text() ,
				"text" : itemEl.children(".list_item_title").text(),
				"image": itemEl.children(".list_item_image img").attr["src"],
				"link" : itemEl.children(".list_item_image").attr["href"], 
			})
		
		data = {
			"items" : items
		}
	else:
		data = {}

	#data = {
	#	"text"  : "text",
	#	"images": [d(item).attr["src"] for item in d("ul.list_products").find("img")],
	#	"links" : [d(item).attr["href"] for item in d("ul.list_products").find("a")]
	#}
	#print d(".list_products").find(".list_item_image")
	return HttpResponse(simplejson.dumps(data), content_type='application/json')

def getGroupon(start,end,index):
	if link[index][0] == "groopanda":
		response = requests.get(link[index][1])
		d = pq(response.content)
		return d(link[index][2])[start:end]
	elif link[index][0] == "oferta":
		response = requests.get(link[index][1])
		d = pq(response.content)
		return d(link[index][2])[start:end]

#use Later
#response = requests.get(link)
#			d2 = pq(response.content)
#							'phone': d2(".product_fine_print").text(),


def my_print(x):
    print x

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