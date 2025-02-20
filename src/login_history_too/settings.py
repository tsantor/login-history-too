"""
Settings for Login History Too are all namespaced in the
LOGIN_HISTORY_TOO setting. For example your project's
`settings.py` file might look like this:

LOGIN_HISTORY_TOO = {
    "GEOLOCATION_METHOD": "login_history_too.utils.get_ip_info"
}

This module provides the `api_settings` object, that is used to access
Login History Too settings, checking for user settings first,
then falling back to the defaults.
"""

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    "GEOLOCATION_METHOD": "login_history_too.utils.get_ip_info",
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    "GEOLOCATION_METHOD",  # example only as it will be imported as a class
]


# List of settings that have been removed
REMOVED_SETTINGS = []

SETTINGS_DOC = "TODO"  # TODO: Add link to documentation


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    if isinstance(val, str):
        return import_from_string(val, setting_name)
    if isinstance(val, (list, tuple)):  # noqa: UP038
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = f"Could not import '{val}' for API setting '{setting_name}'. {e.__class__.__name__}: {e}."
        raise ImportError(msg) from e


class APISettings:
    """
    A settings object that allows Login History Too settings to be
    accessed as properties. For example:

        from login_history_too.settings import api_settings
        print(api_settings.GEOLOCATION_METHOD)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.

    Note:
    This is an internal class that is only compatible with settings namespaced
    under the LOGIN_HISTORY_TOO name. It is not intended to be used by
    3rd-party apps, and test helpers like `override_settings` may not work as
    expected.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "LOGIN_HISTORY_TOO", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                msg = f"The '{setting}' setting has been removed. Please refer to '{SETTINGS_DOC}' for available settings."
                raise RuntimeError(msg)
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "LOGIN_HISTORY_TOO":
        api_settings.reload()


setting_changed.connect(reload_api_settings)
