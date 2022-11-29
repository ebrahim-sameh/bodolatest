from decouple import config

ENV_TYPE = config('ENV_TYPE', 'DEVELOPMENT')


if ENV_TYPE == 'DEVELOPMENT':

    from .local import *
else:
    from .local import *
