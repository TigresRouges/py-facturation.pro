from .helpers import Client, generate_page_params_from_xpag
from .exceptions import InvalidArgumentException




_args_list = 'page api_id api_custom company last_name email with_sepa sort order'.split()
_args_list_post = 'api_id api_custom company last_name email with_sepa '\
                  'first_name city civility category_id company_name country currency '\
                  'default_vat discount fax individual language mobile pay_before penalty '\
                  'phone short_name siret street validity vat_exemption vat_number website '\
                  'zip_code'.split()
_args_list_patch = [a for a in _args_list_post if a not in ('id')]


class Customers(Client):
    POSSIBLE_ARGS_LIST = _args_list
    POSSIBLE_ARGS_POST_BODY = _args_list_post
    POSSIBLE_ARGS_PATCH = _args_list_patch
    RESOURCE = 'customers'
