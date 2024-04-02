import dataclasses

import marshmallow

import minervapy.utils
import minervapy.session

_configuration_url = "configuration/"
_options_url = "configuration/options/"


@dataclasses.dataclass
class MiriamType:
    commonName: str | None = None
    homepage: str | None = None
    registryIdentifier: str | None = None
    uris: list[str] = dataclasses.field(
        default_factory=list
    )  # also labeled registryIdentifier in the docs


@dataclasses.dataclass
class Parameter:
    annotation_type: str | None = (
        None  # doc says MiriamType but seems to be str
    )
    field: str | None = None
    commonName: str | None = None
    description: str | None = None
    inputType: str | None = None
    name: str | None = None
    value: str | None = None
    order: float | None = None
    type: str | None = None


@dataclasses.dataclass
class Annotator:
    name: str | None = None
    url: str | None = None
    className: str | None = None
    elementClassNames: list[str] = dataclasses.field(default_factory=list)
    description: str | None = None
    parameters: list[Parameter] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class BioEntityField:
    commonName: str | None = None
    name: str | None = None


@dataclasses.dataclass
class ElementType:
    className: str | None = None
    name: str | None = None
    parentClass: str | None = None


@dataclasses.dataclass
class ImageFormat:
    extension: str | None = None
    name: str | None = None
    handler: str | None = None


@dataclasses.dataclass
class MapCanvasType:
    id: str | None = None
    name: str | None = None


@dataclasses.dataclass
class MapType:
    id: str | None = None
    name: str | None = None


@dataclasses.dataclass
class ModelFormat:
    extension: str | None = None
    extensions: list[str] = dataclasses.field(
        default_factory=list
    )  # not in the doc
    name: str | None = None
    handler: str | None = None


@dataclasses.dataclass
class MofidicationStateType:
    commonName: str | None = None
    abbreviation: str | None = None


@dataclasses.dataclass
class Option:
    idObject: int | None = None
    commonName: str | None = None
    group: str | None = None
    isServerSide: bool | None = None
    type: str | None = None
    value: str | None = None
    valueType: str | None = None


@dataclasses.dataclass
class OverlayType:
    name: str | None = None


@dataclasses.dataclass
class PrivilegeType:
    commonName: str | None = None
    objectType: str | None = None
    valueType: str | None = None


@dataclasses.dataclass
class ReactionType:
    className: str | None = None
    name: str | None = None
    parentClass: str | None = None


@dataclasses.dataclass
class UnitType:
    name: str | None = None
    id: str | None = None


@dataclasses.dataclass
class Configuration:
    annotators: list[Annotator] = dataclasses.field(default_factory=list)
    bioEntityFields: list[BioEntityField] = dataclasses.field(
        default_factory=list
    )
    buildDate: str | None = None
    gitHash: str | None = None
    version: str | None = None
    imageFormats: list[ImageFormat] = dataclasses.field(default_factory=list)
    mapCanvasTypes: list[MapCanvasType] = dataclasses.field(
        default_factory=list
    )
    mapTypes: list[MapType] = dataclasses.field(default_factory=list)
    miriamTypes: dict[str, MiriamType] = dataclasses.field(default_factory=dict)
    modelFormats: list[ModelFormat] = dataclasses.field(default_factory=list)
    modificationStateTypes: dict[str, MofidicationStateType] = (
        dataclasses.field(default_factory=list)
    )
    options: list[Option] = dataclasses.field(default_factory=list)
    overlayTypes: list[OverlayType] = dataclasses.field(default_factory=list)
    privilegeTypes: dict[str, PrivilegeType] = dataclasses.field(
        default_factory=dict
    )
    reactionTypes: list[ReactionType] = dataclasses.field(default_factory=list)
    unitTypes: list[UnitType] = dataclasses.field(default_factory=list)
    elementTypes: list[ElementType] = dataclasses.field(default_factory=list)

    def get_option(self, option_type):
        for option in self.options:
            if option.type == option_type:
                return option
        return None

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Configuration(**data)


class _MiriamTypeSchema(marshmallow.Schema):
    commonName = marshmallow.fields.String(required=False, allow_none=True)
    homepage = marshmallow.fields.String(required=False, allow_none=True)
    registryIdentifier = marshmallow.fields.String(
        required=False, allow_none=True
    )
    uris = marshmallow.fields.List(
        marshmallow.fields.String(), required=False, allow_none=True
    )  # also labeled registryIdentifier in the docs

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return MiriamType(**data)


class _ParameterSchema(marshmallow.Schema):
    annotation_type = marshmallow.fields.String(
        required=False, allow_none=True
    )  # doc says MiriamType but seems to be str
    field = marshmallow.fields.String(required=False, allow_none=True)
    commonName = marshmallow.fields.String(required=False, allow_none=True)
    description = marshmallow.fields.String(required=False, allow_none=True)
    inputType = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)
    value = marshmallow.fields.String(required=False, allow_none=True)
    order = marshmallow.fields.Float(required=False, allow_none=True)
    type = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Parameter(**data)


