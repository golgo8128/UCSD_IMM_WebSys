from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.conf import settings

from .models import FileUploaded, Project, DataType
from .fileupload_form import FileUpload_Form, JSFUNCNAME_switch

from pprint import pprint

NEW_PROJ_LABEL = "[ New project ]"

@login_required
def fileupload(request):
       
    # Handle file upload

    prj_choices = sorted([(prj.projname, prj.projname)
                          for prj in Project.objects.all()])
    prj_choices.append((NEW_PROJ_LABEL, NEW_PROJ_LABEL))

    dattype_names = sorted([(dattyp.datatype, dattyp.datatype)
                            for dattyp in DataType.objects.all()])

    if request.method == "POST":
        fileupload_form = FileUpload_Form(prj_choices = prj_choices,
                                          dattypes = dattype_names,
                                          data = request.POST,
                                          files = request.FILES)
        if fileupload_form.is_valid():
            projname_sel = request.POST["iprojname_sel"]
            if projname_sel == NEW_PROJ_LABEL:
                projname_new = request.POST["iprojname_new"]
                proj = Project(projname = projname_new)
                proj.save()
            else:
                proj = Project.objects.filter(projname = projname_sel)[0]
                
            idatype = DataType.objects.filter(datatype = request.POST["idatatype"])[0]

            # pprint(idatype, open("/Users/rsaito/Desktop/tmpout2.txt", "a"))

            uploaded_file = FileUploaded(ifile = request.FILES["ifile"],
                                         iuser = request.user,
                                         itimestamp_upload = timezone.now(),
                                         itimestamp_touch  = timezone.now(),
                                         ifilename = request.FILES["ifile"].name,
                                         iproj = proj,
                                         idatatype = idatype,
                                         idescription = request.POST["idescr"])
            uploaded_file.save()
            imode = "redirect"
        else:
            imode = "display error"
    else:
        fileupload_form = FileUpload_Form(prj_choices = prj_choices,
                                          dattypes = dattype_names)
        imode ="display"

    # pprint("\n" + imode, open("/Users/rsaito/Desktop/tmpout2.txt", "a"))
    # pprint(fileupload_form, open("/Users/rsaito/Desktop/tmpout2.txt", "a"))

    if imode == "redirect":
        # Redirect to the document list after POST
        return HttpResponseRedirect(reverse("FileUpload:fileupload_done"))
    else:
        # Make sure to have {% csrf_token %}, even in the case of "display error".
        contxt = RequestContext(request,
              { "fileupload_form" : fileupload_form,
                "new_proj_label":  NEW_PROJ_LABEL,
                "iproj_choicefield_id" : fileupload_form.auto_id % "iprojname_sel",
                "inewproj_textfield_id" : fileupload_form.auto_id % "iprojname_new",
                "jsfuncname_switch" : JSFUNCNAME_switch, })
        templt = loader.get_template("FileUpload/fileupload3.html")
        return HttpResponse(templt.render(contxt))

        # Load files for listing
        # documents = FileUploaded.objects.all()

@login_required
def fileupload_done(request):
    contxt = RequestContext(request, {})
    templt = loader.get_template("FileUpload/fileuploaded1.html")
    return HttpResponse(templt.render(contxt))

