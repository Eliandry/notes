from django.shortcuts import render
import os
import random
from cryptography.fernet import Fernet
from .forms import TextForm
from .models import Note
def index(request):
    form=TextForm()
    if request.method == "POST":
        key = Fernet.generate_key()
        str_key = key.decode('ascii')
        f = Fernet(key)
        bin_string = form.data.encode('utf-8')
        cipher_text = f.encrypt(bin_string)
        str_cipher_text = cipher_text.decode('ascii')
        rnumber = random.randint(1000000, 9999999)
        cipher_note = Note(number=rnumber, text=str_cipher_text)
        cipher_note.save()
        link = f'http://127.0.0.1:8000/{rnumber}/{str_key}'
        return render(request,'over.html', {'link':link})

    return render(request,'index.html', {'form':form})
def decrypt(request,rnumber, str_key):
    cipher_note = Note.objects.get(number=rnumber)
    cipher_text=cipher_note.text.encode('ascii')
    key = str_key.encode('ascii')
    try:
        f = Fernet(key)
        text = f.decrypt(cipher_text)
    except (ValueError,):
        return render(request,'error.html')
    text = text.decode('utf-8')
    cipher_note.delete()
    return render(request,'decrypt.html',{'text':text})