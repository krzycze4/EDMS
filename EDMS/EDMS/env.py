import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "not_secret_key"),
    KRS_API_TIMEOUT=(int, 2),
    POSTGRES_NAME=(str, "postgres"),
    POSTGRES_USER=(str, "postgres"),
    POSTGRES_PASSWORD=(str, "postgres"),
    POSTGRES_HOST=(str, "localhost"),
    POSTGRES_PORT=(int, 5432),
)
