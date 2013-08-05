"""import os, sys
import pymongo

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    _tmp = __import__(module[:-3], locals(), globals())
    for cls in [getattr(_tmp,x) for x in dir(_tmp) if isinstance(getattr(_tmp,x), type)] :
        setattr(sys.modules[__name__], cls.__name__, cls)    
del module"""

from admin_controller import AdminController
from ctype_controller import CTypeController
from ctask_controller import CTaskController

