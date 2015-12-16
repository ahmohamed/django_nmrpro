import unittest
import nmrglue as ng
from .classes.NMRSpectrum import NMRSpectrum
from .session import registerSpecs, getSessionSpec
import pickle
import numpy.testing as ts

class SessionMock(dict):
    def __init__(self):
        self.modified = True
        
class SessionSeriallizationTest(unittest.TestCase):
    def setUp(self):
        self.spec1 = NMRSpectrum.fromBruker("./nmr/test_files/Bruker_1D/")
        self.spec2 = NMRSpectrum.fromBruker("./nmr/test_files/Bruker_1D/")
        self.spec3 = NMRSpectrum.fromBruker("./nmr/test_files/Bruker_1D/")
    
    def test_dill_session(self):
        session_dict = SessionMock()
        session_dict['key'] = 'value'
        registerSpecs(session_dict, [self.spec1, self.spec2, self.spec3])
        
        from_pickle = pickle.loads(pickle.dumps(session_dict))
        self.assertEqual(len(session_dict['specs']), 3, 
                         'Pickled spec list has incorrect length')
        
        unpickled_spec1 = getSessionSpec(from_pickle,0)
        ts.assert_array_equal(self.spec1, unpickled_spec1,
                              'Unpickled spec doesnt match original')
        
        
        hist_vals = self.spec1.history.values()
        rets = [hist_vals[0](None)]
        for i in range(1, len(hist_vals)):
            rets.append(hist_vals[i](rets[-1]))
            
        hist_vals = unpickled_spec1.history.values()
        unpickled_rets = [hist_vals[0](None)]
        for i in range(1, len(hist_vals)):
            unpickled_rets.append(hist_vals[i](unpickled_rets[-1]))
        
        ts.assert_array_equal(self.spec1, rets[-1],
                         'Excuting history functions doesnt yield final spec')
        ts.assert_array_equal(unpickled_spec1, unpickled_rets[-1],
                         'Excuting pickled history functions doesnt yield final spec')
        for i in range(0, len(rets)):
            ts.assert_array_equal(
                rets[i], unpickled_rets[i],
                'Unpickled functions doesnt have the same return as the original'
            )