import dataclasses

import requests
import marshmallow
import io
import zipfile

import minvervapy.project
import minvervapy.utils

_handlers = {
    "sbgnml": "lcsb.mapviewer.converter.model.sbgnml.SbgnmlXmlConverter",
    "celldesigner": "lcsb.mapviewer.converter.model.celldesigner.CellDesignerXmlParser",
    "sbml": "lcsb.mapviewer.converter.model.sbml.SbmlParser",
    "gpml": "lcsb.mapviewer.wikipathway.GpmlParser",
    "png": "lcsb.mapviewer.converter.graphics.PngImageGenerator",
    "pdf": "lcsb.mapviewer.converter.graphics.PdfImageGenerator",
    "svg": "lcsb.mapviewer.converter.graphics.SvgImageGenerator",
}

_models_url = "models/"
_download_model_url = "downloadModel"
_download_image_url = "downloadImage"


@dataclasses.dataclass
class Model:
    idObject: int
    name: str
    projectId: str

    def download(self, format="celldesigner", output=None, unzip=True):
        return download_model(self, format=format, output=output)


class _ModelSchema(marshmallow.Schema):
    idObject = marshmallow.fields.Int()
    name = marshmallow.fields.Str()
    projectId = marshmallow.fields.Str()

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Model(**data)


def get_models(project_or_project_id):
    if isinstance(project_or_project_id, minervapy.project.Project):
        project_id = project_or_project_id.projectId
    url = minervapy.utils.join_urls(
        [_base_url, _projects_url, project_id, _models_url]
    )
    models = minervapy.utils.get_objects(
        url, _ModelSchema, many=True, additional_data={"projectId": project_id}
    )
    return models


def get_model(model_id, project_or_project_id):
    if isinstance(project_or_project_id, Project):
        project_id = project_or_project_id.projectId
    url = minvervapy.utils.join_urls(
        [_base_url, _projects_url, project_id, _models_url, model_id]
    )
    model = minervapy.utils.get_objects(
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
    url = minervapy.utils.join_urls(
        [_base_url, _projects_url, project_id, _models_url, download_url]
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
