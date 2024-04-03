import dataclasses

import marshmallow

import minervapy.utils
import minervapy.session


_projects_url = "projects/"
_download_source_url = "downloadSource"
_statistics_url = "statistics"


@dataclasses.dataclass
class Point:
    x: float | None = None
    y: float | None = None


@dataclasses.dataclass
class Link:  # no doc
    idObject: int | None = None
    imageLinkId: int | None = None
    polygon: list[Point] = dataclasses.field(default_factory=list)
    zoomLevel: int | None = None
    modelPoint: Point | None = None
    modelLinkId: int | None = None
    query: str | None = None
    type: str | None = None


@dataclasses.dataclass
class OverviewImage:  # no doc
    idObject: int | None = None
    filename: str | None = None
    width: int | None = None
    height: int | None = None
    links: list[Link] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Disease:  # no doc
    link: str | None = None
    type: str | None = None
    resource: str | None = None
    id: int | None = None
    annotatorClassName: str | None = None


@dataclasses.dataclass
class Organism:  # no doc
    link: str | None = None
    type: str | None = None
    resource: str | None = None
    id: int | None = None
    annotatorClassName: str | None = None


@dataclasses.dataclass
class Project:
    projectId: str | None = None
    name: str | None = None
    sharedInMinervaNet: bool | None = None
    version: str | None = None
    owner: str | None = None
    creationDate: str | None = None
    disease: Disease | None = None
    organism: str | None = None
    directory: str | None = None
    status: str | None = None
    progress: float | None = None
    notifyEmail: str | None = None
    mapCanvasType: str | None = None
    logEntries: bool | None = None
    overviewImageViews: list[OverviewImage] = dataclasses.field(
        default_factory=list
    )
    topOverviewImage: OverviewImage | None = None


@dataclasses.dataclass
class Statistics:
    publications: int | None = None
    reactionAnnotations: dict[str, int] = dataclasses.field(
        default_factory=dict
    )
    elementAnnotations: dict[str, int] = dataclasses.field(default_factory=dict)


class _PointSchema(marshmallow.Schema):
    x = marshmallow.fields.Float(required=False, allow_none=True)
    y = marshmallow.fields.Float(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Point(**data)


class _LinkSchema(marshmallow.Schema):  # no doc
    idObject = marshmallow.fields.Integer(required=False, allow_none=True)
    imageLinkId = marshmallow.fields.Integer(required=False, allow_none=True)
    polygon = marshmallow.fields.List(
        marshmallow.fields.Nested(_PointSchema), required=False, allow_none=True
    )
    zoomLevel = marshmallow.fields.Integer(required=False, allow_none=True)
    modelPoint = marshmallow.fields.Nested(
        _PointSchema, required=False, allow_none=True
    )
    modelLinkId = marshmallow.fields.Integer(required=False, allow_none=True)
    query = marshmallow.fields.String(required=False, allow_none=True)
    type = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Link(**data)


class _OverviewImageSchema(marshmallow.Schema):  # no doc
    idObject = marshmallow.fields.Integer(required=False, allow_none=True)
    filename = marshmallow.fields.String(required=False, allow_none=True)
    width = marshmallow.fields.Integer(required=False, allow_none=True)
    height = marshmallow.fields.Integer(required=False, allow_none=True)
    links = marshmallow.fields.List(
        marshmallow.fields.Nested(_LinkSchema), required=False, allow_none=True
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return OverviewImage(**data)


class _OrganismSchema(marshmallow.Schema):  # no doc
    link = marshmallow.fields.String(required=False, allow_none=True)
    type = marshmallow.fields.String(required=False, allow_none=True)
    resource = marshmallow.fields.String(required=False, allow_none=True)
    id = marshmallow.fields.Integer(required=False, allow_none=True)
    annotatorClassName = marshmallow.fields.String(
        required=False, allow_none=True
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Organism(**data)


class _DiseaseSchema(marshmallow.Schema):  # no doc
    link = marshmallow.fields.String(required=False, allow_none=True)
    type = marshmallow.fields.String(required=False, allow_none=True)
    resource = marshmallow.fields.String(required=False, allow_none=True)
    id = marshmallow.fields.Integer(required=False, allow_none=True)
    annotatorClassName = marshmallow.fields.String(
        required=False, allow_none=True
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Disease(**data)


class _ProjectSchema(marshmallow.Schema):
    projectId = marshmallow.fields.String(required=False, allow_none=True)
    name = marshmallow.fields.String(required=False, allow_none=True)
    sharedInMinervaNet = marshmallow.fields.Boolean(
        required=False, allow_none=True
    )
    version = marshmallow.fields.String(required=False, allow_none=True)
    owner = marshmallow.fields.String(required=False, allow_none=True)
    creationDate = marshmallow.fields.String(required=False, allow_none=True)
    disease = marshmallow.fields.Nested(
        _DiseaseSchema, required=False, allow_none=True
    )
    organism = marshmallow.fields.Nested(
        _OrganismSchema, required=False, allow_none=True
    )
    directory = marshmallow.fields.String(required=False, allow_none=True)
    status = marshmallow.fields.String(required=False, allow_none=True)
    progress = marshmallow.fields.Float(required=False, allow_none=True)
    notifyEmail = marshmallow.fields.String(required=False, allow_none=True)
    mapCanvasType = marshmallow.fields.String(required=False, allow_none=True)
    logEntries = marshmallow.fields.Boolean(required=False, allow_none=True)
    overviewImageViews = marshmallow.fields.List(
        marshmallow.fields.Nested(_OverviewImageSchema),
        required=False,
        allow_none=True,
    )
    topOverviewImage = marshmallow.fields.Nested(
        _OverviewImageSchema, required=False, allow_none=True
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Project(**data)


class _StatisticsSchema(marshmallow.Schema):
    publications = marshmallow.fields.Integer(required=False, allow_none=True)
    reactionAnnotations = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(),
        values=marshmallow.fields.Integer,
        required=False,
        allow_none=True,
    )
    elementAnnotations = marshmallow.fields.Dict(
        keys=marshmallow.fields.String(),
        values=marshmallow.fields.Integer,
        required=False,
        allow_none=True,
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Statistics(**data)


def get_projects():
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _projects_url]
    )
    projects = minervapy.utils.request_to_objects(
        url, _ProjectSchema, many=True
    )
    return projects


def get_project(project_id):
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _projects_url, project_id]
    )
    project = minervapy.utils.request_to_objects(
        url, _ProjectSchema, many=False
    )
    return project


def download_source(project_or_project_id, output_file_path=None, unzip=True):
    if isinstance(project_or_project_id, Project):
        project_id = project_or_project_id.projectId
    else:
        project_id = project_or_project_id
    url_suffix = f"{project_id}:{_download_source_url}"
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _projects_url, url_suffix]
    )
    data = minervapy.utils.request_to_data(url, unzip=True)
    if output_file_path is not None:
        minervapy.utils.data_to_file(data, output_file_path)
    return data


def get_statistics(project_or_project_id):
    if isinstance(project_or_project_id, Project):
        project_id = project_or_project_id.projectId
    else:
        project_id = project_or_project_id
    url = minervapy.utils.join_urls(
        [
            minervapy.session.get_base_url(),
            _projects_url,
            project_id,
            _statistics_url,
        ]
    )
    statistics = minervapy.utils.request_to_objects(
        url, _StatisticsSchema, many=False
    )
    return statistics
