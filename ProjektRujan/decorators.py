from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect



def student(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user        
        if profile.id is not None and profile.Roles_id == 1:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')

    return wrap


def profesor_or_admin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):        
        if request.user is None:            
            return redirect('/login')

        student_id = int(request.POST.get("Student_id", -1))    
        if request.user.id == student_id and request.user.Roles_id != 1:
            return redirect('/')
        else:
            return function(request, *args, **kwargs)         

    return wrap