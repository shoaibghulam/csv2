from django.shortcuts import render , HttpResponse , redirect
from django.views import View
import operator
from functools import reduce
from django.contrib import messages
import json
from .models import *
import pandas as pd
import numpy as np
from django.db.models import Q
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Sum 



import os 


# Create your views here.
class Login(View):
    def get(self,request):
        if request.session.has_key('user'):
            return redirect('/')
        return render(request,'login.html')
    def post(self, request):
        try:
            email = request.POST['email']
            password = request.POST['pass']
            data=Users.objects.get(email=email ,password=password)
            if data:
                request.session['user']=data.pk
                return redirect('/')
        except:
            messages.error(request,"Please Enter Correct email and Password")
            return redirect('login')
class homePage(View):
    def get(self, request):
        try:
            if request.session.has_key('user'):
                    user=Users.objects.get(uId=request.session['user'])
            else:
                return redirect('login')
            cat=category.objects.filter(~Q(pk=1))
            data=items.objects.filter(uid=request.session['user'])
            dataSet={
                'data':data,
                'cat':cat
            }
            return render(request,'dashboard.html',dataSet)
        except:
            return redirect('logout')

class itemsView(View):
    def get(self, request):
        if request.session.has_key('user'):
                user=Users.objects.get(uId=request.session['user'])
        else:
            return redirect('login')
        data=items.objects.filter(uid=request.session['user'])
        dataSet={
            'data':data
        }
        return render(request,'items.html',dataSet)
    
    
class csvUpload(View):
    def get(self, request):
        if request.session.has_key('user'):
            user=Users.objects.get(uId=request.session['user'])
        else:
            return redirect('login')

        return render(request,'upload.html')
    def post(self , request):
        if request.session.has_key('user'):
            user=Users.objects.get(uId=request.session['user'])
        else:
            return redirect('login')
        
        try:
        #     # data managing through users?
        
            itemsTemp.objects.filter(uid=request.session['user']).delete()
        

            userfile=request.FILES['csvfile']
            y=str(userfile)
            ext = os.path.splitext(y) 
            
        
        
            data = pd.read_csv(userfile)
           

        
            Datecsv=pd.to_datetime(data['Date'])
            Descriptioncsv=data['Description'].tolist()
            Dbacsv=data['Doing Business As'].tolist()
            Amountcsv=data['Amount'].tolist()
            Sacsv=data['Street Address'].tolist()
            Cszcsv=data['City, State Zip'].tolist()
        
        
            for db,date,ds,amount,addres,city in zip(Dbacsv,Datecsv,Descriptioncsv,Amountcsv,Sacsv,Cszcsv):
                try:
                    fkey=subCategory.objects.filter(SName__icontains=db)[0]
                    amt=str(amount)
                    # data=items(Date=date,Amount=amt.replace(',', ''),Description=ds,DoingBusinessAs=db,StreetAddress=addres,City=city, uid=Users.objects.get(uId=request.session['user']),subcatid=fkey)
                    dataTemp=itemsTemp(Date=date,Amount=amt.replace(',', ''),Description=ds,DoingBusinessAs=db,StreetAddress=addres,City=city , uid=Users.objects.get(uId=request.session['user']),subcatid=fkey)
                    dataTemp.save()
                    # data.save()
                except:
                    amt=str(amount)
                    # data=items(Date=date,Amount=amt.replace(',', ''),Description=ds,DoingBusinessAs=db,StreetAddress=addres,City=city, uid=Users.objects.get(uId=request.session['user']))
                    dataTemp=itemsTemp(Date=date,Amount=amt.replace(',', ''),Description=ds,DoingBusinessAs=db,StreetAddress=addres,City=city , uid=Users.objects.get(uId=request.session['user']))
                    dataTemp.save()
                    # data.save()
                
            subcat=subCategory.objects.all()
            ids=list()
           
            
            
            for x in subcat:
                ids.append(x.SName)
            if not ids:
                ids.append("notset")
            
            querylist=list()
            data=itemsTemp.objects.filter(reduce(operator.or_, (~Q(DoingBusinessAs__contains=x) for x in ids)), uid=request.session['user'])
            
            for x in data:
                querylist.append(x.DoingBusinessAs)

            
            l3 = [x for x in querylist if x not in ids]
            cleanData = list(dict.fromkeys(l3))

            dataSet={
                'newdata':cleanData,
                'cat':category.objects.filter(~Q(pk=1))

            }
            
            if not cleanData:
                # messages.success(request,'Data has been Inserted')
                return redirect('datasaver')

            return render(request,'categories.html',dataSet)
        except:
            messages.error(request,'this File System is Not matching')
                
            return redirect('Homepage')    

