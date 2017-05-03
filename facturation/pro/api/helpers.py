import requests.sessions
from .exceptions import InvalidArgumentException

def generate_page_params_from_xpag(p):
    """Generate ?page params based on X-Pagination to allow iteration"""
    total_pages = p['total_pages']
    return tuple({'page': pp} for pp in range(1, total_pages+1))


class ClientFactory(object):
    def __init__(self, username, password, firm_id, identifier):
        self.username = username
        self.password = password
        self.firm_id = firm_id
        self.identifier = identifier

    def get(self, cls):
        return cls(self.username, self.password, self.firm_id, self.identifier)


class Client(object):
    IDENTIFIER_KEY = 'id'  # a safe default


    def __init__(self, username, password, firm_id, identifier):
        self._authtuple = (username, password)
        self._firm_id = firm_id
        self._headers = {
        'User-Agent': "ChloeTigre lib ({})".format(identifier)
        }
        self._session = requests.sessions.Session()
        self._base_url = "https://www.facturation.pro/firms/{}/".format(firm_id)

    @classmethod
    def get_detail_string(cls, details):
        if isinstance(details, str):
            return details
        else:
            return '{}'.format(details[cls.IDENTIFIER_KEY])

    def build_url(self, details=None):
        if not details:
            return '{}{}.json'.format(self._base_url, self.RESOURCE)
        else:
            return '{}{}/{}.json'.format(self._base_url, self.RESOURCE, self.get_detail_string(details))

    def build_headers(self, for_post=False):
        if not for_post:
            return self._headers
        else:
            d = {
            'Content-Type': 'application/json; charset=utf-8'
            }
            d.update(self._headers)
            return d

    def _meth_get(self, details=None, **kwargs):
        return self._session.get(
            self.build_url(details),
            auth=self._authtuple, headers=self.build_headers(), **kwargs)

    def _meth_delete(self, details=None, **kwargs):
        return self._session.delete(
            self.build_url(details),
            auth=self._authtuple, headers=self.build_headers(), params=kwargs)

    def _meth_post(self, details=None, **kwargs):
        return self._session.post(
            url=self.build_url(details),
            auth=self._authtuple, headers=self.build_headers(for_post=True), json=kwargs)

    def _meth_patch(self, details=None, **kwargs):
        return self._session.patch(
            url=self.build_url(details),
            auth=self._authtuple, headers=self.build_headers(for_post=True), json=kwargs)

    def _list(self, **kwargs):
        args_poss = self.POSSIBLE_ARGS_LIST
        bad_args = [k for k in kwargs if k not in args_poss]
        if bad_args:
            raise InvalidArgumentException(', '.join(bad_args))
        return self._meth_get(params=kwargs)

    def list(self, **kwargs):
        response = self._list(**kwargs)
        return response.json()

    def list_all(self, **kwargs):
        d = self._list(**kwargs)
        paginations = generate_page_params_from_xpag(d.headers['X-Pagination'])
        if len(paginations) == 1:
            return d.json()
        for page in paginations:
            kwargs.update(page)
            d += self.list(kwargs)
        return d

    def _post(self, details, body):
        args_poss = self.POSSIBLE_ARGS_POST_BODY
        bad_args = [k for k in body if k not in args_poss]
        if bad_args:
            raise InvalidArgumentException(', '.join(bad_args))
        return self._meth_post(details=details, **body)

    def post(self, details=None, body=None):
        return self._post(details=details, body=body).json()

    def _patch(self, details, body):
        args_poss = self.POSSIBLE_ARGS_PATCH
        bad_args = [k for k in body if k not in args_poss]
        if bad_args:
            raise InvalidArgumentException(', '.join(bad_args))
        return self._meth_patch(details=details, **body)

    def patch(self, details=None, body=None):
        return self._patch(details=details, body=body).json()

    def _delete(self, details):
        return self._meth_delete(details)

    def delete(self, details):
        return self._delete(details=details)
