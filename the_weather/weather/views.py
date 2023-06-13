import requests
from django.contrib import messages
from .models import City,Alert
from .constants import ALERT_NAME, CONDITIONS
from pynotifier import Notification
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CityForm,UserRegister,AlertForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def dash(request):
    
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=b023426aa015d2308a4073e60078ea43&units=metric'

    if request.method=="POST":
        form=CityForm(request.POST)        
        if form.is_valid():
            NCity=form.cleaned_data['name']            
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()                
                if res['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" Added Successfully...!!!")

                     # Create the associated Alert object for the newly added city
                    alert_form = AlertForm(request.POST)
                    if alert_form.is_valid():
                        threshold = alert_form.cleaned_data['threshold']
                        alert = alert_form.save(commit=False)
                        alert.city_names = NCity
                        alert.threshold = threshold
                        alert.save()
                else:
                    messages.error(request, "City Does Not Exist...!!!")
            else:
                messages.error(request, "City Already Exists...!!!")
            
    else:
        form = CityForm()
        alert_form = AlertForm()
        cities=City.objects.all()
        data=[]
        alerts = []
        for city in cities:    

            res=requests.get(url.format(city)).json()   
            city_weather={
                'city':city,
                'temperature' : res['main']['temp'],
                'description' : res['weather'][0]['description'],
                'country' : res['sys']['country'],
                'icon' : res['weather'][0]['icon'],
            }

            data.append(city_weather)
            

            
            alert = Alert.objects.create(city_names=city, threshold=0)
            if alert:

                if alert.alert_name == ALERT_NAME['TEMP_RISE']:
                    if alert.condition == CONDITIONS['GT']:
                        if alert.threshold > city_weather['temperature']:
                            messages.warning(request, f"Temperature in {city} has risen above {alert.threshold}°C.")
                            return render('/dash')
                    elif alert.condition == CONDITIONS['LT']:
                        if alert.threshold < city_weather['temperature']:
                            messages.warning(request, f"Temperature in {city} has risen below {alert.threshold}°C.")
                            return render('/dash')

                elif alert.alert_name == ALERT_NAME['RAINING']:
                    if alert.condition == CONDITIONS['EQ']:
                        if city_weather['description'] == 'rain':
                            messages.warning(request, f"It is raining in {city}.")
                            return render('/dash')
                        
                elif alert.alert_name == ALERT_NAME['THUNDERSTORM']:
                    if alert.threshold == city_weather['description']:
                        messages.warning(request, f"Thunderstorms and torrential downpours are expected in {city}.")
                
        context = {'data': data, 'form': form, 'alerts': alerts}  
        return render(request, "dash.html", context)


        



def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect('/dash')


def user_register(request):

    if request.method=="POST":
        regfmdata=UserRegister(request.POST)
        message={}
        if regfmdata.is_valid():
            regfmdata.save()
            message['msg']="Congratulation, Register Done Successfully. Please Login"
            message['x']=1
            return render(request, 'register_success.html', message)
    
        else:
            message['msg']="Failed to Register User. Please try Again"
            message['x']=0
            return render(request, 'register_success.html', message)
    
    else:
        
        regfm=UserRegister()
        content={}
        content['regfmdata']=regfm
        return render(request,'register.html',content)
    
def user_login(request):
    fmlog=AuthenticationForm()
    content={}
    content['logfmdata']=fmlog
    if request.method=="POST":
        logfmdata=AuthenticationForm(request=request,data=request.POST)
        if logfmdata.is_valid():
            uname=logfmdata.cleaned_data['username']
            upass=logfmdata.cleaned_data['password']
            r=authenticate(username=uname,password=upass)
            if r is not None:
                login(request,r)#start session and store id of logged in user
                return redirect('/dash')
        else:
            content['msg']="Invaild username and Password!!!"
            return render(request,'index.html',content)
    else:
        return render(request,'index.html',content)
    
def user_logout(request): #it destroy session or data stored in session

    logout(request)
    return redirect('/')

