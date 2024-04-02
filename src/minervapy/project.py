import dataclasses

import marshmallow

import minervapy.utils


_projects_url = "projects/"


@dataclasses.dataclass
class Project:
    version: str
    owner: str
    projectId: str


class _ProjectSchema(marshmallow.Schema):
    version = marshmallow.fields.Str()
    owner = marshmallow.fields.Str()
    projectId = marshmallow.fields.Str()

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return Project(**data)


def get_projects():
    url = minervapy.utils.join_urls([_base_url, _projects_url])
    projects = minervapy.utils.get_objects(url, _ProjectSchema, many=True)
    return projects


def get_project(project_id):
    url = minervapy.utils.join_urls([_base_url, _projects_url, project_id])
    project = minvervapy.utils.get_objects(url, _ProjectSchema, many=False)
    return project
