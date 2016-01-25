from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http.request import QueryDict
from django.core.cache import cache
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from django.conf import settings


from models import SessionSpec
from nmrpro.readers import fromFile
from nmrpro.plugins import *
from nmrpro.exceptions import NoNMRDataError
from nmrpro.classes.NMRSpectrum import NMRSpectrum

from json import dumps
import encoder
import exceptions


from .session import registerSpecs, getSessionSpec
from re import compile
import os.path


# TODO: add NMRFILES_ROOT in settings, readme.
media_root = getattr(settings, 'NMRFILES_ROOT', None)
if media_root is None:
    if getattr(settings, 'BASE_DIR', None) is not None:
        media_root = os.path.join( settings.BASE_DIR,
                                   getattr(settings, 'MEDIA_ROOT', '') )


def jsonError(f):
    def newf(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except exceptions.SpecError as e:
            error_json = {'error':{'name':e.__class__.__name__, 'message':e.message}}
            return HttpResponse(dumps(error_json))
    newf.__name__ = f.__name__
    return newf


def jsonSpectrum(f):
    def newf(*args, **kwargs):
        query = args[0].GET

        ret = f(*args, **kwargs)

        #TODO: If nmrSpecs.size > 1: return NMRDataset(*nmrSpecs)
        
        format_ = query.get('format', 'png16')
        encoding = encoder.pngSpecEncoder if format_ == 'png' else encoder.png16SpecEncoder
        
        res = HttpResponse(dumps(ret, cls=encoding))
        res['Access-Control-Allow-Origin'] = '*'
        return res
    newf.__name__ = f.__name__
    return newf


@jsonError
def menu(request):
    #print(dumps(JSCommand.get_menu()))
    actions = JSCommand.get_functions()
    #print('plugins',actions)
    return HttpResponse(dumps(JSCommand.get_menu()))


def plugin_caller(specs, query):
    p = compile("(^.+?)_.*$") # Add '?' to prevent greedy matching
    unique_plugins = set(str(p.match(s).groups(0)[0]) for s in query.keys() if p.match(s))
    
    plugin_funcs = JSCommand.get_functions()
    for p in unique_plugins:
        # print("plugin: ", p,plugins.base.plugin_funcs.keys())
        if plugin_funcs.has_key(p):
            start=len(p+"_")
            params = {k[start:]:v for (k,v) in query.items() if k.startswith(p+"_") and len(k) > start}
            query_params = QueryDict('', mutable=True)
            query_params.update({k:v for (k,v) in query.items() if k.startswith(p+"_")})
            params['query_params'] = query_params.urlencode()
            specs = plugin_funcs[p](specs, params)
            #print(plugin_funcs[p].__name__)
            #import pdb; pdb.set_trace()
        
        else:
            raise exceptions.PluginNotFoundError('Can\'t find plugin %s' %p)
    return specs


@jsonError
@jsonSpectrum
def proc_plugin(request):
    sessionid = request.session.session_key
    cache.set(sessionid, "Request received")
    
    s_id = request.GET.get('sid')
    preview = request.GET.get('preview', '0') == '1'

    specs = getSessionSpec( eval(s_id) )

    ret = plugin_caller(specs, request.GET)
    
    if preview == False:
        registerSpecs(request, ret)
    return ret
    
@jsonError
@jsonSpectrum
def spec_url(request, url):
    validate = URLValidator()
    
    try:
        validate(url)
        # TODO: download url to tempfile
    except ValidationError:
        if media_root is None:
            raise NoNMRDataError('The path supplied has no NMR spectra: %s' %url)
            
        abs_url = os.path.abspath(os.path.join(media_root, url))
        if abs_url[:len(media_root)] != media_root:
            raise NoNMRDataError('Permission denied to access this url: %s' %url)
    
    specs = fromFile(abs_url)
    if isinstance(specs, NMRSpectrum):
        specs = [specs]
    registerSpecs(request, specs)
    return specs


@cache_page(60 * 15)
def view_spectrum(request, url):
    return render_to_response('getSpectrum.html', {'spec_url':url, 'request':request})

@jsonError
@jsonSpectrum
def coffees_test(request):
    import os.path
    abs_url = os.path.join(os.path.dirname(__file__), 'static/nmrpro/demo.tar.gz')
    specs = fromFile(abs_url)
    registerSpecs(request, specs)
    return specs
    

def coffees_view(request):
    return render_to_response('coffees_test.html')