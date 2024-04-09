import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "gW(VDtylhoAuZNcLbIC=ai5=2*tPZ=Gmf4D1^4T!NxX3tB0%_w7pYY2+FgDx"),
    KRS_API_TIMEOUT=(int, 2),
    POSTGRES_NAME=(str, "postgres"),
    POSTGRES_USER=(str, "postgres"),
    POSTGRES_PASSWORD=(str, "postgres"),
    POSTGRES_HOST=(str, "localhost"),
    POSTGRES_PORT=(int, 5432),
)
