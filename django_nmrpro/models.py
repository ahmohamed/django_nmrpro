from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session

import uuid
import dill
import json
import numpy as np
from nmrpro.classes.NMRSpectrum import NMRSpectrum, DataUdic

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()
    
class SessionSpec(models.Model):
    s_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _original_array = models.BinaryField(null=False);
    _original_udic = models.TextField(null=False)
    _original_dtype = models.CharField(max_length=15, null=False)
    _original_shape = models.CharField(max_length=31, null=False)
    _history = models.BinaryField(blank=True)
    session = models.ForeignKey(Session)
    accessed = AutoDateTimeField(default=timezone.now)
    
    def get_original(self):
        array = self._original_array
        dtype = self._original_dtype
        shape = json.loads(self._original_shape)
        original_array = np.frombuffer(array, dtype).reshape(shape)
        
        udic = json.loads(self._original_udic);
        for i in range(0, udic['ndim']): udic[i] = udic.pop(str(i))
        
        return DataUdic( original_array,  udic)
    
    def set_original(self, val):
        self._original_array =  np.array(val)
        self._original_dtype = val.dtype
        self._original_shape = json.dumps(val.shape)
        self._original_udic = json.dumps(val.udic)
    
    original = property(get_original, set_original)

    def get_history(self):
        return dill.loads( str(self._history) )
    
    def set_history(self, val):
        self._history =  buffer( dill.dumps(val) )

    history = property(get_history, set_history)
    
    def get_spectrum(self):
        spec = NMRSpectrum(self.original, self.original.udic)
        spec.history = self.history
        spec.__s_id__ = str(self.s_id)
        return spec.update_data()
    
    def set_spectrum(self, s):
        # If it is the first update
        if not self._original_udic:
            self.original = s.original
        
        #Otherwise, only update the history
        self.history = s.history
        
    spectrum = property(get_spectrum, set_spectrum)
    
        