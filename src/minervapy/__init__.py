import dataclasses

import requests
import marshmallow
import io
import zipfile

base_url = None
auth_cookies = None

_handlers = {
    "sbgnml": "lcsb.mapviewer.converter.model.sbgnml.SbgnmlXmlConverter",
    "celldesigner": "lcsb.mapviewer.converter.model.celldesigner.CellDesignerXmlParser",
    "sbml": "lcsb.mapviewer.converter.model.sbml.SbmlParser",
    "gpml": "lcsb.mapviewer.wikipathway.GpmlParser",
    "png": "lcsb.mapviewer.converter.graphics.PngImageGenerator",
    "pdf": "lcsb.mapviewer.converter.graphics.PdfImageGenerator",
    "svg": "lcsb.mapviewer.converter.graphics.SvgImageGenerator",
}

_login_url = "doLogin"
_projects_url = "projects/"
_models_url = "models/"
_configuration_url = "configuration/"
_download_model_url = "downloadModel"
_download_image_url = "downloadImage"


def _join_urls(urls):
    to_join = []
    for url in urls[:-1]:
        if not url.endswith("/"):
            url = f"{url}/"
        to_join.append(url)
    to_join.append(urls[-1])
    return "".join(to_join)


def _get_objects(url, schema_cls, many=False, additional_data=None):
    if additional_data is None:
        additional_data = {}
    if auth_cookies is not None:
        cookies = auth_cookies
    else:
        cookies = None
    response = requests.get(url, cookies=cookies)
    if not response.ok:
        raise Exception(f"{response.status_code}, {response.text}")
    json = response.json()
    if many:
        json_with_additional_data = [e | additional_data for e in json]
    else:
        json_with_additional_data = json | additional_data
    schema = schema_cls(many=many, unknown=marshmallow.EXCLUDE)
    objects = schema.load(json_with_additional_data, partial=True)
    return objects


@dataclasses.dataclass
class Option:
    type: str
    value: str | None = None
    valueType: str | None = None


@dataclasses.dataclass
class Configuation:
    options: list[Option]

    def get_option(self, option_type):
        for option in self.options:
            if option.type == option_type:
                return option
        return None


@dataclasses.dataclass
class Project:
    version: str
    owner: str
    projectId: str


@dataclasses.dataclass
class Model:
    idObject: int
    name: str
    projectId: str

    def download(self, format="celldesigner", output=None, unzip=True):
        return download_model(self, format=format, output=output)


class _OptionSchema(marshmallow.Schema):
    type = marshmallow.fields.Str()
    value = marshmallow.fields.Str()
    valueType = marshmallow.fields.Str()

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Option(**data)


class _ConfigurationSchema(marshmallow.Schema):
    options = marshmallow.fields.List(
        marshmallow.fields.Nested(_OptionSchema, unknown=marshmallow.EXCLUDE)
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Configuation(**data)


class _ProjectSchema(marshmallow.Schema):
    version = marshmallow.fields.Str()
    owner = marshmallow.fields.Str()
    projectId = marshmallow.fields.Str()

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Project(**data)


class _ModelSchema(marshmallow.Schema):
    idObject = marshmallow.fields.Int()
    name = marshmallow.fields.Str()
    projectId = marshmallow.fields.Str()

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Model(**data)


def set_base_url(url):
    global base_url
    base_url = url


def log_in(username, password):
    url = _join_urls([base_url, _login_url])
    response = requests.post(
        url, data={"login": username, "password": password}
    )
    if not response.ok:
        raise Exception(f"{response.status_code}, {response.text}")
    global auth_cookies
    auth_cookies = response.cookies


def log_out():
    global auth_token
    auth_token = None


def get_configuration():
    url = requests.compat.urljoin(base_url, _configuration_url)
    configuration = _get_objects(url, _ConfigurationSchema)
    return configuration


def get_projects():
    url = _join_urls([base_url, _projects_url])
    projects = _get_objects(url, _ProjectSchema, many=True)
    return projects


def get_project(project_id):
    url = _join_urls([base_url, _projects_url, project_id])
    project = _get_objects(url, _ProjectSchema, many=False)
    return project


def get_models(project_or_project_id):
    if isinstance(project_or_project_id, Project):
        project_id = project_or_project_id.projectId
    url = _join_urls([base_url, _projects_url, project_id, _models_url])
    models = _get_objects(
        url, _ModelSchema, many=True, additional_data={"projectId": project_id}
    )
    return models


def get_model(model_id, project_or_project_id):
    if isinstance(project_or_project_id, Project):
        project_id = project_or_project_id.projectId
    url = _join_urls(
        [base_url, _projects_url, project_id, _models_url, model_id]
    )
    model = _get_objects(
        url, _ModelSchema, additional_data={"projectId": project_id}
    )
    return model


def download_model(
    model_or_model_id,
    project_or_project_id=None,
    format="celldesigner",
    output=None,
    unzip=True,
):
    if not isinstance(model_or_model_id, Model):
        if project_or_project_id is None:
            raise ValueError(
                "you must either provide a model, a model ID and a project ID, or a model ID and a project"
            )
        model_id = model_or_model_id
        if not isinstance(project_or_project_id, Project):
            project_id = project_or_project_id
        else:
            project_id = project_or_project_id.projectId
    else:
        model_id = model_or_model_id.idObject
        project_id = model_or_model_id.projectId
    handler = _handlers[format]
    if handler.startswith("lcsb.mapviewer.converter.model."):
        download_url_suffix = _download_model_url
    else:
        download_url_suffix = _download_image_url
    download_url = f"{model_id}:{download_url_suffix}"
    url = _join_urls(
        [base_url, _projects_url, project_id, _models_url, download_url]
    )
    response = requests.get(
        url,
        params={"handlerClass": _handlers[format]},
    )
    content = response.content
    if unzip and response.headers["Content-Type"] == "application/zip":
        z = zipfile.ZipFile(io.BytesIO(content))
        zip_infos = z.infolist()
        content = z.read(zip_infos[0])
    if output is not None:
        with open(output, "wb") as f:
            f.write(content)
    return content


def get_formats():
    formats = []
    return formats
