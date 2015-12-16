import unittest
import nmrglue as ng
from nmrpro.classes.NMRSpectrum import NMRSpectrum
import numpy.testing as ts
from numpy import asarray
from json import dumps, loads
from .encoder import pngSpecEncoder
from PIL import Image
from io import BytesIO

class pngEncoder_1DTest(unittest.TestCase):
    def setUp(self):
        self.spec1d = NMRSpectrum.fromBruker("./nmr/test_files/Bruker_1D/")
        
    
    def test_encoder_8bits(self):
        spec1d = self.spec1d
        json_1d = dumps(self.spec1d, cls=pngSpecEncoder)
        
        
        parsed_json = loads(json_1d)
        assert parsed_json['bits'] == 8
        assert parsed_json['format'] == 'png'
        assert parsed_json['nd'] == 1
        ts.assert_allclose(parsed_json['x_domain'], spec1d.uc[0].ppm_limits() , 1e-7,0, 'x_domain is incorrect') 
        ts.assert_allclose(parsed_json['y_domain'], [spec1d.real.min(), spec1d.real.max()] , 1e-7,0, 'y_domain is incorrect')
        
        # Decode the base64 png and get pixel data
        decoded_png = parsed_json['data'].decode('base64')
        img_data = BytesIO()
        img_data.write(decoded_png)
        img_data.flush()
        img_data.seek(0)
        img = Image.open(img_data)
        img_arr = asarray(list(img.getdata()))
        
        # Check image shape
        ts.assert_equal(img_arr.shape, spec1d.shape, 'image shape doesnt match spectrum')
        
        # Check data resolution
        y_domain = asarray(parsed_json['y_domain'])
        resolution = y_domain.ptp() / (2**8-1)
        scaled = (img_arr * resolution)+y_domain[0]

        ts.assert_equal( sum(spec1d-scaled > resolution), 0, 'Some scaled points are diviated from the sepctrum by more than accepted resolution')


class pngEncoder_2DTest(unittest.TestCase):
    def setUp(self):
        self.spec2d = NMRSpectrum.fromPipe("./nmr/test_files/Pipe_2D/tocsy.ft2")
        
    
    def test_encoder_8bits(self):
        spec2d = self.spec2d
        json_2d = dumps(self.spec2d, cls=pngSpecEncoder)
        
        
        parsed_json = loads(json_2d)
        assert parsed_json['bits'] == 8
        assert parsed_json['format'] == 'png'
        assert parsed_json['nd'] == 2
        ts.assert_allclose(parsed_json['x_domain'], spec2d.uc[1].ppm_limits() , 1e-7,0, 'x_domain is incorrect') 
        ts.assert_allclose(parsed_json['y_domain'], spec2d.uc[0].ppm_limits() , 1e-7,0, 'y_domain is incorrect') 
        
        # Decode the base64 png and get pixel data
        decoded_png = parsed_json['data'].decode('base64')
        img_data = BytesIO()
        img_data.write(decoded_png)
        img_data.flush()
        img_data.seek(0)
        img = Image.open(img_data)
        img_arr = asarray(img)
        
        # transpose spec2d similar to the encoder
        spec2d = spec2d[::-1]
        
        # Check image shape
        ts.assert_equal(img_arr.shape, spec2d.shape, 'image shape doesnt match spectrum')
        
        # Check data resolution
        z_domain = asarray(parsed_json['z_domain'])
        resolution = z_domain.ptp() / (2**8-1)
        print('resolution', z_domain, resolution)
        scaled = (img_arr * resolution) + z_domain[0]
        print(scaled.shape, spec2d.shape)
        print(sum(spec2d-scaled > resolution))
        
        ts.assert_equal( sum( spec2d.real_part() -scaled > resolution), 0, 'Some scaled points are diviated from the sepctrum by more than accepted resolution')
        
                
