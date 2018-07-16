from lumr_web import config_default


def marge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = marge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


class Dict(dict):
    def __init__(self, name=(), value=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(name, value):
            self[k] = v

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % item)

    def __setattr__(self, key, value):
        self[key] = value


def toDict(db):
    d = Dict()
    for k, v in db.items():
        d[k] = toDict(v) if isinstance(v, dict) else v
    return d

# config = config_default.configs
#
# try:
#     import config_override
#
#     config = marge(config, config_override.configs)
# except ImportError:
#     pass
#
# config = toDict(config)
