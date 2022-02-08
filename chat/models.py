from django.db import models
from users.models import User
from cakeManage.models import *

class chatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referred_store = models.ForeignKey(Store,on_delete=models.CASCADE, verbose_name="가게")
    