def datasaver(request):
    # baloch
    setdata=itemsTemp.objects.filter(uid=request.session['user'])
    print(setdata)
    
    if setdata:
        for xd in setdata:
            print("done done")
            itemdata=items(Date=xd.Date,Amount=xd.Amount,Description=xd.Description,DoingBusinessAs=xd.DoingBusinessAs,StreetAddress=xd.StreetAddress,City=xd.City, uid=xd.uid,subcatid=xd.subcatid)
            itemdata.save()
    messages.success(request,'Data has been Inserted')
    return redirect('Homepage')
       

# Sub Category View
class subCategoryView(View):
    def get(self,request):
        if request.session.has_key('user'):
            user=Users.objects.get(uId=request.session['user'])
        else:
            return redirect('login')
        dataSet={
            'data':subCategory.objects.filter(~Q(pk=1)).order_by('SName'),
            'cat':category.objects.filter(~Q(pk=1)).order_by('catName')
        }
        return render(request,'subcategorydata.html',dataSet)
    def post(self, request):
        if request.session.has_key('user'):
            user=Users.objects.get(uId=request.session['user'])
        else:
            return redirect('login')
        useranwser=dict()
        sigledata=int(request.POST['datalength'])
        for x in range(1,int(request.POST['datalength'])+1):
            data=subCategory(SName=request.POST['item'+str(x)],catid=category.objects.get(catid=request.POST['category'+str(x)]))
            data.save()
            setdata=itemsTemp.objects.filter(DoingBusinessAs=data.SName,subcatid=1,uid=request.session['user'])
            if setdata:
                for xd in setdata:            
                    xd.subcatid=data
                    xd.save()
        

        finaldata=itemsTemp.objects.filter(uid=request.session['user'])   
        if finaldata:
            for xd in finaldata:
                itemdata=items(Date=xd.Date,Amount=xd.Amount,Description=xd.Description,DoingBusinessAs=xd.DoingBusinessAs,StreetAddress=xd.StreetAddress,City=xd.City, uid=xd.uid,subcatid=xd.subcatid)
                itemdata.save()
                
            # baloch
                    
       
        messages.success(request,'Sub Category has been Inserted')
        return redirect('insertsubcat')


def insertsubcatdata(request):
    if request.method == "POST":
        cat=request.POST['cat']
        sname=request.POST['sname']
        data=subCategory(SName=sname,catid=category.objects.get(catid=cat,uid=request.session['user']))
        data.save()
        messages.success(request,'Sub Category has been Inserted')
        return redirect('/insertsubcat')
    else:
         return redirect('/insertsubcat')



class subCatUpdate(View):  
    
    def post(self , request):
        if not request.session.has_key('user'):
           return redirect('login')

        sid=request.POST['uid']
        cat=request.POST['cat']
        sname=request.POST['sname']
        data=subCategory.objects.get(sid=sid)
        data.SName=sname
        data.catid=category.objects.get(catid=cat)
        data.save()
        messages.success(request,'Sub Category has been Updated')
        return redirect('/insertsubcat')
    def get(self, request):
        if not request.session.has_key('user'):
               return redirect('login')

        sid=request.GET.get('id')
        data=subCategory.objects.get(sid=sid)
        serdata=serSubCat(data , many=False)
        return HttpResponse(json.dumps(serdata.data))
       
def subcatdelete(request,id):
    data=subCategory.objects.get(sid=id)
    data.delete()
    messages.success(request,'Sub Category has been Deleted')
    return redirect('/insertsubcat')

def categorydelete(request,id):
    data=category.objects.get(catid=id)
    data.delete()
    messages.success(request,'Category has been Deleted')
    return redirect('/category')


# main category
class categoryView(View):
    def get(self,request):
        if not request.session.has_key('user'):
             return redirect('login')
           
        dataSet={
            'cat':category.objects.filter(~Q(pk=1)).order_by('catName')
        }
        return render(request,'categorydata.html',dataSet)


