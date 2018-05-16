from . import documentation, query

from .query import RESTClientQuery as Query

# Versioneer imports
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
