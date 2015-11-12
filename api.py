import requests
import json
import time

from params import api_token_file, base_url
token = open(api_token_file).read().strip()
assert len(token) == 32
headers = {'Authorization': token}


def get(url_suffix, full_response=False):
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
        print result.headers
        return None
    if full_response:
        # optionally get the full response object
        # not just json content
        return result
    return json.loads(result.content)


def get_person(person_id):
    """
    Get a person by employee id
    :param person_id: string or int, e.g. 10050
    :return: dict, content from person api
    """
    url_suffix = '/people/%s' % person_id
    return get(url_suffix)


def get_all_people():
    """
    Get a list of all people content
    handle pagination and throttling limits
    :return:
    """
    max_calls_per_min = 30
    page_max = 500
    seconds_to_wait = 70

    # get page 1 and extract pagination link info
    result = get('/people', full_response=True)
    people = json.loads(result.content)
    n_pages = int(result.headers['X-Total-Pages'])
    page_max = min(n_pages, page_max)
    for call_num, page in enumerate(xrange(2, page_max+1)):
        if call_num % max_calls_per_min == 0 and call_num > 0:
            # avoid throttling by waiting for a while
            # every time max_calls_per_min additional calls are made
            print "Sleeping for %s seconds to avoid throttling" % seconds_to_wait
            time.sleep(seconds_to_wait)

        url_suffix = "/people?page=%s" % page
        more_people = get(url_suffix)
        print "url: %s, page: %s, n_people=%s" % \
              (url_suffix, page, len(more_people))
        people.extend(more_people)
    return people


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