import requests
import marshmallow

import minervapy.session


def join_urls(urls):
    to_join = []
    for url in urls[:-1]:
        if not url.endswith("/"):
            url = f"{url}/"
        to_join.append(url)
    to_join.append(urls[-1])
    return "".join(to_join)


def get_json(response):
    if not response.ok:
        raise Exception(f"{response.status_code}, {response.text}")
    json = response.json()
    return json


def get_objects(
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
    cookies = minervapy.session.get_auth_cookies()
    response = requests.request(
        url=url,
        method=method,
        data=data,
        params=params,
        headers=headers,
        cookies=cookies,
    )
    json = get_json(response)
    if many:
        json_with_additional_data = [e | additional_data for e in json]
    else:
        json_with_additional_data = json | additional_data
    schema = schema_cls(many=many, unknown=marshmallow.EXCLUDE)
    objects = schema.load(json_with_additional_data, partial=True)
    return objects
