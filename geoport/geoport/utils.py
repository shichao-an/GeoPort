from bson import json_util


class JSONSerializer(object):
    """
    Simple wrapper around json to be used in signing.dumps and
    signing.loads.
    """
    def dumps(self, obj):
        return json_util.dumps(obj, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        return json_util.loads(data.decode('latin-1'))
