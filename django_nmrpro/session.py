from django.db import transaction
from nmrpro.classes.NMRSpectrum import NMRSpectrum
from .exceptions import SessionError
from time import time
import dill
from models import SessionSpec


@transaction.atomic
def registerSpecs2(request, nmrSpecs):
    if not request.session.session_key or not request.session.exists(request.session.session_key):
        request.session.create()
    

    for s in nmrSpecs:
        if not isinstance(s, NMRSpectrum): 
            continue;
    
        o = None
        if hasattr(s, "__s_id__"):
            try:
                o = SessionSpec.objects.get(s_id=s.__s_id__)
            except SessionSpec.DoesNotExist:
                o = SessionSpec.objects.create(session_id = request.session.session_key)
        else:
            o = SessionSpec.objects.create(session_id = request.session.session_key)
        
        s.__s_id__ = str(o.s_id)
        print s.__s_id__
        o.spectrum = s
        print 'model s'
        o.save()

def getSpecObject(request, s):
    o = None

    sid = getattr(s, "__s_id__", None)    
    if sid is not None:
        try:
            o = SessionSpec.objects.get(s_id=s.__s_id__)
        except SessionSpec.DoesNotExist:
            o = SessionSpec.objects.create(session_id = request.session.session_key)
    else:
        o = SessionSpec.objects.create(session_id = request.session.session_key)
    
    s.__s_id__ = str(o.s_id)
    o.spectrum = s
    
    return o

@transaction.atomic
def registerSpecs(request, nmrSpecs):
    if not request.session.session_key or not request.session.exists(request.session.session_key):
        request.session.create()
    
    if not isinstance(nmrSpecs, list):
        raise TypeError('nmrSpecs should be a list');
    
    nmrSpecs = [s for s in nmrSpecs if isinstance(s, NMRSpectrum)]    
    objects = [getSpecObject(request, s) for s in nmrSpecs]
    [o.save() for o in objects]

def getSessionSpec(idx):
    o_list = SessionSpec.objects.filter(s_id__in=idx)
    if not o_list:
        raise SessionError('Apparently your session spectra has been removed \
            from the server. \r Please refresh the page to reload the spectra.')
    return [o.spectrum for o in o_list]
 
