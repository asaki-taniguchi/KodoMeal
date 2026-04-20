from django.shortcuts import render
from .forms import CustomUserCreationForm

def register_view(request):
    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form':form})