class categoryUpdate(View):
    def get(self,request):
        if not request.session.has_key('user'):
               return redirect('login')

        sid=request.GET['id']
        data=category.objects.get(catid=sid)
        serdata=serCat(data , many=False)
        return HttpResponse(json.dumps(serdata.data))
    
    def post(self,request):
        if not request.session.has_key('user'):
               return redirect('login')
        id=request.POST['uid']
        data=category.objects.get(catid=id)
        data.catName= request.POST['sname']
        data.save()
        messages.success(request,'Category has been Updated')
        return redirect('category')
    



class addCategory(View):
    def post(self, request):
        if not request.session.has_key('user'):
               return redirect('login')
        sname=request.POST.get('sname')
        data=category(catName=sname)
        data.save()
        messages.success(request,'Category has been Added')
        return redirect('category')


class setting(View):
    def get(self,request):
        if not request.session.has_key('user'):
               return redirect('login')

        data=Users.objects.get(uId=request.session['user'])
        return render(request,'setting.html',{'data':data})
    def post(self,request):
        if not request.session.has_key('user'):
               return redirect('login')
        data=Users.objects.get(uId=request.session['user'])
        data.firstName= request.POST['fname']
        data.lastName= request.POST['lname']
        data.email= request.POST['email']
        data.contactNo= request.POST['contact']
        data.password= request.POST['password']
        data.save()
        messages.success(request, "User Data has been Updated")
        return redirect('setting')


class chartView(View):
    def get(self,request):
        year=request.GET.get('year',2020)
        print("My year ",year)
        mydata=list()
        data=items.objects.annotate(month=TruncMonth('Date')).filter(Date__year=year,uid=request.session['user']).values('month').annotate(total_income=Sum('Amount')).order_by('Date__month').order_by()
        for x in data:
            mydata.append({
                'date':str(x['month']),
                'amount':round(x['total_income'],2)
            })  
       
       
      
        return HttpResponse(json.dumps(mydata))

def logout(request):
     if request.session.has_key('user'):
         del request.session['user']
         return redirect('login')


