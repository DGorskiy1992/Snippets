from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
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
        if form.is_valid():  # инфа из формы
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
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
    form = CommentForm()
    context = {
        "snippet": snippet,
        "form": form
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


def register(request):
    if request.method == "GET":
        form = UserRegistrationForm
        context = {'pagename': 'Регитрация пользователя', 'form': form}
        return render(request, 'pages/registration.html', context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        context = {'pagename': 'Регитрация пользователя', 'form': form}
        return render(request, 'pages/registration.html', context)


def my_snips(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,

    }
    return render(request, 'pages/view_snippets.html', context)


def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snipet_id = request.POST.get("snippet_id")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snipet_id)
            comment.save()

        return redirect(f'/snippets/{snipet_id}')

    raise Http404
