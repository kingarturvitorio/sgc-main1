from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default='Nome genérico', max_length=200, null=True)
    title = models.CharField(default = 'Terapeuta', max_length=200, null=True)
    desc_text = 'Terapeuta com consultas'
    desc = models.CharField(default = desc_text, max_length=200, null=True)
    profile_img = models.ImageField(default = 'default-user.png', upload_to= 'images', null=True, blank = True)

    def __str__(self):
        return f"{self.user.username}'s profile"