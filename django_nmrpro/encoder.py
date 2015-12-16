from nmrpro.classes.NMRSpectrum import NMRSpectrum1D, NMRSpectrum2D, DataUdic, SpecFeature, SpecLike
import numpy as np
from PIL import Image
from json import JSONEncoder
from base64 import b64encode
from io import BytesIO

def scale_data(data, bits, phases):
    data = data.copy()
    
    if phases == "both":
        max_num = (2.0**bits - 1) /2
        data_range = max(abs(data.max()), abs(data.min()))
        data *=(max_num/data_range)
        data += max_num
        return data
    
    min_data = data.min()
    if phases == "positive":
        max_num = (2.0**bits) -1
        if min_data < 0:
            data -= min_data
        
        data *=(max_num/data.max())
        return data

def get_data_as_png(obj):
    im = Image.fromarray(obj, mode='L')
    data = BytesIO()
    im.save(data, format="png")
    data.flush()
    data.seek(0)
    return data


def reshape_by_factor(obj):
    factor=1;
    for i in range(2,128):
        if obj.shape[0]%i ==0:
            factor = i
    
    return obj.reshape( (factor, obj.shape[0]/factor) )
    
def encodeBytesIO(obj):
    return b64encode(obj.getvalue())



def encode1DArrayAsPNG(obj, format):
    if format == 'png':
        obj = scale_data(obj, 8, "positive")        
        obj = np.uint8( obj )
    elif format == 'png16':
        obj = scale_data(obj, 16, "positive")        
        obj = np.uint16( obj )
        obj = obj.view(np.uint8)
        obj = np.concatenate( (obj[0::2],obj[1::2]) )
    else:
        raise ValueError('Uncupported encoding format: ', format)
    
    
    # Because we encode the the 1D data, and images are 2D,
    # we need to convert reshape 1D data into 2D.
    # Otherwise, the image is will be 1 pixel high, and the web browser will
    # interpret it as completely transparent (baecause 1 pixel is somewhat below the human 
    # eye precision, or just because?).
    obj = reshape_by_factor(obj)
    
    data = get_data_as_png(obj)
    data = encodeBytesIO(data)
    
    return data

def encode1DSpec(obj, format):
    x_domain = obj.uc[0].ppm_limits()
    label = obj.udic['Name']
    x_label = obj.udic[0]['label']
    if hasattr(obj, "__s_id__"):
        s_id = obj.__s_id__
    else:
        s_id = None
    
    obj = obj.real
    y_domain = [float(obj.min()), float(obj.max())]
    
    # write data as png image
    ouput_format = format
    data = encode1DArrayAsPNG(obj, format)
    
    return {'format':ouput_format,
    'data':data,
    'x_domain':x_domain,
    'y_domain':y_domain,
    'bits': 8 if format == 'png' else 16,
    'nd':1,
    's_id': s_id,
    'label': label,
    'x_label':x_label
    }

def encode2DSpec(obj, format):
    x_domain = obj.uc[1].ppm_limits()
    y_domain = obj.uc[0].ppm_limits()
    x_label = obj.udic[1]['label']
    y_label = obj.udic[0]['label']
    label = obj.udic['Name']
    
    if hasattr(obj, "__s_id__"):
        s_id = obj.__s_id__
    else: s_id = None
    
    obj = obj.real_part()
    #obj = np.sign(obj) * np.log(np.abs(obj) + 1)
    print(obj.shape)
    
    
    z_domain = max( abs(float(obj.min())), abs(float(obj.max())) )
    z_domain = [-z_domain, z_domain]
    print(z_domain)
    
    obj = scale_data(obj, 8, "both")
    obj = np.uint8( obj )
    
    # write data as png image
    ouput_format = 'png'
    
    # Transposing and then reversing the array was the only way
    # to align the spectrum on the axes correctly.
    data = get_data_as_png(obj[::-1])
    data = encodeBytesIO(data)
    
    return {'format':ouput_format,
    'data': data,
    'x_domain':x_domain,
    'y_domain':y_domain,
    'z_domain':z_domain,
    'bits':8,
    'nd':2,
    's_id': s_id,
    'label': label
    }

def encodeSpec(obj, format='png16'):
    print(type(obj))
    if isinstance(obj, NMRSpectrum1D):
        ret =  encode1DSpec(obj,format)
    elif isinstance(obj, NMRSpectrum2D):
        ret = encode2DSpec(obj,format)
    
    ret['data_type'] = 'spectrum'
    return ret



def encodeSpecFeature(obj):
    ret = obj.data
    ret['s_id'] = obj.spec.__s_id__
    ret['data_type'] = 'spec_feature'
    return ret

def encodeSpecLike(obj, format='png16'):   
    ret['data'] = encode1DArrayAsPNG(obj.data, format)
    
    ret['s_id'] = - obj.spec.__s_id__
    ret['data_type'] = 'spec_like'
    return ret


# Custom Json encoder
class SpecEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return(obj.astype(np.int64).tolist())
        
        if isinstance(obj, SpecFeature):
            return encodeSpecFeature(obj)
            
        if isinstance(obj, SpecLike):
            return encodeSpecFeature(obj)
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


# Formats NMRSpectrum class as PNG
class pngSpecEncoder(SpecEncoder):
    def default(self, obj):
        print(type(obj), NMRSpectrum2D)
        if isinstance(obj, DataUdic): #TODO:DataUdic or NMRSpectrum?!
            return encodeSpec(obj, format='png')
        return SpecEncoder.default(self, obj)

class png16SpecEncoder(SpecEncoder):
    def default(self, obj):
        if isinstance(obj, DataUdic): #TODO:DataUdic or NMRSpectrum?!
            return encodeSpec(obj, format='png16')
        return SpecEncoder.default(self, obj)
