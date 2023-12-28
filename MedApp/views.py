from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from .models import Tests, User,Beneficiary,DiagnosticCentre,TestsOffered,SlotBookAndReport,DoctorConsult,Doctor
from django.http import HttpResponse
from math import radians, cos, sin, asin, sqrt
from datetime import date
import sys
import tensorflow as tf
from tensorflow import keras,Graph
import numpy as np
from tensorflow.keras.preprocessing import image
model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model=keras.models.load_model('./models/resnetmodel_600.h5')
# Create your views here.
def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)
def index(request):
    return render(request,'index.html')
def register(request):
    if request.method == 'POST':
        name=request.POST['name']
        try:
            email=request.POST['emailid']
            phonenum=request.POST['phonenum']
            password=request.POST['password']
            longitude=83.42186520555933
            latitude=17.929349824525914
            user=User(email=email,name=name,phone=phonenum,password=password,latitude=float(latitude),longitude=float(longitude))
            user.save()
            return render(request,'user_reg_success.html')
        except Exception as e:
            return HttpResponse("Error Occured... May be you are using the same mail'id or phone Number. PLease Login if you have an account")
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        passw=request.POST['passw']
        res=User.objects.filter(email=email,password=passw)
        if(len(res)==1):
            request.session['user_email']=res[0].email
            request.session['userid']=res[0].UserId
            return redirect('dashboard')
        return HttpResponse("Login success ")
def dashboard(request):
    print(request.session.has_key('user_email'))
    if request.session.has_key('user_email'):
        date1=date.today()
        res=User.objects.filter(email=request.session['user_email'])
        res1=Beneficiary.objects.filter(UserId=request.session['userid'])
        testbookings=[]
        upcoming=[]
        doctor=[]
        for i in res1:
            data=SlotBookAndReport.objects.filter(BeneId=i)
            for j in data:
                if j.report:
                    print(j)
                    testbookings.append(j)
                    try:
                        tem=DoctorConsult.objects.get(slotId=j.SlotId)
                        doctor.append(tem)
                        print(tem)
                    except:
                        pass
                else:
                    upcoming.append(j)

        context={
            "res":res[0],
            "res1":res1,
            "tests":testbookings,
            "upcoming":upcoming,
            "doctor":doctor,
        }
        return render(request,'dashboard.html',context)
    else:
        return redirect('./')
def addBene(request):
    if request.method=="POST":
        name=request.POST['name']
        reltouser=request.POST['reltouser']
        age=request.POST['age']
        gender=request.POST['Gender']
        res=User.objects.filter(email=request.session['user_email'])
        UserId=res[0]
        bene=Beneficiary(name=name,RelToUser=reltouser,Age=age,Gender=gender,UserId=UserId)
        bene.save()
        return redirect('./dashboard')
def logout(request):
    request.session.flush()
    return redirect('./')
def DiagnosticCenter(request):
    if request.method=="POST":
        email=request.POST['email']
        passw=request.POST['passw']
        res=DiagnosticCentre.objects.filter(email=email,password=passw)
        if len(res)==1:
            request.session['Dc_email']=res[0].email
            request.session['Dc_id']=res[0].CentreId
            return redirect('DiagnosticCenterDashboard')
        else:
            return render(request,'diagnosticCenter.html')
    else:
        return render(request,'diagnosticCenter.html')
def DiagnosticCenterDashboard(request):
    if request.session.has_key('Dc_id'):
        res=DiagnosticCentre.objects.filter(email=request.session['Dc_email'])
        res1=TestsOffered.objects.filter(CentreId=request.session['Dc_id'])
        test=Tests.objects.all()
        patientlist=[]
        for i in res1:
            patientlist1=SlotBookAndReport.objects.filter(TestId=i,DateOfTest=date.today())
            print(patientlist1)
            for i in patientlist1:
                if i.report:
                    continue
                else:
                    patientlist.append(i)
            print(patientlist)
        context={
            'res':res[0],
            'res1':res1,
            'tests':test,
            'patientlist':patientlist,
        }
        return render(request,'DiagnosticCenterDashboard.html',context)
    else:
        return redirect(request,'DiagnosticCenter')
def addTests(request):
    if request.method=="POST":
        TestId=request.POST['Test']
        price=request.POST['Price']
        testsPerday=request.POST['testsPerDay']
        res=DiagnosticCentre.objects.filter(email=request.session['Dc_email'])
        test1=Tests.objects.filter(TestId=TestId)
        try:
            testOff=TestsOffered(CentreId=res[0],TestId=test1[0],Price=price,TestsPerDay=testsPerday)
            testOff.save()
        except:
            pass
        return redirect('./DiagnosticCenterDashboard')