class _AnnotatorSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=False, allow_none=True)
    url = marshmallow.fields.String(required=False, allow_none=True)
    className = marshmallow.fields.String(required=False, allow_none=True)
    elementClassNames = marshmallow.fields.List(
        marshmallow.fields.String(), required=False, allow_none=True
    )
    description = marshmallow.fields.String(required=False, allow_none=True)
    parameters = marshmallow.fields.List(
        marshmallow.fields.Nested(_ParameterSchema),
        required=False,
        allow_none=True,
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Annotator(**data)


class _BioEntityFieldSchema(marshmallow.Schema):
    commonName = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return BioEntityField(**data)


class _ElementTypeSchema(marshmallow.Schema):
    className = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)
    parentClass = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return ElementType(**data)


class _ImageFormatSchema(marshmallow.Schema):
    extension = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)
    handler = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return ImageFormat(**data)


class _MapCanvasTypeSchema(marshmallow.Schema):
    id = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return MapCanvasType(**data)


class _MapTypeSchema(marshmallow.Schema):
    id = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return MapType(**data)


class _ModelFormatSchema(marshmallow.Schema):
    extension = marshmallow.fields.String(required=False, allow_none=True)
    extensions = marshmallow.fields.List(
        marshmallow.fields.String(), required=False, allow_none=True
    )  # not in the doc
    name = marshmallow.fields.String(required=False, allow_none=True)
    handler = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return ModelFormat(**data)


class _MofidicationStateTypeSchema(marshmallow.Schema):
    commonName = marshmallow.fields.String(required=False, allow_none=True)
    abbreviation = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return MofidicationStateType(**data)


class _OptionSchema(marshmallow.Schema):
    idObject = marshmallow.fields.Int(
        required=False, allow_none=True
    )  # not in the doc
    commonName = marshmallow.fields.String(required=False, allow_none=True)
    group = marshmallow.fields.String(required=False, allow_none=True)
    isServerSide = marshmallow.fields.Boolean(required=False, allow_none=True)
    type = marshmallow.fields.String(required=False, allow_none=True)
    value = marshmallow.fields.String(required=False, allow_none=True)
    valueType = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Option(**data)


class _OverlayTypeSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return OverlayType(**data)


class _PrivilegeTypeSchema(marshmallow.Schema):
    commonName = marshmallow.fields.String(required=False, allow_none=True)
    objectType = marshmallow.fields.String(required=False, allow_none=True)
    valueType = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return PrivilegeType(**data)


class _ReactionTypeSchema(marshmallow.Schema):
    className = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)
    parentClass = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return ReactionType(**data)


class _UnitTypeSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=False, allow_none=True)
    id = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return UnitType(**data)


class _ConfigurationSchema(marshmallow.Schema):
    annotators = marshmallow.fields.List(
        marshmallow.fields.Nested(_AnnotatorSchema),
        required=False,
        allow_none=True,
    )
    bioEntityFields = marshmallow.fields.List(
        marshmallow.fields.Nested(_BioEntityFieldSchema),
        required=False,
        allow_none=True,
    )
    buildDate = marshmallow.fields.String(
        required=False, allow_none=True
    )  # timestamp in the doc
    gitHash = marshmallow.fields.String(
        required=False, allow_none=True
    )  # timestamp in the doc
    version = marshmallow.fields.String(required=False, allow_none=True)
    imageFormats = marshmallow.fields.List(
        marshmallow.fields.Nested(_ImageFormatSchema),
        required=False,
        allow_none=True,
    )
    mapCanvasTypes = marshmallow.fields.List(
        marshmallow.fields.Nested(_MapCanvasTypeSchema),
        required=False,
        allow_none=True,
    )
    mapTypes = marshmallow.fields.List(
        marshmallow.fields.Nested(_MapTypeSchema),
        required=False,
        allow_none=True,
    )
    miriamTypes = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(),
        values=marshmallow.fields.Nested(_MiriamTypeSchema),
        required=False,
        allow_none=True,
    )
    modelFormats = marshmallow.fields.List(
        marshmallow.fields.Nested(_ModelFormatSchema),
        required=False,
        allow_none=True,
    )
    modificationStateTypes = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(),
        values=marshmallow.fields.Nested(_MofidicationStateTypeSchema),
        required=False,
        allow_none=True,
    )
    options = marshmallow.fields.List(
        marshmallow.fields.Nested(_OptionSchema),
        required=False,
        allow_none=True,
    )
    overlayTypes = marshmallow.fields.List(
        marshmallow.fields.Nested(_OverlayTypeSchema),
        required=False,
        allow_none=True,
    )
    privilegeTypes = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(required=False, allow_none=True),
        values=marshmallow.fields.Nested(_PrivilegeTypeSchema),
        required=False,
        allow_none=True,
    )
    reactionTypes = marshmallow.fields.List(
        marshmallow.fields.Nested(_ReactionTypeSchema),
        required=False,
        allow_none=True,
    )
    unitTypes = marshmallow.fields.List(
        marshmallow.fields.Nested(_UnitTypeSchema),
        required=False,
        allow_none=True,
    )
    elementTypes = marshmallow.fields.List(
        marshmallow.fields.Nested(_ElementTypeSchema),
        required=False,
        allow_none=True,
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Configuration(**data)


def get_configuration():
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _configuration_url]
    )
    configuration = minervapy.utils.get_objects(url, _ConfigurationSchema)
    return configuration


def get_options():
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _options_url]
    )
    options = minervapy.utils.get_objects(url, _OptionSchema, many=True)
    return options
