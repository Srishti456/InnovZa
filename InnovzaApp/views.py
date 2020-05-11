from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from .forms import UserDataForm,CommentForm,ProjectCommentForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
import yagmail
import os
import pyotp
from django.conf import settings
from .models import UserInfo,Post,Category,Project,PostView,ProjectView
from django.db.models import Count,Q

# Create your views here.
def search(request):
    queryset=Post.objects.all()
    query=request.GET.get('q')
    if query:
        queryset=queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
        context={
            'queryset':queryset,
            'query': query,
        }
    return render(request,'search_results.html',context)

register = template.Library()
@register.filter
def highlight_search(text, search):
    highlighted = text.replace(search, '<span class="highlight">{}</span>'.format(search))
    return mark_safe(highlighted)

def get_category_count():
    from django.db.models import Count
    queryset=Post\
        .objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    featured1=Project.objects.filter(featured=True)
    latest1=Project.objects.order_by('-timestamp')[0:3]
    context = {
        'object_list': featured,
        'latest': latest,
        'featured1':featured1,
        'latest1':latest1,
    }
    return render(request, 'index.html', context)

def signup(request):
    return render(request,'signup.html',{})

def register(request):
    if request.method == 'POST':
        request.session.pop('t', None)
        request.session.pop('userdata', None)
        userDataForm = UserDataForm(request.POST)
        if userDataForm.is_valid:
            request.session['userdata'] = request.POST
            secret_key = pyotp.random_base32()
            request.session['key'] = secret_key
            print(secret_key)
            totp = pyotp.TOTP(secret_key)
            yagmail_smtp_connection = yagmail.SMTP(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD,
                                                   host='smtp.gmail.com')
            yagmail_smtp_connection.send(request.POST.get('email'), 'OTP for InnoVza login', totp.now())
            return redirect('verifyotp')
    return redirect('signup')

def verifyotp(request):
    if request.method=='POST':
        otp = request.POST.get('otp')
        print(otp)
        verify_otp = request.session['key']
        totp1=pyotp.TOTP(verify_otp)
        print(totp1.now())
        data = request.session.get('userdata')
        if otp==totp1.now() :
            #print("Hello")
            print(data)
            userDataForm = UserDataForm(data)
            user=User.objects.create_user(data['username'],data['email'],data['password'])
            userDataForm.save()
            user.save()
            return redirect('signin')
        else:
            #message
            redirect('verifyotp')
    return render(request, "otp.html", {})

def signin(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('userpage')
    return render(request, 'login.html', {})

def userpage(request):
    user = UserInfo.objects.get(username=request.user)
    if user.profile_pic :
        post_num = Post.objects.filter(author=UserInfo.objects.get(username=request.user)).count()
        project_num = Project.objects.filter(author=UserInfo.objects.get(username=request.user)).count()
        return render(request, 'user.html', {'user': user, 'post_num': post_num, 'project_num': project_num, })
    else:
        return redirect('profile_photo')

def userBlog(request):
    post_list = Post.objects.filter(author=UserInfo.objects.get(username=request.user)).all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
    }
    return render(request,'userBlog.html',context)

def profile_photo(request):
    if request.method=='POST':
        try:
            user_info = UserInfo.objects.get(username=request.user.username)
            user_info.profile_pic = request.FILES['profile_pic']
            user_info.save()
            return redirect('userpage')
        except Exception as e:
            print(e)
    return render(request, 'profile_picture.html',{})

def post_info(request):
    return render(request,'postForm.html',{})


def post_update(request):
    if request.method=='POST':
        try:
            author=UserInfo.objects.get(username=request.user)
            title = request.POST['title']
            overview = request.POST['overview']
            categories = request.POST['category']
            categories=Category.objects.filter(title=categories)
            print(categories)
            thumbnail = request.FILES['thumbnail']
            content = request.POST['content']
            post_info=Post.objects.create(title=title,overview=overview,author=author,thumbnail=thumbnail,content=content)
            post_info.categories.set(categories)
            post_info.save()
        except Exception as e:
            print(e)
    return redirect('userpage')

def blog(request):
    category_count = get_category_count()
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'category_count': category_count,
        'most_recent': most_recent,
        'page_request_var': page_request_var
    }
    print(category_count)
    return render(request, 'blog.html', context)


def post(request,id):
    post=get_object_or_404(Post,id=id)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    category_count = get_category_count()
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=UserInfo.objects.get(username=request.user.username),post=post)
    form=CommentForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.instance.user=UserInfo.objects.get(username=request.user.username)
            form.instance.post=post
            form.save()
            return redirect(reverse('post-detail',kwargs={
                'id':post.id
            }))
    context={
        'form':form,
        'post':post,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request,'post.html',context)


def userProject(request):
    post_list = Project.objects.filter(author=UserInfo.objects.get(username=request.user)).all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
    }
    return render(request, 'userProject.html', context)

def project_info(request):
    return render(request,'projectForm.html',{})


def project_update(request):
    if request.method=='POST':
        try:
            author=UserInfo.objects.get(username=request.user)
            title = request.POST['title']
            overview = request.POST['overview']
            categories = request.POST['category']
            categories=Category.objects.filter(title=categories)
            requirement = request.POST['requirement']
            description= request.POST['description']
            code_file=request.FILES['code_file']
            project_video=request.FILES['project_video']
            project_info=Project.objects.create(title=title,
                                                overview=overview,author=author,
                                                requirement=requirement,description=description,
                                                code_file=code_file,project_video=project_video)
            project_info.categories.set(categories)
            project_info.save()
        except Exception as e:
            print(e)
    return redirect('userpage')

def get_category_count1():
    from django.db.models import Count
    queryset=Project\
        .objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))
    return queryset

def projectinfo(request):
    category_count = get_category_count1()
    project_list = Project.objects.all()
    paginator = Paginator(project_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    most_recent = Project.objects.order_by('-timestamp')[:3]
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'category_count': category_count,
        'most_recent': most_recent,
        'page_request_var': page_request_var
    }
    return render(request, 'projectInfo.html', context)

def project(request,id):
    project= get_object_or_404(Project, id=id)
    most_recent = Project.objects.order_by('-timestamp')[:3]
    category_count = get_category_count1()
    if request.user.is_authenticated :
        ProjectView.objects.get_or_create(user=UserInfo.objects.get(username=request.user.username), project=project)
    form = ProjectCommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = UserInfo.objects.get(username=request.user.username)
            form.instance.project = project
            form.save()
            return redirect(reverse('project-detail', kwargs={
                'id': project.id
            }))
    context = {
        'form':form,
        'project': project,
        'most_recent':most_recent,
        'category_count': category_count,
    }
    return render(request, 'project.html', context)

@login_required(login_url='/signin')
def logoff(request):
    logout(request)
    return redirect('index')

def accountdetail(request):
    user=UserInfo.objects.get(username=request.user.username)
    user1=User.objects.get(username=request.user)
    return render(request,'accountdetail.html',{'user':user,'user1':user1,})

