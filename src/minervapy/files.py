import dataclasses
import os.path

import requests
import marshmallow

import minervapy.utils
import minervapy.session


_files_url = "files/"
_upload_content_url = "uploadContent"


@dataclasses.dataclass
class File:
    id: int | None = None
    filename: str | None = None
    length: int | None = None
    owner: str | None = None  # int in doc
    uploadedDataLength: int | None = None


class _FileSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer(required=False, allow_none=True)
    filename = marshmallow.fields.String(required=False, allow_none=True)
    length = marshmallow.fields.Integer(required=False, allow_none=True)
    owner = marshmallow.fields.String(required=False, allow_none=True)
    uploadedDataLength = marshmallow.fields.Integer(
        required=False, allow_none=True
    )

    @marshmallow.post_load
    def make(self, data, **kwargs):
        return File(**data)


def create_new_file(file_name, length):
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _files_url]
    )
    new_file = minervapy.utils.get_objects(
        url=url,
        schema_cls=_FileSchema,
        method="POST",
        params={"filename": file_name, "length": length},
    )
    return new_file


def upload_content_to_file(input_file_path, output_file_or_file_id):
    if isinstance(output_file_or_file_id, File):
        output_file_id = output_file_or_file_id.id
    elif isinstance(output_file_or_file_id, int):
        output_file_id = str(output_file_or_file_id)
    else:
        output_file_id = output_file_or_file_id
    url_suffix = f"{output_file_id}:{_upload_content_url}"
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _files_url, url_suffix]
    )
    with open(input_file_path, "rb") as input_file:
        input_data = input_file.read()
    output_file = minervapy.utils.get_objects(
        url=url,
        schema_cls=_FileSchema,
        method="POST",
        data=input_data,
        headers={"Content-Type": "application/octet-stream"},
    )
    return output_file


def upload_file(input_file_path, file_name, length=None):
    if length is None:
        length = os.path.getsize(input_file_path)
    output_file = create_new_file(file_name, length)
    output_file = upload_content_to_file(input_file_path, output_file)
    return output_file


def get_file(file_id):
    if isinstance(file_id, int):
        file_id = str(file_id)
    url = minervapy.utils.join_urls(
        [minervapy.session.get_base_url(), _files_url, file_id]
    )
    file = minervapy.utils.get_objects(url, _FileSchema)
    return file
