class ProdConfig:
    pass


class DevConfig:
    pass


class TestConfig:
    pass  # there is no test server for this app atm


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
