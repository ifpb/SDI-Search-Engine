import sqlalchemy as sql


def create_engine():
    return sql.create_engine('postgresql://postgres:postgres@localhost:5433/inde_database', pool_size=10, max_overflow=30)
