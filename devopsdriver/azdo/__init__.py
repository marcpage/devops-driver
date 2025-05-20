"""initialize azure module"""

# re export symbols for easier use
from .azureobject import AzureObject
from .clients import Azure
from .timestamp import Timestamp

from .workitem.wiql import Wiql, Value, Field
from .workitem.wiql import Ascending, Descending, And, Or, In, NotIn
from .workitem.wiql import Equal, NotEqual, LessThanOrEqual, GreaterThanOrEqual
from .workitem.wiql import IsEmpty, IsNotEmpty, LessThan, GreaterThan
