import environ

env = environ.Env(
    SECRET_KEY=(str, "gW(VDtylhoAuZNcLbIC=ai5=2*tPZ=Gmf4D1^4T!NxX3tB0%_w7pYY2+FgDx"),
    DEBUG=(bool, False),
    POSTGRES_NAME=(str, "postgres_name"),
    POSTGRES_USER=(str, "postgres_user"),
    POSTGRES_PASSWORD=(str, "postgres_password"),
    POSTGRES_HOST=(str, "localhost"),
    POSTGRES_PORT=(int, 5432),
    REDIS_HOST=(str, "localhost"),
    REDIS_PORT=(int, 6379),
    CELERY_BROKER_URL=(str, "redis://localhost:6379"),
    EMAIL_HOST_USER=(str, "user@email.com"),
    EMAIL_HOST_PASSWORD=(str, "password"),
)
