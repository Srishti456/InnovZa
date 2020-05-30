from django.db import models
from tinymce import HTMLField
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# Create your models here.

class UserInfo(models.Model):
    full_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30,unique=True)
    phoneno=models.CharField(max_length=10)
    gender=models.CharField(max_length=1)
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return self.username

class PostView(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #comment_count=models.IntegerField(default=0)
    #view_count=models.IntegerField(default=0)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)
    content = HTMLField()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

class ProjectView(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class ProjectComment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    project = models.ForeignKey('Project', related_name='pro_comments', on_delete=models.CASCADE)


class Project(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    requirement=HTMLField()
    description=models.TextField()
    code_file=models.FileField(upload_to='code/')
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    project_video = models.FileField(upload_to='videos/')
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={
            'id': self.id
        })

    @property
    def get_comment(self):
        return self.pro_comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return ProjectComment.objects.filter(project=self).count()

    @property
    def view_count(self):
        return ProjectView.objects.filter(project=self).count()



class Contact_Us(models.Model):
    name=models.CharField(max_length=32)
    email=models.EmailField()
    message=models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)