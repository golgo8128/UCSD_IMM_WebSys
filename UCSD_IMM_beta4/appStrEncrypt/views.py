from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.conf import settings

from Str_Proc.StrEncryption_simple1_4 import str_enc_simple

# Record this secretly somewhere, or you may lost a way to decode strings.
# Working with this as of Feb. 15, 2016.
conv = (r'''!#$%&*+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ^_abcdefghijklmnopqrstuvwxyz|~''',
        r'''p01I<6x29*LCyMsb^cZi#fFavE:87dmYw;Pez3QH5$%&gj4A=_RVKu>-q.GOr~oJT+|?kD,nBhUNlWSXt!@''')
segm_len = 3

def index(request):
    
    contxt = RequestContext(request,
                            { })
    
    templt = loader.get_template("appStrEncrypt/str_input.html")
    return HttpResponse(templt.render(contxt))

def strconv(request):
    
    istr = request.POST["istring"].strip()
    idir = request.POST["direncdec"]
    
    if not istr:
        return HttpResponseRedirect(reverse("appStrEncrypt:index"))
    elif idir == "Decryption":
        return HttpResponseRedirect(reverse("appStrEncrypt:strdec", args = (istr,)))
    else:
        return HttpResponseRedirect(reverse("appStrEncrypt:strenc", args = (istr,)))


def strenc(request, istr):
    
    return HttpResponse('"%s" --> "%s"'
                        % (istr, str_enc_simple(istr.strip(),
                                                conv,
                                                segm_len,
                                                idir = "Forward")))

@login_required
def strdec(request, istr):
    
    return HttpResponse('"%s" --> "%s"'
                        % (istr, str_enc_simple(istr.strip(),
                                                conv,
                                                segm_len,
                                                idir = "Reverse")))

    