def Dclogout(request):
    request.session.flush()
    return redirect('./DiagnosticCenter')
def TestBook(request):
    if request.session.has_key('user_email'):
        if request.method=='POST':
            date=request.POST['SlotDate']
            testtype=request.POST['testname']
            diagCenter=TestsOffered.objects.filter(TestId=testtype)
            res=User.objects.filter(email=request.session['user_email'])
            lat1=res[0].latitude
            long1=res[0].longitude
            res1=Beneficiary.objects.filter(UserId=request.session['userid'])
            tests=DiagnosticCentre.objects.all()
            centerlist=[]
            for i in diagCenter:
                lat2=i.CentreId.latitude
                long2=i.CentreId.longitude
                dis=distance(lat1, lat2, long1, long2)
                print(dis)
                if dis<30:
                    testdata=SlotBookAndReport.objects.filter(TestId=i.TOId,DateOfTest=parse_date(date))
                    if len(testdata)<i.TestsPerDay:
                        val=i.TestsPerDay-len(testdata)
                        centerlist.append([i,val])
            context={
                'centers':centerlist,
                'date':date,
                'bene':res1,
            }
            return render(request,'TestBook.html',context)
        else:
            list=Tests.objects.all()
            context={
                'testlists':list,
            }
            return render(request,'TestBookForm.html',context)
def TestBookSuccess(request):
    if request.method=='POST':
        test=request.POST['TestId']
        print(test)
        test1=TestsOffered.objects.filter(TOId=test)
        print(test1)
        beneId=request.POST['bene']
        beneId1=Beneficiary.objects.filter(BenId=beneId)
        print(beneId1)
        date=request.POST['date']
        date1=parse_date(date)
        report=None
        status=False
        BookTest=SlotBookAndReport(BeneId=beneId1[0],TestId=test1[0],DateOfTest=date1,report=report,status=status)
        try:
            BookTest.save()
        except:
            print('Some Error Incurred')
        return redirect('dashboard')
    else:
        return redirect('TestBook')
def UploadReport(request,SlotId):
    data=SlotBookAndReport.objects.get(SlotId=SlotId)
    if request.method=='POST':
        image1=request.FILES['image']
        data.report=image1
        data.save()
        data1=SlotBookAndReport.objects.get(SlotId=SlotId)
        y=data1.report.url
        print(y)
        y='.'+y
        testimg=image.load_img(y,target_size=(224, 224))
        testimg=image.img_to_array(testimg)
        testimg=np.expand_dims(testimg,axis=0)
        testimg= testimg/255.0
        with model_graph.as_default():
            with tf_session.as_default():
                result1=model.predict(testimg)
        print(result1[0])
        res=result1[0][0]>result1[0][1]
        if res==True:
            res="covid"
            res1=True
        else:
            res="Normal"
            res1=False
        print(res)
        data1.status=res1
        data1.save()
        return redirect('DiagnosticCenterDashboard')
    context={
        'data':data,
    }
    return render(request,'UploadReport.html',context)
def viewReport(request):
    id=request.POST['slotId']
    data=SlotBookAndReport.objects.get(SlotId=id)
    x='/MedApp'+data.report.url
    context={
        'data':data,
        'x':x,
    }
    return render(request,'viewReport.html',context)
def BookWard(request):
    pass
def DoctorConsultation(request,SlotId):
    if request.method=='POST':
        date=request.POST['date']
        doctors=Doctor.objects.all()
        res=[]
        for i in doctors:
            temp=DoctorConsult.objects.filter(Doctor_Id=i,ConsultDate=parse_date(date))
            if len(temp)<i.patient_count_per_day:
                res.append(i)
        context={
            'res':res,
            'SlotId':SlotId,
            'date':date,

        }
        return render(request,'Doctorlist.html',context)

    context={
        'SlotId':SlotId,
    }
    return render(request,'doctorConsultation.html',context)
def DoctorConsultConfirm(request):
    if request.method=='POST':
        date=request.POST['date']
        SlotId=request.POST['SlotId']
        res=SlotBookAndReport.objects.get(SlotId=SlotId)
        doctor=request.POST['doctor']
        res1=Doctor.objects.get(DoctorId=doctor)
        docCon=DoctorConsult(slotId=res,Doctor_Id=res1,ConsultDate=parse_date(date))
        docCon.save()
        return render(request,'success.html')





