from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

class MyView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dcashier/static/index.html')
        #return render(request, 'static/index.html')
        #return HttpResponse('Hello, World!')
