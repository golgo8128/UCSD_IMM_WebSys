from django import forms

# http://www.ilian.io/django-forms-choicefield-with-dynamic-values/
# For dynamic update of ModelChoiceField, see:
# http://qiita.com/44d/items/897e5bb20113315af006 

JSFUNCNAME_switch = "switch_enable_writing_new_name"

class FileUpload_Form(forms.Form):
    iprojname_sel = forms.ChoiceField(label  = "Project name",)
    # widget = forms.Select(attrs={"onChange":"switch_enable_writing_new_name()"})),
    # For unknown reason, if we put the above, the field is ignored. ...
    # here without any actual choice information.
    iprojname_new = forms.CharField(label = "New project name", required = False,
                                    help_text = "(Select new project to fill this in)")
    idatatype = forms.ChoiceField(label = "Data type")
    idescr = forms.CharField(label = "Description",
                             widget=forms.TextInput(attrs={"size" : 80}))
    ifile = forms.FileField(label = "Select a file")
    
    def __init__(self, prj_choices = None, dattypes = None,
                 *args, **kwargs):
        super(FileUpload_Form, self).__init__(*args, **kwargs)
        if prj_choices:
            self.fields[ "iprojname_sel" ] = \
                forms.ChoiceField(choices = prj_choices,
                                  label = "Project name",
                                  widget =
                                    forms.Select(attrs
                                        = {"onChange": JSFUNCNAME_switch + "()"}))
        if dattypes:
            self.fields[ "idatatype" ] = \
                forms.ChoiceField(choices = dattypes,
                                  label = "Data type")
