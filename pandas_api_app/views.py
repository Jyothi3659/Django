from django.shortcuts import render
from .serializers import *
import os, glob, io, base64, urllib
# Create your views here.
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import matplotlib.pyplot as plt
import pandas as pd
from django.utils.decorators import method_decorator
from django.core.cache import cache
# from django.views.decorators.cache import cache_page
# from .forms import 
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from django.views import View
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .forms import *
from rest_framework.permissions import IsAuthenticated
import pdb

class CovidAPIView(APIView):
    permission_classes = (AllowAny,)
    # import ipdb; ipdb.set_trace()
    def get(self, request):
        covid = Covid.objects.all()
        serializer = CovidSerializer(covid, many = True)
        return Response(serializer.data)    

class HTMLView(APIView):
    def get(self, request):
        return render(request, 'login.html')



class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class TitanicJsonView(APIView):
    def titanicdata(self):
        titanic = Titanic.objects.all()
        serializer  = TitanicSerializer(titanic, many = True)
        # import ipdb; ipdb.set_trace()
        return serializer.data


class GoogleChartView(APIView):
    # @method_decorator(cache_page(60*60))
    # @cache_page(60*15)
    def get(self,request):
        # @cache_page(60*15)
        # import ipdb; ipdb.set_trace()
        # if cache.get('googlecharts'):
        #     return Response(cache.get('googlecharts'))
        pdb.set_trace()
        covid = Covid.objects.all() 
        titanic = Titanic.objects.all()
        covid_data_list = []
        titanic_data_list = []
        for covid_obj in covid:
            covid_data_list.append([covid_obj.country, covid_obj.confirmed,covid_obj.death,covid_obj.recovered])
        for titanic_obj in titanic:
            titanic_data_list.append([titanic_obj.survived, titanic_obj.pclass,titanic_obj.name,titanic_obj.sex,titanic_obj.age,titanic_obj.sibsp,titanic_obj.parch,titanic_obj.ticket,titanic_obj.fare,titanic_obj.cabin,titanic_obj.embarked]) 
        chart = {'result' : covid_data_list , 'titanic' : titanic_data_list}
        # import ipdb; ipdb.set_trace()
        # cache.set('googlechart',chart,60)
        # cache_chart = cache.set('googlechart',{'result' : covid_data_list , 'titanic' : titanic_data_list}, 60)
        return render(request, 'plot.html', {'result' : covid_data_list , 'titanic' : titanic_data_list})
        
class CovidView(APIView): 
    # @method_decorator(cache_page(60))
    def get(self, request):
        # import ipdb; ipdb.set_trace()
        # if 'covid' in cache:
        #     return render(request, 'index.html', cache.get('covid'))
        covid = Covid.objects.all()
        df = covid.to_dataframe()
        country = list(df['country'].unique())
        country.insert(0,'All countries')
        df.tail(20).plot()
        plotted_fig = plt.gcf()
        buf = io.BytesIO()
        plotted_fig.savefig(buf, format = 'png')
        buf.seek(0)
        img = buf.getvalue()
        string = base64.b64encode(img)
        img = urllib.parse.quote(string)
        return render(request , 'index.html' , {'country' : country, 'image' : img })
       
    def plot_data(self,file_url):
        # import ipdb; ipdb.set_trace()
        covid = Covid.objects.all()
        df = covid.to_dataframe()
        titanic = Titanic.objects.all()
        df_titanic = titanic.to_dataframe()
        img_list = []
        images = [] 
        fig_list = []
        query_file = open("pandas_api_app/pandas_plot_queries.txt",'r+')
        i=0
        for query in query_file:
            fig_list.append(plt.figure())
            pd.eval(str.strip(query))
            fig_list[i].savefig('static/abc_' + str(i) + '.png')
            i +=1
        
        for img in glob.glob('static/*.png'):
            img = open(img , 'rb')
            img_list.append(base64.b64encode(img.read()))
        
        for img in img_list:
            images.append(urllib.parse.quote(img))
        
        return images
    # @method_decorator(cache_page(60))
    def post(self, request):
        # import ipdb; ipdb.set_trace()
        file_path = os.path.abspath('train.csv')
        list_of_files = glob.glob('/'.join( file_path.split('/')[0:-1])+str('/media')+str('/*')) # * means all if need specific format then *.csv
        latest_file_url = list_of_files
        images =  self.plot_data(latest_file_url)
        data = request.data
        country = data.get('country')
        covid = Covid.objects.all()
        df = covid.to_dataframe()
        # import ipdb; ipdb.set_trace()
        # df.groupby('country')['confirmed', 'death', 'recovered'].sum().plot()
        df[df['country']== country].groupby('country')[['confirmed','death','recovered']].sum().plot.bar()
        countries = list(df['country'].unique())
        countries.insert(0,'All countries')
        plotted_fig = plt.gcf()
        buf = io.BytesIO()
        plotted_fig.savefig(buf, format = 'png')
        buf.seek(0)
        img = buf.getvalue()
        string = base64.b64encode(img)
        img = urllib.parse.quote(string)
        images.insert(0,img)
        return render(request , 'index.html' , {'plot' : images,'country' : countries })
        # return Response(serializer.data)

