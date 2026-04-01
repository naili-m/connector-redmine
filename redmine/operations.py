from redminelib import Redmine
from connectors.core.connector import get_logger, ConnectorError


logger = get_logger('redmine')


class Redmine(object):
    def __init__(self, config):
        self.server_url = config.get('server_url')
        if not self.server_url.startswith('https://'):
            self.server_url = 'https://' + self.server_url
        self.server_url = self.server_url.strip('/')
        self.api_key = config.get('api_key')
        self.verify_ssl = config.get('verify_ssl')
        return Redmine(self.server_url, key=self.api_key)

def _check_health(config):
    try:
        redmine = Redmine(config)
    except:
        logger.exception('Error occured')
        raise ConnectorError('Error occured')


def run_api_call(config, params):
   
    http_method = params.get('http_method')
    endpoint = params.get('endpoint')
    url_params = params.get('url_params')
    payload = params.get('payload')
    params = [
        ("set_filter", "1"),
        ("sort", "id:desc"),
        ("f[]", "status_id"),
        ("op[status_id]", "!"),
        ("v[status_id][]", "15"),
        ("v[status_id][]", "5"),
        ("v[status_id][]", "6"),
        ("v[status_id][]", "21"),
        ("f[]", "cf_1"),
        ("op[cf_1]", "="),
        ("v[cf_1][]", "FortiMonitor"),
        ("v[cf_1][]", "FortiSOAR"),
        ("f[]", "assigned_to_id"),
        ("op[assigned_to_id]", "!*"),
        ("f[]", "tracker_id"),
        ("op[tracker_id]", "="),
        ("v[tracker_id][]", "9"),
        ("c[]", "tracker"),
        ("c[]", "status"),
        ("c[]", "priority"),
        ("c[]", "subject"),
        ("c[]", "updated_on"),
        ("c[]", "cf_2"),
        ("c[]", "project"),
        ("c[]", "author"),
    ]
    redmine = Redmine("https://knock.fortinet-cse.com", key="API_KEY")
    return redmine.engine.request(http_method, endpoint, params=url_params)

operations = {
    'run_api_call': run_api_call
}