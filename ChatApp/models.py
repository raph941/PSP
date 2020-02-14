from django.db import models
from django.db import models
from accounts.models import User, UserProfile

# Create your models here.
class Messanger(models.Model):
    message = models.CharField(max_length=50)
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='msg_sender')
    reciever = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='msg_reciever')    
    read_status = models.BooleanField(default=False)
    send_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'by : { self.sender }'

    class Meta:
        ordering = ['-send_date']