import requests

import minervapy.utils

_login_url = "doLogin"
_logout_url = "doLogout"
_is_session_valid_url = "users/isSessionValid"

_base_url = None
_auth_cookies = None


def set_base_url(url):
    global _base_url
    _base_url = url


def get_base_url():
    return _base_url


def set_auth_cookies(cookies):
    global _auth_cookies
    _auth_cookies = cookies


def get_auth_cookies():
    return _auth_cookies


def log_in(username, password):
    url = minervapy.utils.join_urls([_base_url, _login_url])
    response = requests.post(
        url, data={"login": username, "password": password}
    )
    if not response.ok:
        raise Exception(f"{response.status_code}, {response.text}")
    set_auth_cookies(response.cookies)
    return response


def log_out():
    url = minervapy.utils.join_urls([_base_url, _logout_url])
    auth_cookies = get_auth_cookies()
    if auth_cookies is None:
        raise Exception("must log in first before logging out")
    response = requests.get(url, cookies=auth_cookies)
    set_auth_cookies(None)
    return response


def is_session_valid():
    url = minervapy.utils.join_urls([_base_url, _is_session_valid_url])
    response = requests.get(url, cookies=get_auth_cookies())
    if response.ok:
        if response.json().get("login") is not None:
            return True
    else:
        if response.json().get("error") == "Access denied.":
            return False
    raise Exception(f"{response.status_code}, {response.text}")
