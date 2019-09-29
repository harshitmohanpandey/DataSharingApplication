from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3,os,json
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from .s3functions import *
import datetime,re,smtplib 
from .models import UserDetails,send_recieve_details
from awspolicy import BucketPolicy
# Create your views here.
s3=connect()

def rgister(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        email = request.POST['email']
        password = request.POST['password']
        bucketname=str(datetime.datetime.now())
        bucketname=re.sub('[^A-Za-z0-9]+', '', bucketname)
        bucketname=bucketname+firstname.lower()        
        create_bucket(s3,bucketname)
        set_bucket_policy(bucketname)
        user_data=UserDetails()
        user_data.name=firstname
        user_data.email=email
        user_data.password=password
        user_data.awsbucketname=bucketname
        user_data.save()
        return render(request,'image_upload/login.html')
    else: 
        return render(request,'image_upload/register.html')

def logout(request):
    if 'username' in request.session:
        del request.session["username"]
    return render(request,'image_upload/login.html')

def login(request):
    try:
        print(settings.TEMPLATE_DIR)
        if request.method == 'POST':
            username = request.POST['inputEmail']
            password = request.POST['inputPassword']
            userdetails=UserDetails.objects.filter(email=username,password=password)
            if userdetails.exists():
                request.session["username"] = username                
                return HttpResponseRedirect(reverse('image_upload:index'))     
            else:
                 return render(request,'image_upload/login.html')
                           
        else:
            return render(request,'image_upload/login.html')
    except Exception as ex:
        print("error at login",ex)

def index(request):    
    try:
        if 'username' in request.session:  
            userdata=UserDetails.objects.filter(email=request.session['username'])
            awsbucketname=userdata.values('awsbucketname')[0]['awsbucketname']
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                # path=r'images\\'+myfile.name
                path=os.path.join("images", myfile.name)
                filename = fs.save(path, myfile)
                filename=upload_intobucket(filename, awsbucketname, myfile.name,s3)
                bucket_items=get_itemsin_bucket(awsbucketname,s3)
                allusers=UserDetails.objects.exclude(email='')
                allusers_email=[]
                for item in allusers:
                    allusers_email.append(item.email)

                count=1
                list_buckt_itm_with_id=[]
                for item in bucket_items:
                    bucket_items_with_id={}
                    bucket_items_with_id={'id':count,'file':item}
                    list_buckt_itm_with_id.append(bucket_items_with_id)
                    count=count+1 

                context = {
                    'bucket_name':awsbucketname,
                    'bucket_items':list_buckt_itm_with_id,
                    'success_upload':True,
                    'username':request.session["username"],
                    'filename':filename,
                    'allusers_email':allusers_email 
                }
                return render(request,'image_upload/index.html',context)
            else:
                allusers=UserDetails.objects.exclude(email='')
                allusers_email=[]
                for item in allusers:
                    allusers_email.append(item.email)              
                
                bucket_items=get_itemsin_bucket(awsbucketname,s3)
                count=1
                list_buckt_itm_with_id=[]
                for item in bucket_items:
                    bucket_items_with_id={}
                    bucket_items_with_id={'id':count,'file':item}
                    list_buckt_itm_with_id.append(bucket_items_with_id)
                    count=count+1                
                context = {
                    'bucket_name':awsbucketname,
                    'bucket_items':list_buckt_itm_with_id,
                    'username':request.session["username"],
                    'success_upload':False   ,
                    'allusers_email':allusers_email 
                }
                return render(request,'image_upload/index.html',context)
        else:
            return render(request,'image_upload/login.html')
    except Exception as ex:
        print("error at index",ex)

class send_to_user(View):
    def post(self, request):
        if 'username' in request.session:
           to_username=request.POST['to_username']
           link=request.POST['link']
           from_user=request.session['username']
           send_recieve_details_obj=send_recieve_details()
           send_recieve_details_obj.from_user=from_user
           send_recieve_details_obj.to_user=to_username
           send_recieve_details_obj.link_to_download=link
           send_recieve_details_obj.file_name=link.split('/')[len(link.split('/'))-1]
           send_recieve_details_obj.date=str(datetime.datetime.now().date())
           send_recieve_details_obj.save()
        #    send_email(to_username,from_user)

class delete_from_aws(View):
    def post(self, request):
        if 'username' in request.session:
           link=request.POST['link']
           leng=len(link.split(r'/'))
           filename_to_delete= link.split(r'/')[leng-1] 
           bucketname= link.split(r'/')[leng-2]      
           print(filename_to_delete) 
           print(bucketname)
           s3.Object(bucketname, filename_to_delete).delete()


def download(request):
    if 'username' in request.session:
        received_data=send_recieve_details.objects.filter(to_user=request.session["username"] )
        # if alluser.exists():

        context = {                    
                    'username':request.session["username"],
                    'received_data':received_data            
                }
        return render(request,'image_upload/download.html',context)
    else:
        return render(request,'image_upload/login.html')


def send_email(TO,fromm):
    print(TO)
    print(fromm)
    gmail_user = "XXXX"
    gmail_pwd = "XXXX"
    TEXT = "Testing sending mail using gmail servers"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    SUBJECT="AWS File sharing system"
    BODY = 'Greetings from data sharing application,'+fromm+' has shared data with you.please login to your account to download the same'
    message ='Subject: {}\n\n{}'.format(SUBJECT, BODY)
    server.sendmail(gmail_user, [TO], message)
    print ('email sent')


if __name__ == "__main__": 
    print('')
    # send_email()
