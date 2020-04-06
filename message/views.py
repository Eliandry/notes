from django.shortcuts import render
import os
import random
from cryptography.fernet import Fernet
from .models import Note
from django.http import HttpResponseRedirect,HttpResponseServerError
def index(request):
    if request.method == "POST":
        key = Fernet.generate_key()
        str_key = key.decode('ascii')
        rnumber = random.randint(1000000, 9999999)
        cipher_note = Note(number=rnumber, text=request.POST.get("texta"))
        cipher_note.save()
        link = f'http://127.0.0.1:8000/{rnumber}/{str_key}'
        return render(request,'over.html', {'link':link})

    return render(request,'index.html')
def open(request,rnumber,str_key):
    if request.method == "POST":
        return HttpResponseRedirect(f'http://127.0.0.1:8000/decrypt/{rnumber}/{str_key}')
    return render(request,'open.html')
def decrypt(request,rnumber, str_key):
    try:
        cipher_note = Note.objects.get(number=rnumber)
    except:
        return render(request,'oops.html')
    cipher_text=cipher_note.text
    key = str_key.encode('ascii')
    try:
        f = Fernet(key)
        text = cipher_text
    except (ValueError):
        return HttpResponseServerError
    cipher_note.delete()
    return render(request,'decrypt.html',{'text':text})