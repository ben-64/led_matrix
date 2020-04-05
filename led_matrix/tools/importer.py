import sys
import os
import pkgutil


def import_module_to_globals(mod,globals_var,cond=None):
    for k,v in mod.__dict__.items():
        if not k.startswith("__"):
            try:
                if cond and cond(mod.__dict__[k]):
                    globals_var[k] = mod.__dict__[k]
            except:
                pass


def add_classes_to_globals(path,prefix,cond=None):
    folder = os.path.dirname(path)
    module = sys.modules[prefix]
    def f(globals_var=globals()):
        for importer, name, _ in pkgutil.iter_modules([folder]):
            absname = prefix+"."+name
            if absname in sys.modules:
                mod = sys.modules[absname]
            else:
                loader = importer.find_module(absname)
                try:
                    mod = loader.load_module(absname)
                except ImportError as e:
                    mod = None
            if mod:
                import_module_to_globals(mod,globals_var,cond)
    return f
