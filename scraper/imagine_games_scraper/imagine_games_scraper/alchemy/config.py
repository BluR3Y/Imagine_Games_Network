import os
from dotenv import dotenv_values

from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

env = os.environ.get("PYTHON_ENV")
environment_variables = os.environ if env == "production" else dotenv_values("../../../../env/scraper/.env.development")


def postgres_connection():
    return create_engine(
        url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            environment_variables.get('POSTGRES_ACCESS_USER'),
            parse.quote(environment_variables.get('POSTGRES_ACCESS_PASSWORD')),
            environment_variables.get('POSTGRES_HOST'),
            environment_variables.get('POSTGRES_PORT'),
            environment_variables.get('POSTGRES_DATABASE')
        )
    )

# engine = postgres_connection()
# session = sessionmaker(bind=engine)()

def create_session():
    engine = postgres_connection()
    return sessionmaker(bind=engine)()

Base = declarative_base()

# if __name__ == '__main__':
#     try:
#         engine = postgres_connection()
#         session = sessionmaker(bind=engine)()
#         print(f"Connection to the database created successfully.")
#     except Exception as ex:
#         print("Connection could not be made due to the following error: \n", ex)