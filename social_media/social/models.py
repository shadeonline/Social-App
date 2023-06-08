from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        User, 
        related_name="posts",
        on_delete=models.DO_NOTHING
    )
    description = models.CharField(max_length=256, db_index=True)
    image = models.FileField(blank=False)
    thumbnail = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}) : "
            f"{self.description}"
            )
    


#Create a user profile model
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", 
                                     related_name="followed_by", 
                                     symmetrical=False, 
                                     blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    intro = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username
    

#Create profile when new user signs up
@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #have the user folow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
        

# Chat Message
class ChatMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']