from multiprocessing import context
from time import time
from winreg import HKEY_PERFORMANCE_DATA
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Korisnici,Dokumenti, Korisnici, Student_Dokument ,Uloge
from .forms import DocumentCreate, LoginForm, RegisterForm, ShareForm,UserCreate
from .decorators import profesor_or_admin, student
from collections import OrderedDict
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from .filters import FilterForm
from django.db.models import Count

# Create your views here.




def home(request):
    return render(request,"pages/index.html")

##LOGIN
def login_page(request):
    loggedUser = request.user
    if loggedUser.id:
        return redirect("/")

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username  = form.cleaned_data.get("Email")
        password  = form.cleaned_data.get("Password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context["login_error"] = "Failed to login, wrong username and/or password!"
            print("Error")
    return render(request, "project/login.html", context)


##REGISTER
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    
    if form.is_valid():
        form.save()
        return redirect('/login')
    return render(request, "project/register.html", context)

##LOGOUT
@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('/login')


##ADMIN PAGE
#---------------------------------------------------------------------------------------------------------------------------------

# ##CREATE USER
@profesor_or_admin
def create_user(request):
    uploadForm = UserCreate()
    if request.method == 'POST':
        uploadForm = UserCreate(request.POST)
        if uploadForm.is_valid():
            uploadForm.save()
            return redirect('/users')
        else:
            return HttpResponse("""Wrong form!""")
    else:
        return render(request, 'project/user_create.html', {'user_form':uploadForm})

@profesor_or_admin
def edit_user(request, user_id):
    user_id = int(user_id)
    try:
        user = Korisnici.objects.get(id = user_id)
    except Korisnici.DoesNotExist:
        return redirect('/users')
    user_form = UserCreate(request.POST or None, instance = user)
    if user_form.is_valid():
       user_form.save()
       return redirect('/users')
    return render(request, 'project/user_edit.html', {'user_form':user_form})

#DELETE
@profesor_or_admin
def delete_user(request, user_id):
    user_id = int(user_id)
    try:
        korisnik = Korisnici.objects.get(id = user_id)
    except Korisnici.DoesNotExist:
        return redirect('/users')
    korisnik.delete()
    return redirect('/users')

@profesor_or_admin
def users_list_all(request):
    context={}
    p = Paginator(Korisnici.objects.filter().order_by('Role_id'),3)
    page = request.GET.get('page')
    korisnik_lista = p.get_page(page)
    context["users"] =  korisnik_lista
    return render(request, "project/users_list.html", context)

@profesor_or_admin
def users_list_by_students(request):
    context={}
    context["users"] = Korisnici.objects.filter(Role_id=('3')).order_by('Email')
    return render(request, "project/users_list.html", context)

@profesor_or_admin
def users_list_by_profesors(request):
    context={}
    context["users"] = Korisnici.objects.filter(Role_id=('2')).order_by('Email')
    return render(request, "project/users_list.html", context)


##PROFESOR PAGE
##------------------------------------------------------------------------------------------------------------------


def document_list(request):
    user_id=request.user.id
    profesors=Dokumenti.objects.all()
    profFilter=FilterForm(request.GET,queryset=profesors)
    
    
    if request.user.Role_id==2:
        documents = Dokumenti.objects.filter(Kreator_id=user_id).order_by('Vrijeme')
    
    if request.user.Role_id==3:
        
        sd=Student_Dokument.objects.filter(StudentID_id=user_id)
        if sd:
            for d in sd:
                documents=Dokumenti.objects.filter(id=d.DokumentID_id).order_by('Vrijeme')
        else:
            return HttpResponse("""Ooops! No documents shared to you!""")
    else:
        documents = Dokumenti.objects.all().order_by('Vrijeme')
    context={}
    context["docs"]=documents
    context['profs']=profFilter
    
    return render(request,'project/document_list.html',context)

@profesor_or_admin
def upload(request):
    if request.method == 'POST':
        form = DocumentCreate(request.POST, request.FILES)
        if form.is_valid():
            new_submit = form.save(commit=False)
            new_submit.Kreator_id = request.user.id
            new_submit.save()
            form.save()
            return redirect('document_list')
    else:
        form = DocumentCreate()
        
    return render(request, 'project/upload.html', {'form':form } )

def share_document(request, document_id):
    documentid=int(document_id)
    share_form = ShareForm(request.POST or None) 
    
    if share_form.is_valid():
        student_list = share_form.cleaned_data.get("Studenti")
        print(student_list)
        
        for student in student_list:
                temp=share_form.save(commit=False)
                print(documentid)
                print(student)            
                temp.DokumentID_id=documentid
                temp.StudentID_id=student.id
                temp.save()
                share_form.save_m2m()
                
                
        
                
        return redirect('/document_list')
    return render(request, 'project/document_share.html', {'document_form':share_form})


def stop_share_document(request, document_id):
    documentid=int(document_id)
    share_form = ShareForm(request.POST or None) 
    
    if share_form.is_valid():
        student_list = share_form.cleaned_data.get("Studenti")
        print(student_list)
        
        for student in student_list:
                temp=share_form.save(commit=False)
                print(documentid)
                print(student)
                if temp.id is not None:            
                    temp.DokumentID_id=documentid
                    temp.StudentID_id=student.id
                    temp.save()
                    share_form.delete(temp)
                else:
                    continue
                  
                
        return redirect('/document_list')
    return render(request, 'project/document_stop_share.html', {'document_form':share_form})

@profesor_or_admin
def delete_document(request, document_id):
    document_id = int(document_id)
    try:
        document = Dokumenti.objects.get(id = document_id)
    except Korisnici.DoesNotExist:
        return redirect('/document_list')
    document.delete()
    return redirect('/document_list')


##### STUDENT PAGE

def document_list_by_name(request):
    user_id=request.user.id
    if request.user.Role_id==2:
        documents = Dokumenti.objects.filter(Kreator_id=user_id).order_by('Naslov')
    
    if request.user.Role_id==3:
        sd=Student_Dokument.objects.filter(StudentID_id=user_id)
        for d in sd:
            documents=Dokumenti.objects.filter(id=d.DokumentID_id).order_by('Naslov')
    else:
        documents = Dokumenti.objects.all().order_by('Naslov')
    return render(request,'project/document_list_by_name.html',{'docs':documents})


def profesor_document_list(request,user_id):
    userid=int(user_id)
    documents=Dokumenti.objects.filter(Kreator_id=userid).order_by('Vrijeme')
    
    return render(request,'project/profesor_document_list.html',{'docs':documents})


#RUJAN

def rujan(request):
    context={}
    profesori=Korisnici.objects.filter(Role_id=2).order_by('Role_id')
    for p in profesori:
        dokumenti=Dokumenti.objects.filter(Kreator_id=p.id).aggregate(Count('id'))
        print(dokumenti)    
    context["users"] =  profesori
    context["id_count"] =  dokumenti
    return render(request, "project/rujan.html", context)

def document_page(request,user_id):
    if request.user.Role_id == 1:
        
        context={}
        documents=Dokumenti.objects.filter(Kreator_id=user_id).order_by('Vrijeme')
        lst=[]
        for d in documents:
            studenti=Student_Dokument.objects.filter(DokumentID_id=d.id).aggregate(Count('StudentID_id'))
            lst.append(studenti)
            continue
        print(studenti)
        context["studenti"]=lst
        context["docs"]=documents
        
    else:
        return HttpResponse("""Ooops! Only admin allowed!""")
    return render(request,'project/document_page.html',context)
    
    
@profesor_or_admin
def document_edit(request,document_id):
    if request.user.Role_id==1 or request.user.Role_id==2:
        
        try:
            document = Dokumenti.objects.get(id = document_id)
        except Dokumenti.DoesNotExist:
            return redirect('/document_list')
        document_form = DocumentCreate(request.POST ,request.FILES,instance=document)
        if document_form.is_valid():
            document_form.save(commit=False)
            temp=document_form
            temp.Azuriran=time.now()
            temp.save()
            document_form.save()
            return redirect('/document_list')
    else:
        return HttpResponse("""Ooops! Only admin and profesor allowed!""")
    return render(request, 'project/document_edit.html', {'document_form':document_form})