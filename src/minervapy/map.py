import dataclasses

import marshmallow

import minervapy.utils
import minervapy.session
import minervapy.project
import minervapy.conversion

_maps_url = "models/"
_download_format_url = "downloadModel"
_download_image_url = "downloadImage"


@dataclasses.dataclass
class Article:
    title: str | None = None
    authors: list[str] = dataclasses.field(default_factory=list)
    journal: str | None = None
    year: int | None = None
    link: str | None = None
    pubmedId: str | None = None
    citationCount: int | None = None


@dataclasses.dataclass
class Reference:
    link: str | None = None
    article: Article | None = None
    type: str | None = None
    resource: str | None = None
    id: int | None = None
    annotatorClassName: str | None = None


@dataclasses.dataclass
class Author:
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    organisation: str | None = None


@dataclasses.dataclass
class Map:
    name: str | None = None
    description: str | None = None
    idObject: int | None = None
    width: float | None = None
    height: float | None = None
    tileSize: float | None = None
    defaultCenterX: float | None = None
    defaultCenterY: float | None = None
    defaultZoomLevel: float | None = None
    minZoom: float | None = None
    maxZoom: float | None = None
    authors: list[Author] = dataclasses.field(default_factory=list)
    references: list[Reference] = dataclasses.field(default_factory=list)
    creationDate: str | None = None
    modificationDates: list[str] = dataclasses.field(default_factory=list)
    projectId: str | None = (
        None  # added to keep track of the project the map belongs to
    )

    def download(
        self,
        format="celldesigner",
        output_file_path=None,
        unzip=True,
        polygon=None,  # list[tuple[float, float]]
        element_ids=None,  # list[str]
        reaction_ids=None,  # list[str]
        background_overlay_id=None,  # str
        zoom_level=None,  # float
        overlay_ids=None,  # list[str]
    ):
        return download_map(
            self,
            format=format,
            output_file_path=output_file_path,
            unzip=unzip,
            polygon=polygon,
            element_ids=element_ids,
            reaction_ids=reaction_ids,
            background_overlay_id=background_overlay_id,
            zoom_level=zoom_level,
            overlay_ids=overlay_ids,
        )


class _ArticleSchema(marshmallow.Schema):
    title = marshmallow.fields.String(required=False, allow_none=True)
    authors = marshmallow.fields.List(
        marshmallow.fields.String, required=False, allow_none=True
    )
    journal = marshmallow.fields.String(required=False, allow_none=True)
    year = marshmallow.fields.Integer(required=False, allow_none=True)
    link = marshmallow.fields.String(required=False, allow_none=True)
    pubmedId = marshmallow.fields.String(required=False, allow_none=True)
    citationCount = marshmallow.fields.Integer(required=False, allow_none=True)


class _ReferenceSchema(marshmallow.Schema):
    link = marshmallow.fields.String(required=False, allow_none=True)
    article = marshmallow.fields.Nested(
        _ArticleSchema, required=False, allow_none=True
    )
    type = marshmallow.fields.String(required=False, allow_none=True)
    resource = marshmallow.fields.String(required=False, allow_none=True)
    id = marshmallow.fields.Integer(required=False, allow_none=True)
    annotatorClassName = marshmallow.fields.String(
        required=False, allow_none=True
    )


class _AuthorSchema(marshmallow.Schema):
    firstName = marshmallow.fields.String(required=False, allow_none=True)
    lastName = marshmallow.fields.String(required=False, allow_none=True)
    email = marshmallow.fields.String(required=False, allow_none=True)
    organisation = marshmallow.fields.String(required=False, allow_none=True)


