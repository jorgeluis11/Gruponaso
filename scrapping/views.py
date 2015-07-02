from django.shortcuts import HttpResponse
import requests
import time
import simplejson
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import mechanize

link = {
    "groopanda": {
        "link": "http://www.groopanda.com/todos",
        "element": "li.list_item_product"
    },
    "oferta": {
        "link": "http://www.ofertadeldia.com/puerto-rico-ofertas/oferta",
        "element": ".wrapping .item"
    },
    "ofertones": {
        "link": "http://www.ofertones.com/pr",
        "element": "a.js_offer"
    },
    "groupon": {
        "link": "http://www.groupon.com.pr/browse/san-juan?context=local",
        "element": "figure.deal-card"
    },
    "gustazos": {
        "link": "http://www.gustazos.com/?utm_source= \
        splashpage&utm_medium=website&utm_campaign=2012-10-SplashPageCity-PR",
        "element": "div.boxContent"
    },
    "peroquedescuentos": {
        "link": "http://peroquedescuentos.com/active",
        "element": "div.content"
    },
    "prgoza": {
        "link": "http://www.prgoza.com/deal/all",
        "element": "div.allDeal"
    },
    # "caprichos": {
    #     "link": "http://www.prgoza.com/deal/all",
    #     "element": "div.allDeal"
    # }
    "kokigo": {
        "link": "http://www.kokigo.com/discountdeal/",
        "element": "div.Getway_second_priority"
    },
    "puertoricolike": {
        "link": "http://www.puertoricolike.com/ofertas/deals/recent/",
        "element": "li.item"
    }
}

page_list = {'pages': ["oferta", "peroquedescuentos", "ofertones", "groupon",
                       "groopanda", "gustazos", "peroquedescuentos", "kokigo",
                       "puertoricolike"]}

limit = 6


def index(request):
    if request.GET:
        start = int(request.GET.get("start"))
        end = start + limit
        index = int(request.GET.get("index"))
        next = 0
        company_list = request.GET.get("list").split(",")

        groupon = get_groupon(start, end, index, company_list)
        length = len(groupon)
        print length
        if length != limit:
            next = limit - length
            index = index + 1
            start = next
            print next
            next_group = get_groupon(0, next, index, company_list)
            if next_group:
                groupon = groupon + next_group

        data = {
            'start': start,
            'end': end,
            'index': index,
            "items": groupon
        }
    else:
        data = {}
    return HttpResponse(simplejson.dumps(data),
                        content_type='application/json')


