import random
import string

from django.conf import settings
from django.utils.translation import get_language


def swap_pid_prefix(pid, new_prefix, delimiter='_'):
    new_string = pid.split(delimiter)
    new_string[0] = new_prefix
    new_id = delimiter.join(new_string)
    return new_id


def id_generator(n=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def get_active_lang():
    language = get_language()
    if not language:
        language = settings.LANGUAGE_CODE
    return language.split('-')[0]


def switch_lang_code(path_, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    if path_ == '':
        raise Exception('URL path for language switch is empty')
    elif path_[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)

    parts = path_.split('/')
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = '/' + language
    return '/'.join(parts)
