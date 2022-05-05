
from django.shortcuts import render

# Create your views here.

import getpass # getpass.getuser()
import pytz

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .accauth_info_input import AccAuth_Info_Input

def entry(request):

        accauthform = AccAuth_Info_Input()
        accauthform_choice_i_user_h = \
            dict([(str(ikey), ival)
                  for ikey, ival in AccAuth_Info_Input().fields['i_user'].choices])
        # type of .choices: <class 'django.forms.models.ModelChoiceIterator'>
        
        if request.method == "POST":
                username  = accauthform_choice_i_user_h[ request.POST["i_user"] ]
                password  = request.POST["i_pass"]
                user_auth = authenticate(username = username,
                                         password = password)
                if user_auth is None:
                        auth_success = False                
                        acc_activ = None
                elif not user_auth.is_active:
                        auth_success = True
                        acc_activ = False
                else:
                        auth_success = True
                        acc_activ = True            
        else:
                auth_success = None
                acc_activ = None

        if auth_success is True and acc_activ is True:
            login(request, user_auth)
            # timezone.activate(pytz.timezone("US/Pacific")) # <---------- !!! Time zone !!! 
            if "next" in request.GET:
                return HttpResponseRedirect(request.GET["next"])
            else:
                return HttpResponseRedirect(reverse("AccAuth_TZ:authenticated"))
        else:
            contxt = RequestContext(request,
                  { "accauth_info_input" : AccAuth_Info_Input,
                    "auth_success"       : auth_success,
                    "acc_activ"          : acc_activ,
                    "current_user"       : request.user,
                    "server_user"        : getpass.getuser() })
            templt = loader.get_template("AccAuth_TZ/entry1.html")
            # print("Anonymous user?", request.user.is_anonymous())
            return HttpResponse(templt.render(contxt))


# @login_required decorator:
# If the user isn't logged in, the user is redirected to settings.LOGIN_URL,
# with the accessed absolute path in the query string.
# Example: /accounts/login/?next=/polls/3/.
# Also see http://stackoverflow.com/questions/25229830/django-login-required-decorator-not-passing-next-value-to-template
# request.POST['next']
@login_required
def authenticated(request):
        
    return HttpResponse("Authentication was successful. Welcome %s!" % request.user.username)


@login_required
def getout(request):
    
    iusername = request.user.username
    logout(request)
    return HttpResponseRedirect(reverse("AccAuth_TZ:goodbye", args = (iusername, )))


def goodbye(request, iusername):

    return HttpResponse("Good bye %s!" % iusername)


@login_required
def test_member_page1(request):
        
        return HttpResponse("This page is only for those who was authenticated. Welcome %s!" % request.user.username)
