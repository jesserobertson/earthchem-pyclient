from . import documentation, query, validation, transform, geochem, plot

from .query import Query

# Versioneer imports
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