def get_groupon(start, end, index, company_list):
    company = company_list[index]
    items = []

    if company == "groopanda":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)
        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            items.append({
                'from': "groopanda",
                # "title": item_el.children(".list_item_merchant").text(),
                "title": item_el.children(".list_item_title").text(),
                "image": item_el.children(".list_item_image img").attr["src"],
                "link": item_el.children(".list_item_image").attr["href"],
                "price": item_el.find(".button_price").text(),
            })
    elif company == "oferta":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)

        if start is 0:
            target = d(".intro")
            price = target.find(".price").text()
            s = price.find('$')

            items.append(
                {
                    'from': "oferta",
                    # "title": d(".name").text(),
                    "title": target.find(".intro-heading").text(),
                    "image": target.find(".mobile-hidden").attr["src"],
                    "link": target.find("a").attr["href"],
                    "price": price[s:len(price)].replace(" ", ""),
                })
            end = end - 1

        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            items.append(
                {
                    'from': "oferta",
                    # "title": item_el.find(".title").text(),
                    "title": item_el.find(".item-title").text(),
                    "image": item_el.find(".image-holder").children("img")
                    .attr["src"],
                    "link": "http://www.ofertadeldia.com" + item_el.
                    find("a").attr["href"],
                    "price": item_el.find(".price").text(),
                })
    elif company == "peroquedescuentos":
        br = mechanize.Browser()
        website = link.get(company)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; \
            Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 \
            Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        r = br.open(website.get("link"))
        r = br.open(website.get("link"))
        html = r.read()
        d = pq(html)
        elements = d(website.get("element"))

        if start is 0:
            first = d(".deal.box")
            # face = d(elements[0]).find("a").attr["href"]
            items.append(
                {
                    'from': "peroquedescuentos",
                    # "title": d(".name").text(),
                    "title": first.children("h1").text(),
                    "image": first.find(".picture_main").attr["src"],
                    "link" : first.find("a").attr["href"],
                    "price": first.find(".deal-price").html(),
                })
            start = start + 1
            end = end

        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            price = item_el.find(".price").text()
            price_index = price.find("$")
            items.append(
                {
                    'from': "peroquedescuentos",
                    # "title": item_el.find(".title").text(),
                    "title": item_el.find(".title").text(),
                    "image": "http://peroquedescuentos.com"+item_el.find("img").attr["src"],
                    "link": item_el.find("a").attr["href"],
                    "price": price[price_index:price_index + 4].replace(" ", ""),
                })
    elif company == "prgoza":
        br = mechanize.Browser()
        website = link.get(company)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; \
            Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 \
            Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        r = br.open(website.get("link"))
        r = br.open(website.get("link"))
        html = r.read()
        d = pq(html)
        elements = d(website.get("element"))

        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            price = item_el.find(".buy-deal").text()
            price_index = price.find("$")
            items.append(
                {
                    'from': "prgoza",
                    # "title": item_el.find(".title").text(),
                    "title": item_el.find(".allTitle").text(),
                    "image": item_el.find("img").attr["src"],
                    "link": "http://www.prgoza.com/" +
                            item_el.find("a").attr["href"],
                    "price": price[price_index:price_index + 5].replace(" ",""),
                })
    elif company == "ofertones":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)

        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            price = item_el.find(".pagas").text()
            items.append(
                {
                    'from': "ofertones",
                    "title": item_el.find(".desc").text(),
                    # "title": "",
                    "image": "http://www.ofertones.com" + item_el.
                    find("img").attr["src_m"],
                    "link": "http://www.ofertones.com" + item_el.attr["href"],
                    "price": price[0:len(price) - 5].replace(" ", "")
                })
    elif company == "kokigo":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)

        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            title = item_el.find(".hover_info").text()
            image = item_el.find(".getway_second-imgpanel>a").attr["style"]
            s = title.find('$')

            items.append(
                {
                    'from': "kokigo",
                    "title": title,
                    # "title": "",
                    "image": "http://www.kokigo.com" +
                             image[image.find("(") + 1: image.find(")")],
                    "link": "http://www.kokigo.com" +
                            item_el.find(".hover_info>a").attr["href"],
                    "price": title[s:s + 4].replace(" ", "")
                })
    elif company == "puertoricolike":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)

        for item in d(website.get("element"))[start:end]:
            item_el = d(item)
            # s = title.find('$')

            items.append(
                {
                    'from': "puertoricolike",
                    "title": item_el.find(".product-name").text(),
                    # "title": "",
                    "image": item_el.find(".recent-image").find("img").attr["src"],
                    "link": item_el.find(".recent-image").attr["href"],
                    # "price": title[s:s + 4].replace(" ", "")
                })
    elif company == "gustazos":
        br = mechanize.Browser()
        website = link.get(company)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; \
            Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 \
            Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        r = br.open(website.get("link"))
        r = br.open(website.get("link"))
        html = r.read()
        d = pq(html)
        elements = d(website.get("element"))

        if start is 0:
            first = d(elements[0])
            face = d(elements[0]).find("a").attr["href"]
            if face is None:
                elements.pop(1)
            items.append(
                {
                    'from': "gustazos",
                    # "title": first(".summary").children("h1").children("a").text(),
                    "title": first(".description").children("p").text(),
                    "image": first(".slideshow").find("img").attr["src"],
                    "link": "http://www.gustazos.com" + d(".summary").
                    find("a").attr["href"],
                    "price": first.find(".price").text()[0:4],
                })
            start = start + 1
            # end = end

        face = d(elements[1]).find("a").attr["href"]
        if face is None:
            elements.pop(1)

        for item in elements[start:end]:
            item_el = d(item)
            title = item_el.find(".company").text()
            text = item_el.find(".name").text()
            price = text.find("$")
            items.append({
                'from': "gustazos",
                # "title": title,
                "title": text,
                "image": item_el.find("img").attr["src"],
                "link": "http://www.gustazos.com%s" % (
                    item_el.find(".company").attr["href"]),
                "price": text[price:price + 4].rstrip().replace(".", ""),
            })
    elif company == "groupon":
        br = mechanize.Browser()
        website = link.get(company)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; \
            en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 \
            Firefox/3.0.1')]
        r = br.open(website.get("link"))
        r = br.open(website.get("link"))
        html = r.read()
        d = pq(html)
        print start
        if start is 0:
            first = d("#hero-tile")
            title = first(".hero-tile-title").text()
            price = title.find("$")

            items.append({
                'from': "groupon",
                # "title": first(".title").text(),
                "title": title,
                "image": first.find("img").attr["src"],
                "link": "http://www.groupon.com.pr%s" % (
                    first(".btn-buy").attr["href"]),
                "price": title[price:price + 4].rstrip(),
            })
            end = end - 1
        elements = d(website.get("element"))

        for item in elements[start:end]:
            item_el = d(item)
            title = item_el.find(".deal-title").text()
            prices = title.find("$")
            items.append({
                'from': "groupon",
                # "title": item_el(".deal-title").text(),
                "title": item_el(".deal-title").text(),
                "image": item_el.find("img.lazy-load").attr["data-original"],
                "link": "http://www.groupon.com.pr%s" % (
                    item_el(".deal-tile-inner").attr["href"]),
                "price": title[prices:prices + 4].rstrip(),
            })
    return items


def pages(request):
    return HttpResponse(simplejson.dumps(page_list),
                        content_type='application/json')


def my_print(x):
    print x


def groopanda():
    d = pq(url="http://www.groopanda.com/todos", parser="html")
    x = d(".list_products").html()
    return x

from push_notifications.models import GCMDevice


def registration(request):
    if request.GET:
        name = request.GET.get("name")
        regid = request.GET.get("regID")
        print regid
        try:
            device = GCMDevice.objects.get(registration_id=regid)
        except GCMDevice.DoesNotExist:
            device = None
        if(device is None):
            print "iffff"
            device = GCMDevice(name=name, registration_id=regid).save()
            print "stored"
            return HttpResponse("Si Guardo!!!!!")
        else:
            return HttpResponse("Existe!")
    return HttpResponse("Stored!!!")


def push_example(request):
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
    return HttpResponse("Send!!!")


def push_instant(request):
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
    return HttpResponse("Send!!!")
