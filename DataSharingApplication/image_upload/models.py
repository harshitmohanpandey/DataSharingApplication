from django.db import models

# Create your models here.
class UserDetails(models.Model):
    # user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255,blank=False)
    password = models.CharField(max_length=255, blank=False)
    awsbucketname= models.CharField(max_length=255, blank=False)

class send_recieve_details(models.Model):
    from_user = models.CharField(blank=False,max_length=255)
    to_user = models.CharField(blank=False,max_length=255)
    file_name = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=None, blank=True, null=True)
    link_to_download=models.CharField(max_length=255, blank=True)

# class upload_details(models.Model):
#     from_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)    
#     file_name = models.CharField(max_length=255, blank=True)
#     date = models.DateField(default=None, blank=True, null=True)