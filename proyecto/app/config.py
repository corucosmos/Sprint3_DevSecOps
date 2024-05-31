from sqlalchemy import create_engine

# Parámetros de conexión a la base de datos
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "mysql"
DB_NAME = "pedidos_db"

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URI)
