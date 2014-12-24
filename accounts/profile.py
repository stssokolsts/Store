from models import UserProfile
from forms import UserProfileForm
from django.shortcuts import HttpResponseRedirect


def retrieve(request):
    """ gets the UserProfile instance for a user, creates one if it does not exist """
    try:
        #profile = UserProfile.objects.get(id=request.user.id)
        profile = request.user.userprofile #????
        print("exist")
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    return profile


def set(request):
    """ updates the information stored in the user's profile """
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()


try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
