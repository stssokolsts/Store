from accounts.models import UserProfile

class UploadSocialAuthAvatar(object):
    def __init__(self, provider, info):
        self.provider = provider
        self.info = info
        self.image_url = None

    def vk_oauth(self):
        return self.info.get('user_photo')

    def twitter(self):
        image_url = self.info.get('profile_image_url')
        if not 'default_profile' in image_url:
            return image_url.replace('_normal', '_bigger')
        return None

    def google_oauth2(self):
        return self.info.get('picture')

    def yandex_oauth2(self):
        return self.info.get('userpic')

    def facebook(self):
        return 'http://graph.facebook.com/{0}/picture?type=large'.format(
            self.info.get('id'))

    def github(self):
        raise NotImplementedError('GitHub not implemented!')

    def process(self):
        """Find and fetch image_url, and save to user.avatar
        """
        social_backend = self.provider.name.replace('-', '_')
        image_url = getattr(self, social_backend)()
        print(image_url)
        if not image_url:
            return None

        image_content = urlopen(image_url)
        if self.provider.name == 'facebook' and 'image/gif' in str(image_content.info()):
            return None

        return image_content


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def upload_avatar1(request, *args, **kwargs):
    avatar_content = UploadSocialAuthAvatar(
        kwargs['backend'], kwargs['response']).process()


def get_name(request,user, social_user,*args, **kwargs):
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()
    try:
        first_name = kwargs['response']['first_name']
        last_name = kwargs['response']['last_name']
        name = first_name +" " + last_name
    except KeyError:
        name = kwargs['response']['login']
    if name:
        user.userprofile.name = name
        print(user.userprofile.name)
        user.userprofile.save()