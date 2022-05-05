
from django.shortcuts import render

# Create your views here.

import pytz

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template import RequestContext, loader

from .accauth_info_input import AccAuth_Info_Input

def entry(request):

        from pprint import pprint

        accauthform = AccAuth_Info_Input()
        accauthform_choice_i_user_h = \
            dict([(str(ikey), ival) for ikey, ival in AccAuth_Info_Input().fields['i_user'].choices])
        # pprint(request.method, open("/Users/rsaito/Desktop/tmp1.txt", "a"))
        
        # from django.conf import settings
        # pprint(dir(settings), open("/Users/rsaito/Desktop/tmp1.txt", "a"))
        
        if request.method == "POST":
                # pprint(request.POST, open("/Users/rsaito/Desktop/tmp1.txt", "a"))
                # pprint(accauthform_choice_i_user_h, open("/Users/rsaito/Desktop/tmp1.txt", "a"))
                username = accauthform_choice_i_user_h[ request.POST["i_user"] ]
                password = request.POST["i_pass"]
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
        
        # pprint(user_auth, open("/Users/rsaito/Desktop/tmp1.txt", "a"))  
                
        if auth_success is True and acc_activ is True:
            login(request, user_auth)
            # timezone.activate(pytz.timezone("US/Pacific")) # <---------- !!! Time zone !!! 
            if "next" in request.GET:
                return HttpResponseRedirect(request.GET["next"])
            else:
                return HttpResponseRedirect(reverse("AccAuth:authenticated"))
        else:
            contxt = RequestContext(request,
                  { "accauth_info_input" : AccAuth_Info_Input,
                    "auth_success"       : auth_success,
                    "acc_activ"          : acc_activ })
            templt = loader.get_template("AccAuth/entry1.html")
            return HttpResponse(templt.render(contxt))


# If the user isn't logged in, redirect to settings.LOGIN_URL,
# passing the current absolute path in the query string.
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
    return HttpResponseRedirect(reverse("AccAuth:goodbye", args = (iusername, )))


def goodbye(request, iusername):

    return HttpResponse("Good bye %s!" % iusername)


@login_required
def test_member_page1(request):
        
        return HttpResponse("This page is only for those who was authenticated. Welcome %s!" % request.user.username)
