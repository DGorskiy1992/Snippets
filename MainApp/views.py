from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm
from django.contrib import auth


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid(): #инфа из формы
            form.save()
            return redirect("snippets_list")


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,

    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    context = {
        "snippet": snippet
    }
    return render(request, 'pages/snippet.html', context)


def login_page(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
   return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')