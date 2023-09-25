from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,UserProfile
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    # if lets say user profile is deleted but still user exists and when we go and edit 
    # in the user part it will show error heche try-except block is put
    if created:
        UserProfile.objects.create(user=instance)
    else: 
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the userprofile if not exists
            UserProfile.objects.create(user=instance)
