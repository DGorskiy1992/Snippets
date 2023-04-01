from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment, User
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

from pygments import highlight
from pygments.lexers.c_cpp import CppLexer
from pygments.lexers.python import PythonLexer

from pygments.formatters import HtmlFormatter


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






@login_required
def snippet_delete(request, id):
    snippet = Snippet.objects.get(pk=id)
    snippet.delete()
    return redirect("snippets_list")


@login_required
def snippet_edit(request, id):
    try:
        snippet = Snippet.objects.get(pk=id)

        if request.method == "POST":
            snippet.name = request.POST.get("name")
            snippet.lang = request.POST.get("lang")
            snippet.is_public = request.POST.get("is_public")
            # snippet.lang = "python"
            snippet.code = request.POST.get("code")
            snippet.save()
            return redirect("snippets_list")
        else:
            return render(request, "pages/edit.html", {"snippet": snippet})
    except Snippet.DoesNotExist:
        raise Http404


def snippets_page(request):
    snippets = Snippet.objects.all()
    users = User.objects.annotate(Count("snippets"))
    sort = 'none'

    if request.user.is_anonymous:
        snippets = snippets.filter(is_public=True)
    else:
        snippets = snippets.filter(Q(is_public=True) | Q(user=request.user))

    if request.GET.get('reverse'):
        snippets = snippets.reverse()

    if request.GET.get("lang"):
        language = request.GET.get("lang")
        snippets = snippets.filter(lang=language)
        sort_type = request.GET.get("sort_method")
        if not (sort_type == 'none'):
            snippets = snippets.order_by(sort_type)

    if request.GET.get("sort"):
        sort = request.GET.get("sort")
        snippets = snippets.order_by(sort)

    if request.GET.get("selected_user"):
        selected_username = request.GET.get("selected_user")
        selected_user = User.objects.get(username=selected_username)
        snippets = snippets.filter(user=selected_user)


    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'quantity': len(snippets),
        'users': users,
        'sort_method': sort,
        }

    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, id):
    snippet = Snippet.objects.get(pk=id)
    form = CommentForm()
    code = snippet.code
    my_lexer = None
    if snippet.lang == "C++":
        my_lexer = CppLexer
    else:
        my_lexer = PythonLexer
    formatted_code = highlight(code, my_lexer(), HtmlFormatter())
    if request.user.is_anonymous:
        context = {
            "snippet": snippet,
            "code": formatted_code,
        }
    else:
        context = {
            "snippet": snippet,
            "form": form,
            "code": formatted_code,
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
        comment_form = CommentForm(request.POST, request.FILES)
        snipet_id = request.POST.get("snippet_id")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snipet_id)
            comment.save()

        return redirect(f'/snippets/{snipet_id}')

    raise Http404


def snippets_sort(request):
    field = request.GET.get("sort")
    if field in {'snip_name', 'snip_date', 'snip_auth'}:
        return snippets_page(request, field)
    else:
        raise Http404


def snippets_search(request):
    if request.method == "POST":
        try:
            snippet_id = request.POST.get("snid")
            snippet = Snippet.objects.get(pk=snippet_id)
            return snippet_page(request, snippet_id)
        except Snippet.DoesNotExist:
            return redirect('/')
    raise Http404


def users_rate(request):
    users = User.objects.all()

    class Rated_User:
        def __init__(self, id, name, snips, comms):
            self.id = id
            self.name = name
            self.snips = snips
            self.comms = comms

    rated_users = []
    total_snippets = 0
    total_comments = 0
    for user in users:
        user_snips = user.snippets.all()
        user_comms = user.comments.all()

        num_of_user_snips = user_snips.count()  # количество снипов и комментов от текущего юзера
        num_os_user_comms = user_comms.count()

        total_snippets += num_of_user_snips  # подсчитываем общее количество снипов и комментов на сайте от всех юзеров
        total_comments += num_os_user_comms

        new_user = Rated_User(user.id, user.username, num_of_user_snips, num_os_user_comms)
        rated_users.append(new_user)

        sort_field = request.GET.get("sort")
        if sort_field == "name" or not sort_field:
            rated_users.sort(key=lambda x: x.name)
        elif sort_field == "snippets":
            rated_users.sort(key=lambda x: x.snips, reverse=True)
        elif sort_field == "comments":
            rated_users.sort(key=lambda x: x.comms, reverse=True)

    context = {"users": rated_users,
               "total_snips": total_snippets,
               "total_comms": total_comments}

    return render(request, 'pages/users_rating.html', context)
