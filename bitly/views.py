# References: https://stackoverflow.com/questions/5129402/access-instance-passed-to-modelform-from-cleanself-method
# https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#overriding-the-clean-method
# 


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import UrlForm
from .models import Url

# Generic imports
import random
import math

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = UrlForm(request.POST)

        # check whether it's valid
        if form.is_valid():
            # Get what was just inputted and create new url model
            input_url = form.cleaned_data['url']
            output_short = form.cleaned_data['short']
            get_url = Url.objects.filter(url__startswith=input_url)
            get_short = Url.objects.filter(short__startswith=output_short)
            print (input_url)
            print (output_short)
            if output_short != "" and input_url == "":
                url_id = get_url.first().id
                print ("hello")
                return HttpResponseRedirect(reverse('bitly:long', args=(url_id)))
            if not get_url:
                form.save()
                get_url = Url.objects.filter(url__startswith=input_url)
                url_id = get_url.first().id
                url = get_object_or_404(Url, pk=url_id)
                url.short = "http://text.me/" + shorten(url.id)
                url.save()
                print (url.id)
                print (url.short)
                print (url.url)
                return HttpResponseRedirect(reverse('bitly:result', args=(url.id,)))
            else:
                url_id = get_url.first().id
                url = get_object_or_404(Url, pk=url_id)
                return HttpResponseRedirect(reverse('bitly:result', args=(url.id,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UrlForm()

    return render(request, 'bitly/index.html', {'form': form})

def result(request, url_id):
    url = get_object_or_404(Url, pk=url_id)
    return render(request, 'bitly/result.html', {'url': url})

def long(request, url_id):
    url = get_object_or_404(Url, pk=url_id)
    return render(request, 'bitly/long.html', {'url': url})

# This will be the logic for the url shortening and resolving
def shorten(url_id):
    # Convert url to int
    digits = []

    # store the digits
    while url_id > 0:
        rem = (int) (url_id % 62)
        digits.append(rem)
        url_id = (int) (url_id / 62)
    digits = digits[::-1]

    # Now get a translation of the digits
    result = ""
    for i in digits:
        if i < 26:
            result = chr(i + 97) + result
        elif i >= 26 and i < 53:
            result = chr(i + 39) + result
        else:
            result = chr(i - 5) + result

    return result

# Get the original one back
def lengthen(short_url):
    result = 0
    short_url = short_url[::-1]
    for c in range(0, len(short_url)):
        if short_url[c].islower():
            result += (ord(short_url[c]) - 97) * int(math.pow(62, c))
        elif short_url[c].isupper():
            result += (ord(short_url[c]) - 39) * int(math.pow(62, c))
        else:
            result += (ord(short_url[c]) + 5) * int(math.pow(62, c))
    url = get_object_or_404(Url, pk=result)
    return url.url