class _MapSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=False, allow_none=True)
    description = marshmallow.fields.String(required=False, allow_none=True)
    idObject = marshmallow.fields.Integer(required=False, allow_none=True)
    width = marshmallow.fields.Float(required=False, allow_none=True)
    height = marshmallow.fields.Float(required=False, allow_none=True)
    tileSize = marshmallow.fields.Float(required=False, allow_none=True)
    defaultCenterX = marshmallow.fields.Float(required=False, allow_none=True)
    defaultCenterY = marshmallow.fields.Float(required=False, allow_none=True)
    defaultZoomLevel = marshmallow.fields.Float(required=False, allow_none=True)
    minZoom = marshmallow.fields.Float(required=False, allow_none=True)
    maxZoom = marshmallow.fields.Float(required=False, allow_none=True)
    authors = marshmallow.fields.List(
        marshmallow.fields.Nested(_AuthorSchema),
        required=False,
        allow_none=True,
    )
    references = marshmallow.fields.List(
        marshmallow.fields.Nested(_ReferenceSchema),
        required=False,
        allow_none=True,
    )
    creationDate = marshmallow.fields.String(required=False, allow_none=True)
    modificationDates = marshmallow.fields.List(
        marshmallow.fields.String, required=False, allow_none=True
    )
    projectId = marshmallow.fields.String(
        required=False, allow_none=True
    )  # added to keep track of the project the map belongs to

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Map(**data)


def get_maps(project_or_project_id):
    if isinstance(project_or_project_id, minervapy.project.Project):
        project_id = project_or_project_id.projectId
    else:
        project_id = project_or_project_id
    url = minervapy.utils.join_urls(
        [
            minervapy.session.get_base_url(),
            minervapy.project._projects_url,
            project_id,
            _maps_url,
        ]
    )
    maps = minervapy.utils.request_to_objects(
        url, _MapSchema, many=True, additional_data={"projectId": project_id}
    )
    return maps


def get_map(map_id, project_or_project_id):
    if isinstance(project_or_project_id, minervapy.project.Project):
        project_id = project_or_project_id.projectId
    else:
        project_id = project_or_project_id
    url = minervapy.utils.join_urls(
        [
            minervapy.session.get_base_url(),
            minervapy.project._projects_url,
            project_id,
            _maps_url,
            str(map_id),
        ]
    )
    model = minervapy.utils.request_to_objects(
        url, _MapSchema, additional_data={"projectId": project_id}
    )
    return model


def download_map(
    map_or_map_id,
    project_or_project_id=None,
    format="celldesigner",
    output_file_path=None,
    unzip=True,
    polygon=None,  # list[tuple[float, float]]
    element_ids=None,  # list[str]
    reaction_ids=None,  # list[str]
    background_overlay_id=None,  # str
    zoom_level=None,  # float
    overlay_ids=None,  # list[str]
):
    if not isinstance(map_or_map_id, Map):
        if project_or_project_id is None:
            raise ValueError(
                "you must either provide a map, a map ID and a project ID, or a map ID and a project"
            )
        map_id = map_or_map_id
        if not isinstance(project_or_project_id, minervapy.project.Project):
            project_id = project_or_project_id
        else:
            project_id = project_or_project_id.projectId
    else:
        map_id = map_or_map_id.idObject
        project_id = map_or_map_id.projectId
    if format in minervapy.conversion._image_formats:
        download_url = _download_image_url
    else:
        download_url = _download_format_url
    url_suffix = f"{map_id}:{download_url}"
    url = minervapy.utils.join_urls(
        [
            minervapy.session.get_base_url(),
            minervapy.project._projects_url,
            project_id,
            _maps_url,
            url_suffix,
        ]
    )
    params = {
        "handlerClass": minervapy.conversion._short_format_to_minerva_default_format[
            format
        ]
    }
    if polygon is not None:
        polygon_str = ";".join([f"{t[0]},{t[1]}" for t in polygon])
        params["polygonString"] = polygon_str
    if element_ids is not None:
        element_ids_str = ",".join(element_ids)
        params["elementIds"] = element_ids_str
    if reaction_ids is not None:
        reaction_ids_str = ",".join(reaction_ids)
        params["reactionIds"] = reaction_ids_str
    if background_overlay_id is not None:
        params["backgroundOverlayId"] = background_overlay_id
    if zoom_level is not None:
        params["zoomLevel"] = zoom_level
    if overlay_ids is not None:
        overlay_ids_str = ",".join(overlay_ids)
        params["overlayIds"] = overlay_ids_str
    data = minervapy.utils.request_to_data(url, params=params, unzip=unzip)
    if output_file_path is not None:
        minervapy.utils.data_to_file(data, output_file_path)
    return data
