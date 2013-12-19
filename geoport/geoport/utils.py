# Project-wide utility functions
from bson import json_util
from django.utils.encoding import smart_unicode
from slugify import slugify as pyslugify


class JSONSerializer(object):
    """
    Simple wrapper around json to be used in signing.dumps and
    signing.loads.
    """
    def dumps(self, obj):
        return json_util.dumps(obj, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        return json_util.loads(data.decode('latin-1'))


def slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0,
            word_boundary=False, separator='-'):
    """ Make a slug from a given text """
    return smart_unicode(pyslugify(text, entities, decimal, hexadecimal,
                                   max_length, word_boundary, separator))


# uuslug adaptation to MongoEngine documents
def uuslug(s, instance, entities=True, decimal=True, hexadecimal=True,
           slug_field='slug', filter_dict=None, start_no=1, max_length=0,
           word_boundary=False, separator='-'):

    queryset = instance.__class__.objects.all()
    if filter_dict:
        queryset = queryset.filter(**filter_dict)
    if instance.id:
        queryset = queryset(id__ne=instance.id)

    slug = slugify(s, entities=entities, decimal=decimal,
                   hexadecimal=hexadecimal, max_length=max_length,
                   word_boundary=word_boundary, separator=separator)

    new_slug = slug
    counter = start_no
    while queryset.filter(**{slug_field: new_slug}):
        if max_length > 0:
            if len(slug) + len(separator) + len(str(counter)) > max_length:
                r = max_length - len(slug) - len(separator) - len(str(counter))
                slug = slug[:r]  # make room for the "-1, -2 ... etc"
        new_slug = "%s%s%s" % (slug, separator, counter)
        counter += 1

    return new_slug


def get_post_data(request, *fields):
    data = {}
    for field in fields:
        data[field] = request.POST.get(field)
    return data


def get_initial_data(instance, *fields):
    data = {}
    for field in fields:
        value = getattr(instance, field, '')
        if value is None:
            data[field] = ''
        else:
            data[field] = value
    print data
    return data
