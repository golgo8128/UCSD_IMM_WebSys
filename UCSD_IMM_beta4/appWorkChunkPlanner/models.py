
import datetime
import pytz

from django.utils import timezone
from django.db import models

# Create your models here.

from django.contrib.auth.models import User # , AnonymousUser
from django.forms import ModelForm
from django import forms

from .Usefuls1 import get_tzone_str

# http://stackoverflow.com/questions/9594081/how-to-use-jquery-ui-datepicker-as-a-django-widget

class WorkChunk_Class(models.Model):
    user = models.ForeignKey(User, verbose_name = "User")
    
    type_name = models.CharField(max_length = 100)
    type_note = models.TextField(default = "")

    class Meta:
        verbose_name = 'Work chunk class'
        verbose_name_plural = 'Work chunk classes'

    def __str__(self):
        return self.type_name


class WorkChunk_Type(models.Model):
    user = models.ForeignKey(User, verbose_name = "User")
    
    type_name = models.CharField(max_length = 100)
    type_note = models.TextField(default = "")

    class Meta:
        verbose_name = 'Work chunk type'

    def __str__(self):
        return self.type_name


class WorkChunk_Project(models.Model):
    user = models.ForeignKey(User, verbose_name = "User")
    
    proj_name = models.CharField(max_length = 100)
    proj_note = models.TextField(default = "")
 
    class Meta:
        verbose_name        = "Project for the work chunks"  
        verbose_name_plural = "Projects for the work chunks"

    def __str__(self):
        return self.proj_name
    
class WorkChunk_Plan_Status(models.Model):
    
    status_name = models.CharField(max_length = 20)
    # "Completion expected", "Canceled", "Completed"
 
    class Meta:
        verbose_name        = "Plan status"  
        verbose_name_plural = "Plan status"

    def __str__(self):
        return self.status_name    
          
# class WorkChunk_Plan_Status_Form(ModelForm):
#        
#     class Meta:
#         model = WorkChunk_Plan_Status        
#         exclude = ()
           
class WorkChunk_Plan(models.Model):
    plan_title  = models.CharField(max_length = 100)
    creator     = models.ForeignKey(User, verbose_name = "Creator")
    timestamp   = models.DateTimeField("Planned time")
    chunk_class = models.ForeignKey(WorkChunk_Class)
    chunk_type  = models.ForeignKey(WorkChunk_Type)
    project     = models.ForeignKey(WorkChunk_Project)
    begin_time  = models.DateTimeField("Planned begin time")
    finish_time = models.DateTimeField("Planned finish time")
    plan_status = models.ForeignKey(WorkChunk_Plan_Status)
    timestamp_cancel = models.DateTimeField("Canceled time", null=True, blank=True)
    plan_note   = models.TextField(default = "", blank=True)
    plan_cancel_note = models.TextField(default = "", blank=True)

    def worked_records(self):
        
        return WorkChunk_Record.objects.filter(corresp_plan__id = self.id)

    def served_evals(self):
        
        return WorkChunk_Served.objects.filter(worked_plan__id = self.id)

    def plan_links_from_this(self):
        
        return WorkChunk_Plan_Link.objects.filter(plan_src = self)
    
    def plan_links_to_this(self):    
    
        return WorkChunk_Plan_Link.objects.filter(plan_tgt = self)

    def bool_started_late(self):
        
        started_time = self.work_started_time()
        if started_time and self.begin_time < started_time: 
            return True
        else:
            return False
    
    def bool_started_early(self):
        
        started_time = self.work_started_time()
        if started_time and started_time < self.begin_time: 
            return True
        else:
            return False

    def bool_finished_late(self):
        
        finished_time = self.work_finished_time()
        if finished_time and self.finish_time < finished_time:
            return True
        else:
            return False

    def bool_finished_late(self):
        
        finished_time = self.work_finished_time()
        if finished_time and self.finish_time < finished_time:
            return True
        else:
            return False

    def bool_finished_early(self):
        
        finished_time = self.work_finished_time()
        if finished_time and finished_time < self.finish_time:
            return True
        else:
            return False


    def bool_not_started_yet(self):
        
        if len(self.worked_records()) == 0 and self.begin_time < timezone.now():
            return True
        else:
            return False

    def bool_took_longer(self):
        
        time_spent = self.time_spent_start_to_finish()
        if time_spent is not None and self.finish_time - self.begin_time < time_spent:
            return True
        else:
            return False 

    def bool_took_shorter(self):
        
        time_spent = self.time_spent_start_to_finish()
        if time_spent is not None and time_spent < self.finish_time - self.begin_time:
            return True
        else:
            return False 

    def bool_completed(self):
        
        return self.plan_status.status_name == "Completed"

    def bool_canceled(self):
        
        return self.plan_status.status_name == "Canceled"

    def bool_plan_spans_different_days(self):

        begin_time_local  = self.begin_time.astimezone(pytz.timezone(get_tzone_str()))
        finish_time_local = self.finish_time.astimezone(pytz.timezone(get_tzone_str()))
               
        return (finish_time_local.day != begin_time_local.day or 
                self.finish_time - self.begin_time >= datetime.timedelta(days = 1))
            
    def work_started_time(self):
        
        started_time = None
        for wc_rec in self.worked_records():
            if started_time is None or wc_rec.start_time < started_time:
                started_time = wc_rec.start_time
        return started_time
    
    def work_last_end_time(self):
        
        last_end_time = None
        for wc_rec in self.worked_records():
            if last_end_time is None or last_end_time < wc_rec.end_time:
                last_end_time = wc_rec.end_time    
        return last_end_time
                
    
    def work_finished_time(self):
        
        finished_time = None
        if self.bool_completed():
            finished_time = self.work_last_end_time()

        return finished_time

    def time_spent_start_to_last_end(self):
        
        started_time  = self.work_started_time()
        last_end_time = self.work_last_end_time()
        
        if started_time is None or last_end_time is None:
            return None
        else:
            return last_end_time - started_time  
    
    def time_spent_start_to_finish(self):
        
        started_time  = self.work_started_time()
        finished_time = self.work_finished_time()
        
        if started_time is None or finished_time is None:
            return None
        else:
            return finished_time - started_time  
        

    class Meta:
        verbose_name        = "Plan for the work chunks"  
        verbose_name_plural = "Plans for the work chunks"
        
    def __str__(self):
        return self.plan_title
    

