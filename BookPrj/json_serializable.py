import json
import flask
from collections import OrderedDict
from datetime import datetime
from models.database import Base


class JSONEncoder(json.JSONEncoder):

    def default(self, o):

        def recursive(p):
            result = OrderedDict()
            for k in p.keys():
                result[k] = getattr(o, k)

                if isinstance(result[k], dict):
                    result[k] = recursive(result[k])
                if isinstance(result[k], datetime):
                    result[k] = result[k].timestamp()

            return result

        if isinstance(o, Base):
            return dict(recursive(o.__mapper__.c))

        return flask.json.JSONEncoder.default(self, o)


def JSONSerializable(app=None, **kwargs):
    if app is not None:
        app.json_encoder = JSONEncoder