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
    authors: list[str] = dataclasses.field(default_factory=list)
    references: list[str] = dataclasses.field(default_factory=list)
    creationDate: str | None = None
    modificationDates: list[str] = dataclasses.field(default_factory=list)
    projectId: str | None = (
        None  # added to keep track of the project the map belongs to
    )

    def download(
        self, format="celldesigner", output_file_path=None, unzip=True
    ):
        return download_map(
            self, format=format, output_file_path=output_file_path, unzip=unzip
        )


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
        marshmallow.fields.String, required=False, allow_none=True
    )
    references = marshmallow.fields.List(
        marshmallow.fields.String, required=False, allow_none=True
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
    response = minervapy.utils.request_to_response(
        url,
        params={
            "handlerClass": minervapy.conversion._short_format_to_minerva_default_format[
                format
            ]
        },
    )
    minervapy.utils.check_response(response)
    content = response.content
    if output_file_path is not None:
        minervapy.utils.response_to_file(response, output_file_path)
    return content
