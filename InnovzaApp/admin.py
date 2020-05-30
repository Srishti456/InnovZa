from .models import UserInfo,Post,Category,Project,Comment,PostView,Contact_Us
from django.contrib import admin
# Register your models here.

admin.site.register([UserInfo,Post,Category,Project,Comment,PostView,Contact_Us])
