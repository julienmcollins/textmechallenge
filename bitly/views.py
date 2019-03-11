from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import UrlForm, ChoiceForm, UrlFormChoice
from .models import Url, UrlChoice

from django.contrib import messages

# Generic imports
import random
import math

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = UrlFormChoice(request.POST)

        # check whether it's valid
        if form.is_valid():
            # Get what was just inputted and create new url model
            result = form.cleaned_data

            # Check for which one was clicked
            if result['url']:
                return HttpResponseRedirect(reverse('bitly:l'))
            elif result['short']:
                return HttpResponseRedirect(reverse('bitly:s'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UrlFormChoice()

    return render(request, 'bitly/index.html', {'form': form})

def result(request, url_id):
    url = get_object_or_404(Url, pk=url_id)
    return render(request, 'bitly/result.html', {'url': url})

def long(request, url_id):
    url = get_object_or_404(Url, pk=url_id)
    return render(request, 'bitly/long.html', {'url': url})

def request_l(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = UrlForm(request.POST)

        # check whether it's valid
        if form.is_valid():
            # Get what was just inputted and create new url model
            input_url = form.cleaned_data['url']
            get_url = Url.objects.filter(url__startswith=input_url)
            print (get_url)
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

    return render(request, 'bitly/l.html', {'form': form})

def request_s(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = ChoiceForm(request.POST)

        # check whether it's valid
        if form.is_valid():
            # Get what was just inputted and create new url model
            output_short = form.cleaned_data['short']
            get_short = Url.objects.filter(short__startswith=output_short)
            print(get_short)
            if get_short:
                url_id = get_short.first().id
                return HttpResponseRedirect(reverse('bitly:long', args=(url_id,)))
            else:
                messages.error(request, 'username or password not correct')
                render(request, 'bitly/s.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChoiceForm()

    return render(request, 'bitly/s.html', {'form': form})

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