# def create_view(request): 
#     # dictionary for initial data with  
#     # field names as keys 
#     context ={} 
  
#     # add the dictionary during initialization 
#     form = TitanicForm(request.POST or None) 
#     if form.is_valid(): 
#         form.save() 
          
#     context['form']= form 
#     return render(request, "create_view.html", context) 

# def get(self, request, *args, **kwargs):

#     form = self.form_class(initial=self.initial)
#     return render(request, 'create_view.html', {'form': form})

# def post(self, request, *args, **kwargs):
#     form = self.form_class(request.POST)
#     if form.is_valid():
#         # <process form cleaned data>
#         return HttpResponseRedirect('/success/')

#     return render(request, 'create_view.html', {'form': form})
def create_view(request): 
    # dictionary for initial data with  
    # field names as keys 
    context ={} 
  
    # add the dictionary during initialization 
    form = TitanicForm(request.POST or None) 
    if form.is_valid(): 
        form.save() 
          
    context['form']= form 
    return render(request, "create_view.html", context) 

def titaniclist(request):
	titanic_obj = Titanic.objects.all()
	return render(request,'titanic.html',{'titanic_obj': titanic_obj})

def titanic_create(request):
    # import ipdb; ipdb.set_trace()
    titanic_obj = Titanic.objects.all()
    data = TitanicForm()
    
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        form = TitanicForm(request.POST)
        # raise NameError(form.__dict__)
        # raise NameError(form.is_valid())
        if form.is_valid():
            # import ipdb; ipdb.set_trace()
            titanic, created = Titanic.objects.get_or_create(
                survived = request.POST.get('survived'),
                pclass   = request.POST.get('pclass'),        
                name     = request.POST.get('name'), 
                sex      = request.POST.get('sex'),
                age      = request.POST.get('age'), 
                sibsp    = request.POST.get('sibsp'), 
                parch    = request.POST.get('parch'),
                ticket   = request.POST.get('ticket'),
                fare     = request.POST.get('fare'),
                cabin    = request.POST.get('cabin'),
                embarked = request.POST.get('embarked')
                )
            titanic.save()
            return HttpResponseRedirect('/titanic-list/')
            # return render(request, 'sample.html')
        else:
            form = TitanicForm()
            msg="Error while adding data"            
    return render(request,'create_view.html',locals())

def edittitanic(request,pk):
    # import ipdb; ipdb.set_trace()
    titanic_obj = Titanic.objects.get(id=pk)
    data = TitanicForm()
    if request.method == 'POST':
        form = TitanicForm(request.POST)
        if form.is_valid():
            # import ipdb; ipdb.set_trace() 
            titanic_obj.survived = request.POST.get('survived'),
            titanic_obj.pclass   = request.POST.get('pclass'),        
            titanic_obj.name     = request.POST.get('name'), 
            titanic_obj.sex      = request.POST.get('sex'),
            titanic_obj.age      = request.POST.get('age'), 
            titanic_obj.sibsp    = request.POST.get('sibsp'), 
            titanic_obj.parch    = request.POST.get('parch'),
            titanic_obj.ticket   = request.POST.get('ticket'),
            titanic_obj.fare     = request.POST.get('fare'),
            titanic_obj.cabin    = request.POST.get('cabin'),
            titanic_obj.embarked = request.POST.get('embarked')
            titanic_obj.save()
            return HttpResponseRedirect('/titanic-list/')
        else:
            form = TitanicForm({'survived':titanic_obj.survived,'pclass':titanic_obj.pclass,'name':titanic_obj.name,
            'sex':titanic_obj.sex,'age':titanic_obj.age,'sibsp':titanic_obj.sibsp,'parch':titanic_obj.parch,
            'ticket':titanic_obj.ticket,'fare':titanic_obj.fare,'cabin':titanic_obj.cabin,'embarked':titanic_obj.embarked})
            msg="Error while adding data"
    return render(request,'titanic-edit.html',locals())
