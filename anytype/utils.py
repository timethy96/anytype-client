import re
import keyword
from functools import wraps


def sanitize_property_name(name: str) -> str:
    """
    Sanitizes a property name to be a valid Python attribute name.
    - Converts to lowercase
    - Replaces all non-alphanumeric characters with underscores
    - Ensures the name doesn't start with a number
    - Ensures the name isn't a Python keyword
    """
    # Convert to lowercase and replace non-alphanumeric chars with underscore
    sanitized = re.sub(r'[^a-z0-9_]', '_', name.lower())
    
    # Remove leading numbers by adding underscore
    if sanitized and (sanitized[0].isdigit() or keyword.iskeyword(sanitized)):
        sanitized = '_' + sanitized
        
    return sanitized


def requires_auth(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self._apiEndpoints is None:
            raise Exception("You need to auth first")
        return method(self, *args, **kwargs)

    return wrapper


from enum import Enum


class PropertyFormat(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    FILES = "files"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    OBJECTS = "objects"


_ANYTYPE_PROPERTIES_COLORS = (
    "grey",
    "yellow",
    "orange",
    "red",
    "pink",
    "purple",
    "blue",
    "ice",
    "teal",
    "lime",
)

_ANYTYPE_SYSTEM_RELATIONS = (
    "id",
    "name",
    "description",
    "snippet",
    "iconEmoji",
    "iconImage",
    "type",
    "layout",
    "layoutAlign",
    "coverId",
    "coverScale",
    "coverType",
    "coverX",
    "coverY",
    "createdDate",
    "creator",
    "lastModifiedDate",
    "lastModifiedBy",
    "lastOpenedDate",
    "featuredRelations",
    "isFavorite",
    "workspaceId",
    "spaceId",
    "links",
    "internalFlags",
    "restrictions",
    "addedDate",
    "source",
    "sourceObject",
    "setOf",
    "relationFormat",
    "relationKey",
    "relationReadonlyValue",
    "relationDefaultValue",
    "relationMaxCount",
    "relationOptionColor",
    "relationFormatObjectTypes",
    "isReadonly",
    "isDeleted",
    "isHidden",
    "spaceShareableStatus",
    "isAclShared",
    "isHiddenDiscovery",
    "done",
    "isArchived",
    "templateIsBundled",
    "smartblockTypes",
    "targetObjectType",
    "recommendedLayout",
    "fileExt",
    "fileMimeType",
    "sizeInBytes",
    "oldAnytypeID",
    "spaceDashboardId",
    "recommendedRelations",
    "iconOption",
    "widthInPixels",
    "heightInPixels",
    "fileExt",
    "sizeInBytes",
    "sourceFilePath",
    "fileSyncStatus",
    "defaultTemplateId",
    "uniqueKey",
    "backlinks",
    "profileOwnerIdentity",
    "fileBackupStatus",
    "fileId",
    "fileIndexingStatus",
    "origin",
    "revision",
    "imageKind",
    "importType",
    "spaceAccessType",
    "spaceInviteFileCid",
    "spaceInviteFileKey",
    "readersLimit",
    "writersLimit",
    "sharedSpacesLimit",
    "participantPermissions",
    "participantStatus",
    "latestAclHeadId",
    "identity",
    "globalName",
    "syncDate",
    "syncStatus",
    "syncError",
    "lastUsedDate",
    "mentions",
    "chatId",
    "hasChat",
    "timestamp",
    "iconName",
    "recommendedFeaturedRelations",
    "recommendedHiddenRelations",
    "recommendedFileRelations",
    "layoutWidth",
    "defaultViewType",
    "defaultTypeId",
    "resolvedLayout",
    "pluralName",
)