class HomeData(View):
    def get(self,request):
        smonth=datetime.now().month
        syear=datetime.now().year
        month=request.GET['month']
        year=request.GET['year']
        cats=request.GET['cat']
       
        mydata=list()
        query=list()
        data=None
        cat=subCategory.objects.filter()
        for d in cat:
            query.append(d.SName)
        if month=='a' and year=='a' and cats=='b':
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=2020,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=2020,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
        elif month=='a' and not year=='a' and cats=='b':
            # select year for all months data calculate
            # data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=year,uid=request.session['user']).values('DoingBusinessAs','Date','subcatid.catid').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
            y=items.objects.filter(Date__year=year,uid=request.session['user']).values_list('Date__year', 'Date__month').annotate(Sum('Amount'))
            data=items.objects.filter(Date__year=year,uid=request.session['user']).values_list('Date__year', 'Date__month','subcatid__catid__catName').annotate(total_sales=Sum('Amount')).order_by('Date__month')
            print(data)
           
            for x in data:
                mydata.append({
                        'mydata':x,
                        # 'amount':round(x['total_sales'],2),
                        # 'date':str(x['Date'])
                    })  
           
            for z in y:
                mydata.append({
                       
                        'z':z,
                       
                    })  
        
           
           
            
            return HttpResponse(json.dumps(mydata))
            # end yearly query
        elif not month=='a' and not year=='a' and cats=='b':
            print("join ge")
           
           
            
            # return HttpResponse(json.dumps(mydata))
            y=items.objects.filter(Date__year=year,Date__month=month,uid=request.session['user']).values_list('Date__year','Date__day', 'Date__month').annotate(Sum('Amount'))
            data=items.objects.filter(Date__year=year,Date__month=month,uid=request.session['user']).values_list('Date__year', 'Date__month','Date__day','subcatid__catid__catName').annotate(total_sales=Sum('Amount')).order_by('subcatid__catid__catName')
           
           
            for x in data:
                mydata.append({
                        'mydata':x,
                        # 'amount':round(x['total_sales'],2),
                        # 'date':str(x['Date'])
                    })  
           
            for z in y:
                mydata.append({
                       
                        'z':z,
                       
                    })  
        
           
           
            
            return HttpResponse(json.dumps(mydata))
        elif not month=='a' and year=='a' and cats=='b':
            print("waa day 2")
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__month=month,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
           
        elif not cats=='a' and month=='a' and year=='a':
          
            cats=subCategory.objects.filter(catid=cats)
            catlist=list()
            for x in cats:
                catlist.append(x.SName)
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
        elif not cats=='b' and not month=='a' and not year=='a':
            print("waa")
            cat=subCategory.objects.filter(catid=cats)
            catlist=list()
            for x in cat:
                catlist.append(x.SName)
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,Date__month=month,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
            
        elif not cats=='b' and month=='a' and not year=='a':
            
            catss=subCategory.objects.filter(catid=cats)
            catlist=list()
            for x in catss:
                catlist.append(x.SName)
            data=items.objects.filter(Date__year=year,uid=request.session['user']).values_list('DoingBusinessAs','Date__day','Date__month','Date__year').annotate(Sum('Amount')).order_by('Date__month','Date__day')
            # data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('Date__month','Date__day')
            y=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,uid=request.session['user']).values_list('Date__month','Date__year').annotate(total_sales=Sum('Amount')).order_by('Date__month')
            # y=items.objects.filter(subcatid__uid=cats,Date__year=year,uid=request.session['user']).values_list('Date__month','Date__year').annotate(Sum('Amount')).order_by('Date__month','Date__day')
            mydata= list()
            # mydata.append(data)
            # print(data)
            for x in data:
                mydata.append({
                        'mydata':x,
                        # 'amount':round(x['total_sales'],2),
                        # 'date':str(x['Date'])
                    })  
           
            for z in y:
                mydata.append({
                       
                        'z':z,
                       
                    })  
            return HttpResponse(json.dumps(mydata))
           
        elif not cats=='b' and not month=='a' and year=='a':
            
            cats=subCategory.objects.filter(catid=cats)
            catlist=list()
            for x in cats:
                catlist.append(x.SName)
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__month=month,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
            
        elif not month =='a':
             data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=year,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
        elif not year=='a':
             data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__month=month,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
        

            # data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,Date__month=month).values('DoingBusinessAs').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
     
            
        else:
             data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=year,Date__month=month,uid=request.session['user']).values('DoingBusinessAs','Date').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
        for x in data:
           mydata.append({
                'Sub':str(x['DoingBusinessAs']),
                'amount':round(x['total_sales'],2),
                'date':str(x['Date'])
            })  
        
        # print(mydata)

        return HttpResponse(json.dumps(mydata))


