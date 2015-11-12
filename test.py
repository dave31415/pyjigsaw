from api import get_person


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