import os

from sqlalchemy import create_engine


# Parámetros de conexión a la base de datos
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("MYSQL_DATABASE")

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URI)