#  refund data start
class refundData(View):
    def get(self,request):
        smonth=datetime.now().month
        syear=datetime.now().year
        month=request.GET['month']
        year=request.GET['year']
        cats=request.GET['cat']
       
        mydata=list()
        query=list()
        data=None
        cat=subCategory.objects.all()
        for d in cat:
            query.append(d.SName)
        if month=='a' and year=='a' and cats=='b':
            print("1")
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=2020,Amount__lte=0,uid=request.session['user']).order_by('DoingBusinessAs')
        elif not cats=='b' and month=='a' and year=='a':
          
            catey=subCategory.objects.filter(catid=cats)
            print("catey")
            catlist=list()
            for x in catey:
                catlist.append(x.SName)
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Amount__lte=0,uid=request.session['user']).values('DoingBusinessAs','Amount','Date').order_by('Date__year')
            mydata=list()
            for x in data:
               mydata.append({
                'DoingBusinessAs':str(x['DoingBusinessAs']),
                'Amount':round(x['Amount'],2),
                'Date':str(x['Date'])
            })
            return HttpResponse(json.dumps(mydata))  
        elif not cats=='b' and month=='a' and not year=='a':
             
            catey=subCategory.objects.filter(catid=cats)
            catlist=list()
            print("hello done")
            for x in catey:
                catlist.append(x.SName)
            # print(catlist)
            # data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Amount__lte=0,Date__year=year,uid=request.session['user'],subcatid=cats).values('DoingBusinessAs','Amount','Date')
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,Amount__lte=0,uid=request.session['user']).values('DoingBusinessAs','Amount','Date').order_by('Date__month','Date__day')
           
            mydata=list()
            for x in data:
               mydata.append({
                'DoingBusinessAs':str(x['DoingBusinessAs']),
                'Amount':round(x['Amount'],2),
                'Date':str(x['Date'])
            })
            # mydata.sort()
            return HttpResponse(json.dumps(mydata))  
            
        elif not cats=='b' and not month=='a' and  year=='a':
          
            catey=subCategory.objects.filter(catid=cats)
            catlist=list()
            for x in catey:
                catlist.append(x.SName)
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Amount__lte=0,Date__month=month,uid=request.session['user']).values('DoingBusinessAs','Amount').order_by('DoingBusinessAs')
            mydata=list()
            for x in data:
               mydata.append({
                'DoingBusinessAs':str(x['DoingBusinessAs']),
                'Amount':round(x['Amount'],2)
            })
            print("don")
            return HttpResponse(json.dumps(mydata))  
        elif not month=='a' and not year=='a' and cats=='b':
            print("hi bro")
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=year,Date__month=month,Amount__lte=0,uid=request.session['user']).order_by('DoingBusinessAs')
        elif not cats=='b' and not month=='a' and not year=='a':
            print("this is my wrldworld")
            cats=subCategory.objects.filter(catid=cats)
            catlist=list()
            for x in cats:
                catlist.append(x.SName)
            data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,Date__month=month,Amount__lte=0,uid=request.session['user']).order_by('DoingBusinessAs')
            
        elif not month =='a':
             print("new done") 
             data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__month=month,Amount__lte=0,uid=request.session['user']).order_by('DoingBusinessAs')
             
        elif not year=='a':
             print("done d")
             data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=year,Amount__lte=0,uid=request.session['user']).order_by('DoingBusinessAs')
        
        

            # data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in catlist)),Date__year=year,Date__month=month).values('DoingBusinessAs').annotate(total_sales=Sum('Amount')).order_by('DoingBusinessAs')
     
            
        else:
             print("jost do")
             data=items.objects.filter(reduce(operator.or_, (Q(DoingBusinessAs__contains=x) for x in query)),Date__year=year,Date__month=month,Amount__lte=0,uid=request.session['user']).order_by('DoingBusinessAs')
       
        
        
        serdata= serItems(data , many=True)
      
          

        return HttpResponse(json.dumps(serdata.data))

#  refund data end

def additem(request):
    if request.method == "POST":
        itemname=request.POST['itemname']
        itemdesc=request.POST['itemdesc']
        itemDoingBusinessAs=request.POST['itemDoingBusinessAs']
        StreetAddress=request.POST['StreetAddress']
        city=request.POST['city']
        amount=request.POST['amount']
        date=request.POST['date']
        try:
            subcat=subcategory.objects.get(SName=itemDoingBusinessAs)
        except:
            subcat=subcategory.objects.get(sid=i)
        data=items(Date=date,Amount=amount,Description=itemdesc,DoingBusinessAs=itemDoingBusinessAs,StreetAddress=StreetAddress,City=city,uid=Users.objects.get(uid=request.session['user']),subcatid=subcat)
        data.save()
        messages.success(request,"Data has been Inserted")
        return redirect('/items')

def itemdelete(request,id):  
    data=items.objects.get(id=id)
    data.delete()    
    messages.success(request,"Data has been Deleted")
    return redirect('/items')


# delete all category
@csrf_exempt
def deleteallcat(request):
    x= request.POST.getlist('ids[]')
    print(x)
    for x in x:
        deldata=category.objects.get(pk=x)
        deldata.delete()
    messages.success(request,"Selected Category has been Deleted")
    return HttpResponse("check")
@csrf_exempt
def deleteallsubcat(request):
    x= request.POST.getlist('ids[]')
    print(x)
    for x in x:
        deldata=subCategory.objects.get(pk=x)
        deldata.delete()
    messages.success(request,"Selected Sub Category has been Deleted")
    return HttpResponse("check")

@csrf_exempt
def deleteallitem(request):
    x= request.POST.getlist('ids[]')
    print(x)
    for x in x:
        deldata=items.objects.get(pk=x)
        deldata.delete()
    messages.success(request,"Selected Item has been Deleted")
    return HttpResponse("check")