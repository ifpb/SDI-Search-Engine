import sqlalchemy as sql


def create_engine():
    return sql.create_engine('postgresql://postgres:postgres@db_postgres:5432/inde_database_docker', pool_size=10, max_overflow=30)
