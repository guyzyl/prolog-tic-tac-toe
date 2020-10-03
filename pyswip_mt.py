"""
A solution for running Prolog in a multithreaded environment (Flask in our case).
Based on https://github.com/yuce/pyswip/issues/3#issuecomment-355458825
"""
import ctypes
import pyswip

class PrologMT(pyswip.Prolog):
    """
    Multi-threaded (one-to-one) pyswip.Prolog ad-hoc reimpl
    """
    _swipl = pyswip.core._lib

    PL_thread_self = _swipl.PL_thread_self
    PL_thread_self.restype = ctypes.c_int

    PL_thread_attach_engine = _swipl.PL_thread_attach_engine
    PL_thread_attach_engine.argtypes = [ctypes.c_void_p]
    PL_thread_attach_engine.restype = ctypes.c_int

    @classmethod
    def _init_prolog_thread(cls):
        pengine_id = cls.PL_thread_self()
        if (pengine_id == -1):
            pengine_id = cls.PL_thread_attach_engine(None)
        if (pengine_id == -1):
            raise pyswip.prolog.PrologError("Unable to attach new Prolog engine to the thread")

    class _QueryWrapper(pyswip.Prolog._QueryWrapper):
        def __call__(self, *args, **kwargs):
            PrologMT._init_prolog_thread()
            return super().__call__(*args, **kwargs)
