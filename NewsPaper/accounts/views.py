from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import *

class AuthorList(ListView):
    model = Author



