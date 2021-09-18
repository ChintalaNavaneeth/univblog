from django.shortcuts import render, redirect
from django.http import Http404
from .models import Post, Author, subscribe, Contact, Comment, SubComment
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import *


from login.models import profile
from django.contrib.auth.models import User
from .forms import *


def index(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if email:
            subscribe(email=email).save()

    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Post.objects.filter(time_upload__gte=week_ago).order_by('-read')
    TopAuthors = Author.objects.order_by('-rate')[:4]
    AuthorsPost = [Post.objects.filter(
        auther=author).first() for author in TopAuthors]

    print(AuthorsPost)

    all_post = Paginator(Post.objects.filter(publish=True), 3)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)

    parms = {
        'posts': posts,
        'trends': trends[:5],
        'author_post': AuthorsPost,
        'pop_post': Post.objects.order_by('-read')[:9],
    }
    return render(request, 'index.html', parms)


def about(request):
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Post.objects.filter(time_upload__gte=week_ago).order_by('-read')
    TopAuthors = Author.objects.order_by('-rate')[:4]
    AuthorsPost = [Post.objects.filter(
        auther=author).first() for author in TopAuthors]

    all_post = Paginator(Post.objects.filter(publish=True), 3)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)
    parms = {
        'title': 'Univ`Blog',
        'posts': posts,
        'trends': trends[:5],
        'author_post': AuthorsPost,
        'pop_post': Post.objects.order_by('-read')[:9],

    }
    return render(request, 'about.html', parms)


def post(request, id, slug):
    try:
        post = Post.objects.get(pk=id, slug=slug)
    except:
        raise Http404("Post Does Not Exist")

    post.read += 1
    post.save()

    if request.method == 'POST':
        comm = request.POST.get('comm')
        comm_id = request.POST.get('comm_id')  # None

        if comm_id:
            SubComment(post=post,
                       user=request.user,
                       comm=comm,
                       comment=Comment.objects.get(id=int(comm_id))
                       ).save()
        else:
            Comment(post=post, user=request.user, comm=comm).save()

    comments = []
    for c in Comment.objects.filter(post=post):
        comments.append([c, SubComment.objects.filter(comment=c)])
    parms = {
        # 'info': x,
        'comments': comments,
        'post': post,
        'pop_post': Post.objects.order_by('-read')[:9],
    }
    return render(request, 'blog-single.html', parms)


def contact(request):
    if request.method == 'POST':
        name = f"{request.POST.get('fname')} {request.POST.get('lname')}"
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        mess = request.POST.get('mess', 'default')

        Contact(name=name, email=email, mob=mob, mess=mess).save()
    return render(request, 'contact.html')


def search(request):
    q = request.GET.get('q')
    posts = Post.objects.filter(
        Q(title__icontains=q) |
        Q(overview__icontains=q)
    ).distinct()

    parms = {
        'posts': posts,
        'title': f'Search Results for {q}',
        'pop_post': Post.objects.order_by('-read')[:9],
    }

    return render(request, 'all.html', parms)


def view_all(request, query):
    week_ago = datetime.date.today() - datetime.timedelta(days=7)

    acpt = ['trending', 'popular']
    q = query.lower()
    if q in acpt:
        if q == acpt[0]:
            parms = {
                'posts': Post.objects.filter(time_upload__gte=week_ago).order_by('-read'),
                'title': "Trending Posts",
                'pop_post': Post.objects.order_by('-read')[:9],
            }
        elif q == acpt[1]:
            parms = {
                'posts': Post.objects.order_by('-read'),
                'title': "Trending Posts",
                'pop_post': Post.objects.order_by('-read')[:9],
            }
        else:
            pass

    return render(request, 'all.html', parms)


@login_required(login_url='signin')
def newblog(request, id):
    info = User.objects.get(id=id)
    authorname = Author.objects.get(user=info)
    initial_dict = {
        "auther": authorname
    }
    form = createblog(initial=initial_dict)
    form.fields['auther'].widget = forms.HiddenInput()
    form.fields['read'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = createblog(request.POST,  request.FILES, initial=initial_dict)
        print(form.errors)
        if form.is_valid():
            img = form.cleaned_data.get("thumbnail")
            print(img)
            form.save()
            return redirect('home')
    parms = {'form': form}
    return render(request, 'newblog.html', parms)


@login_required(login_url='signin')
def editblog(request, id):
    userpost = Post.objects.all()
    for x in userpost:
        if x.id == id:
            mainid = x.id
    userpostfile = Post.objects.get(id=mainid)
    form = editblogs(instance=userpostfile)
    if request.method == 'POST':
        form = createblog(request.POST,  request.FILES, instance=userpostfile)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, f"Blog Updated")
            return redirect('home')
    parms = {'form': form}
    return render(request, 'editblog.html', parms)


@login_required(login_url='signin')
def deleteblog(request, id):
    postid = Post.objects.filter(id=id)
    if request.method == 'POST':
        postid.delete()
        return redirect('home')
    parms = {'postid': postid}
    return render(request, 'deleteblog.html', parms)


def pagenotfound(request, exception):
    return render(request, 'pagenotfound.html')
