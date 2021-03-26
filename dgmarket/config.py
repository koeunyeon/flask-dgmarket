import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dgmarket_secret_key"  # 개발은 뭐 고칠때마다 바뀌니까 귀찮아서 고정.
    SQLALCHEMY_DATABASE_URI = "sqlite:///{path}".format(
        path=os.path.join(base_dir, "dgmarket.development.sqlite"))
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    DEBUG = True
    SECRET_KEY = "dgmarket_test_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///{path}".format(
        path=os.path.join(base_dir, "dgmarket.test.sqlite"))
    SQLALCHEMY_ECHO = False


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestConfig
)


def from_object(config_name=None):
    if config_name is not None:
        return config_by_name[config_name]

    env_config_name = os.getenv("FLASK_ENV", None)
    if env_config_name is not None:
        return config_by_name[env_config_name]
    default_config_name = 'development'
    return config_by_name[default_config_name]
