import importlib


def import_as_mapping(modname: str) -> dict[str, type]:
    mod = importlib.import_module(modname)
    if hasattr(mod, "__all__"):
        names = list(mod.__all__)
    else:
        names = [n for n in dir(mod) if not n.startswith("_")]
    return {n: getattr(mod, n) for n in names if hasattr(mod, n)}
