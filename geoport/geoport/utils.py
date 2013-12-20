# Project-wide utility functions
from bson import json_util
import os
import uuid
import random
import requests
from slugify import slugify as pyslugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
from django.forms.util import ErrorList


GEOCODING_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


class DivErrorList(ErrorList):

    def __unicode__(self):
        return mark_safe(self.as_divs())

    def as_divs(self):
        if not self:
            return u''
        divs = [u'<div class="error">%s</div>' % e for e in self]
        return u'<div class="errorlist">%s</div>' % ''.join(divs)


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


def generate_file_path(filename, category):
    """
    Generate hashed upload path similar to MediaWiki, though the filename is
    UUID instead of original one

    The result is something like this:
        avatars/5/d/5a754a6da92440f0b314edfcbad0bd5e.jpg

    """
    random_name = uuid.uuid4().hex
    directory, subdirectory = get_hashed_directories()
    extension = os.path.splitext(filename)[-1]
    fn = random_name + extension
    return os.path.join(category, directory, subdirectory, fn)


def get_hashed_directories():
    directory = hex(random.randint(1, 15)).lstrip('0x')
    subdirectory = hex(random.randint(1, 31)).lstrip('0x')
    return directory, subdirectory


def handle_uploaded_file(f, category, filename=None):
    """Universal function for handling uploaded file using `default_storage'"""
    path = None
    if hasattr(f, 'name'):
        path = generate_file_path(f.name, category)
        default_storage.save(path, f)
    elif not hasattr(f, 'name') and filename:
        path = generate_file_path(filename, category)
        default_storage.save(path, ContentFile(f))
    assert path is not None
    return path


def delete_file(path):
    default_storage.delete(path)


def get_location_by_address(address, sensor=True):
    """Get location by address (string) using Google Geocoding
    Return a 2-tuple of coordinates (latitude, longitude)
    """
    params = {}
    params['sensor'] = 'true' if sensor else 'false'
    params['address'] = address.encode('utf-8')
    res = requests.get(GEOCODING_URL, params=params).json()
    try:
        lat = res['results'][0]['geometry']['location']['lat']
        lng = res['results'][0]['geometry']['location']['lng']
        return lat, lng
    except:
        return None
