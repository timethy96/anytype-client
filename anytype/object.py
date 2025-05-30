import re

from .type import Type
from .icon import Icon
from .property import Property
from .api import apiEndpoints, APIWrapper
from .utils import requires_auth, _ANYTYPE_SYSTEM_RELATIONS, sanitize_property_name


class Object(APIWrapper):
    """
    Represents an object within a specific space, allowing creation and manipulation of its properties. The object can be customized with various attributes such as `name`, `icon`, `body`, `description`, and more. This class provides methods to export objects and add different content types to the object body, such as titles, text, code blocks, checkboxes, and bullet points.

    ### IMPORTANT

    Certain properties of an object, such as:

    - `DOI` in a collection of articles;
    - `Release Year` in albums;
    - `Genre` in music collections;
    - `Author` in book collections;
    - `Publication Date` in documents;
    - `Rating` in review-based objects;
    - `Tags` in categorized objects;

    are accessible through the class properties. For example, if an object is created with a `Type` (e.g., `anytype.Type`) that includes a `DOI` property, the DOI URL can be set during the object creation using `Object.doi`.

    Note that these property names are derived from the corresponding name in the Anytype GUI. They are all lowercase with spaces replaced by underscores. For instance, a property called `Release Year` in the Anytype GUI will be accessed as `release_year` in the object, and a property called `Publication Date` will be accessed as `publication_date`.

    """

    def __init__(self, name: str = "", type: Type | None = None):
        self._apiEndpoints: apiEndpoints | None = None
        self._icon: Icon = Icon()
        self._values = {}

        self.id: str = ""
        self.source: str = ""
        self.name: str = name
        self.body: str = ""
        self.description: str = ""
        self.details = []
        self.layout: str = "basic"

        self.properties: list[Property] = []
        if type is not None:
            for prop in type.properties:
                if prop.key not in _ANYTYPE_SYSTEM_RELATIONS:
                    self.properties.append(prop)

        self.root_id: str = ""
        self.space_id: str = ""
        self.template_id: str = ""

        self.snippet: str = ""
        self.type_key: str = ""

        self._custom_setters = {}
        self._custom_getters = {}
        self._values = {}
        notoverdrive = ("icon", "type")

        if type is not None:
            self.type = type
            for prop in self.properties:
                class_prop = sanitize_property_name(prop.name)
                if class_prop in notoverdrive:
                    continue

                def setter(prop, value):
                    prop.__setattr__(prop.format, value)

                def getter(name, prop):
                    return prop.__getattr__(prop.format, name)

                self._custom_setters[class_prop] = {"prop": class_prop, "func": setter}
                self._custom_getters[class_prop] = {"prop": prop, "func": getter}

    def __setattr__(self, name, value):
        if "_custom_setters" in self.__dict__ and name in self._custom_setters:
            for prop in self.properties:
                class_prop = sanitize_property_name(prop.name)
                if class_prop == name:
                    self._custom_setters[name]["func"](prop, value)
                    return
            raise AttributeError(f"Attribute {name} not found")
        elif hasattr(type(self), name):
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if "_custom_getters" in self.__dict__ and name in self._custom_getters:
            prop = self._custom_getters[name]["prop"]
            return self._custom_getters[name]["func"](name, prop)
        elif hasattr(type(self), name):
            return getattr(self, name)
        else:
            try:
                return self.__dict__[name]
            except KeyError:
                raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, dict):
            self._type = Type._from_api(self._apiEndpoints, value | {"space_id": self.space_id})
        elif isinstance(value, Type):
            self._type = value
        else:
            raise Exception("Invalid type")

    @type.getter
    def type(self):
        return self._type

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        if isinstance(value, dict):
            new_icon = Icon()
            new_icon._update_with_json(value)
            self._icon = new_icon
        elif isinstance(value, str):
            emoji_pattern = re.compile(
                "[\U0001f600-\U0001f64f"
                "\U0001f300-\U0001f5ff"
                "\U0001f680-\U0001f6ff"
                "\U0001f1e0-\U0001f1ff"
                "\U00002702-\U000027b0"
                "\U000024c2-\U0001f251"
                "]+",
                flags=re.UNICODE,
            )
            if bool(emoji_pattern.fullmatch(value)):
                self._icon.emoji = value
            else:
                raise Exception("Invalid icon format")
        elif isinstance(value, Icon):
            self._icon = value
        else:
            raise Exception("Invalid icon format")

    @icon.getter
    def icon(self):
        return self._icon

    def add_type(self, type: Type):
        """
        Adds a type for an Object.

        Parameters:
            type (anytype.Type): Type from the space retrieved using `space.get_types()[0]`, `space.get_type(type)`, `space.get_type_byname("Articles")`

        Returns:
            None

        """
        self.template_id = type.template_id
        self.type_key = type.key

    def add_title1(self, text) -> None:
        """
        Adds a level 1 title to the object's body.

        Parameters:
            text (str): The text to be added as a level 1 title.

        Returns:
            None
        """
        self.body += f"# {text}\n"

    def add_title2(self, text) -> None:
        """
        Adds a level 2 title to the object's body.

        Parameters:
            text (str): The text to be added as a level 2 title.

        Returns:
            None
        """
        self.body += f"## {text}\n"

    def add_title3(self, text) -> None:
        """
        Adds a level 3 title to the object's body.

        Parameters:
            text (str): The text to be added as a level 3 title.

        Returns:
            None
        """
        self.body += f"### {text}\n"

    def add_text(self, text) -> None:
        """
        Adds plain text to the object's body.

        Parameters:
            text (str): The text to be added.

        Returns:
            None
        """
        self.body += f"{text}\n"

    def add_codeblock(self, code, language=""):
        """
        Adds a code block to the object's body.

        Parameters:
            code (str): The code to be added.
            language (str, optional): The programming language of the code block. Default is an empty string.

        Returns:
            None
        """
        self.body += f"``` {language}\n{code}\n```\n"

    def add_bullet(self, text) -> None:
        """
        Adds a bullet point to the object's body.

        Parameters:
            text (str): The text to be added as a bullet point.

        Returns:
            None
        """
        self.body += f"- {text}\n"

    def add_checkbox(self, text, checked=False) -> None:
        """
        Adds a checkbox to the object's body.

        Parameters:
            text (str): The text to be added next to the checkbox.
            checked (bool, optional): Whether the checkbox is checked. Default is False.

        Returns:
            None
        """
        self.body += f"- [x] {text}\n" if checked else f"- [ ] {text}\n"

    def add_image(self, image_url: str, alt: str = "", title: str = "") -> None:
        """
        Adds an image to the object's body.

        Parameters:
            image_url (str): The URL of the image.
            alt (str, optional): The alternative text for the image. Default is an empty string.
            title (str, optional): The title of the image. Default is an empty string.

        Returns:
            None
        """
        if title:
            self.body += f'![{alt}]({image_url} "{title}")\n'
        else:
            self.body += f"![{alt}]({image_url})\n"

    def __repr__(self):
        if self.type:
            if self.type.name != "":
                return f"<Object(name={self.name}, type={self.type.name})>"
            else:
                return f"<Object(name={self.name})>"
        else:
            return f"<Object(name={self.name})>"
