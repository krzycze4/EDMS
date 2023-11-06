import environ

env = environ.Env(DEBUG=(bool, False), SECRET_KEY=(str, "not_secret_key"))
