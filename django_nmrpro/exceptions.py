from nmrpro.exceptions import SpecError

class PluginNotFoundError(SpecError):
    '''Raised when an unavailbale plugin is requested'''

class SessionError(SpecError):
    '''Raised when session data is unavailable'''
