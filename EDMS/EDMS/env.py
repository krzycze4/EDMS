import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "not_secret_key"),
    KRS_API_TIMEOUT=(int, 2),
)