class WorkChunk_Plan_Form(ModelForm):
    
    plan_title = forms.CharField(widget=forms.Textarea(attrs={ 'cols': 40,
                                                               'rows':  1 }))
    
    link_planids_str = forms.CharField(required = False)

        
    class Meta:
        model = WorkChunk_Plan
        exclude = ('creator', 'timestamp', "plan_status", "timestamp_cancel") # , 'begin_time', 'finish_time')
        
    
class WorkChunk_Record(models.Model):
    timestamp       = models.DateTimeField("Recorded time")
    corresp_plan    = models.ForeignKey(WorkChunk_Plan)
    start_time      = models.DateTimeField("Started time")
    end_time        = models.DateTimeField("Ended time")
    weight_per_time = models.FloatField(default = 0.8)
    rec_note        = models.TextField(default = "", blank=True)
  
    class Meta:
        verbose_name        = "Work record for the planned chunks"  
        verbose_name_plural = "Work records for the planned chunks"
          
    def __str__(self):
        # wc_rec_same_plan = WorkChunk_Record.objects.filter(corresp_plan = self.corresp_plan)
        # len(wc_rec_same_plan)
        
        return "Rec %s on %s - %s" % (self.corresp_plan.plan_title,
                                      self.start_time.strftime("%b %d, %Y (%H:%M)"),
                                      self.end_time.strftime("%b %d, %Y (%H:%M)"))
          
class WorkChunk_Record_Form(ModelForm):
    
    weight_per_time = forms.CharField(widget=forms.Textarea(attrs={ 'cols': 5,
                                                                    'rows': 1 }),
                                      initial="0.80")    
    
    # This will be associated with WorkChunk_Plan
    plan_status = forms.ModelChoiceField(queryset = WorkChunk_Plan_Status.objects.all(),
                                         to_field_name = "status_name", 
                                         empty_label = None)

    class Meta:
        model = WorkChunk_Record
        exclude = ('timestamp', )
        
        
class WorkChunk_Served(models.Model):
    """ Was the chunk of work done actually useful?
    e.g. The work was absolutely necessary and useful later on.
    
    """
    timestamp      = models.DateTimeField("Recorded time")
    worked_plan    = models.ForeignKey(WorkChunk_Plan)
    score          = models.IntegerField(default = 70)
    served_note    = models.TextField(default = "")

    class Meta:
        verbose_name        = "How the product was useful afterward"  
        verbose_name_plural = "How the product was useful afterward"
    
    def __str__(self):
        # wc_rec_same_plan = WorkChunk_Record.objects.filter(corresp_plan = self.corresp_plan)
        # len(wc_rec_same_plan)
        
        return "Srv %s" % (self.worked_plan.plan_title, )    
    
class WorkChunk_Served_Form(ModelForm):
    
    score = forms.IntegerField(widget = forms.NumberInput(attrs={ "style" :"width: 4em",
                                                                  "min"   : "0",
                                                                  "max"   : "100" }),
                               initial = 70)
    
    class Meta:
        model = WorkChunk_Served
        exclude = ('timestamp', )


class WorkChunk_Plan_Link_Type(models.Model):
    
    link_type_name = models.CharField(max_length = 100)
        
    def __str__(self):
        return self.link_type_name        
        
class WorkChunk_Plan_Link(models.Model):
    
    plan_src   = models.ForeignKey(WorkChunk_Plan, related_name = "plan_src",
                                   verbose_name = "Source plan")
    plan_tgt   = models.ForeignKey(WorkChunk_Plan, related_name = "plan_tgt",
                                   verbose_name = "Target plan")
    link_weight = models.FloatField(default = 0.8)
    link_type   = models.ForeignKey(WorkChunk_Plan_Link_Type,
                                    verbose_name = "Link type")
    link_note   = models.TextField(default = "", blank=True)
  
    def __str__(self):
        return "%s --- %s" % (str(self.plan_src),
                              str(self.plan_tgt))   



