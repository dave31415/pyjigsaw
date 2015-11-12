import requests
import json

from params import api_token_file, base_url
token = open(api_token_file).read().strip()
assert len(token) == 32
headers = {'Authorization': token}


def get(url_suffix):
    """
    :param url_suffix: a string suffix added to base url
                       should start with wth "/"
    :return:
    """
    assert url_suffix.startswith("/")
    url = base_url + url_suffix
    result = requests.get(url, headers=headers)
    if result.status_code != requests.codes.ok:
        print "Failed, status code: %s" % result.status_code
        # to catch exception requests.HTTPError, do this
        # result.raise_for_status()
        return None
    return json.loads(result.content)


def get_person(person_id):
    """
    Get a person by employee id
    :param person_id: string or int, e.g. 10050
    :return: dict, content from person api
    """
    url_suffix = '/people/%s' % person_id
    return get(url_suffix)


def test_api():
    """
    Tests that the api can be hit and that authorization works
    and that it can return one particular person who is likely
    to be with the company for some time
    :return:
    """
    # person id for one long time employee
    content = get_person(10050)
    assert content['preferredName'].endswith('immel')


def get_projects():
    """
    Get all projects
    :return:
    """
    # person id for one long time employee
    url_suffix = '/projects'
    content = get(url_suffix)
    return content