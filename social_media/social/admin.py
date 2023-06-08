from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Post, ChatMessage
# Register your models here.



# Unregister Groups
admin.site.unregister(Group)


#Mix Profiles into User Info
class ProfileInline(admin.StackedInline):
    model = Profile


#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model =  User
    fields = ["username"]
    inlines = [ProfileInline]

#Unregister initial User
admin.site.unregister(User)

#Reregister initial User
admin.site.register(User, UserAdmin)


# Register Post
admin.site.register(Post)


# Register Chatroom
admin.site.register(ChatMessage)
