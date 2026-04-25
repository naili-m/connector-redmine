from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import operations, _check_health

logger = get_logger('Fabric Studio')


class FortinetFabricStudio(Connector):

    def execute(self, config, operation, params, **kwargs):
        params.update({'action':operation})
        action = operations.get(operation)
        return action(config, params)

    def check_health(self, config):
        _check_health(config)
