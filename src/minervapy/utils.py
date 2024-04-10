import requests
import zipfile
import io

import marshmallow

import minervapy.session


class StatusCodeException(Exception):
    pass


def join_urls(urls):
    to_join = []
    for url in urls[:-1]:
        if not url.endswith("/"):
            url = f"{url}/"
        to_join.append(url)
    to_join.append(urls[-1])
    return "".join(to_join)


def check_response(response):
    if not response.ok:
        raise StatusCodeException(f"{response.status_code}, {response.text}")


def unzip_data(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    zip_infos = z.infolist()
    data = z.read(zip_infos[0])
    return data


def data_to_file(data, output_file_path):
    with open(output_file_path, "wb") as output_file:
        output_file.write(data)


def request_to_response(
    url,
    method="GET",
    data=None,
    params=None,
    headers=None,
):
    cookies = minervapy.session.get_auth_cookies()
    response = requests.request(
        url=url,
        method=method,
        data=data,
        params=params,
        headers=headers,
        cookies=cookies,
    )
    return response


def request_to_data(
    url, method="GET", data=None, params=None, headers=None, unzip=True
):
    response = request_to_response(
        url, method=method, data=data, params=params, headers=headers
    )
    check_response(response)
    data = response.content
    if unzip and response.headers["Content-Type"] == "application/zip":
        data = unzip_data(data)
    return data


def request_to_objects(
    url,
    schema_cls,
    method="GET",
    data=None,
    params=None,
    headers=None,
    many=False,
    additional_data=None,
):
    if additional_data is None:
        additional_data = {}
    response = request_to_response(
        url, method=method, data=data, params=params, headers=headers
    )
    check_response(response)
    json = response.json()
    if many:
        json_with_additional_data = [e | additional_data for e in json]
    else:
        json_with_additional_data = json | additional_data
    schema = schema_cls(many=many, unknown=marshmallow.EXCLUDE)
    objects = schema.load(json_with_additional_data, partial=True)
    return objects
