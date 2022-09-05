from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect



def student(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user        
        if profile.id is not None and profile.Role_id == 3:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')

    return wrap



def profesor_or_admin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):        
        if request.user is None:            
            return redirect('/login')

        user_id = int(request.POST.get("id", -1))    
        if request.user.id == user_id and request.user.Role_id != 3:
            return redirect('/')
        else:
            return function(request, *args, **kwargs)         

    return wrap