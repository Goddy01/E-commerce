from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .forms import PaymentForm
from .models import Payment
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.http import HttpRequest, HttpResponse

