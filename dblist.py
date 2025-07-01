from sqlalchemy import create_engine, inspect

def get_database_url(config):
    dbtype = config['dbtype']
    user = config['user']
    password = config['password']
    host = config['host']
    database = config['database']

    if dbtype == 'mysql':
        return f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
    elif dbtype == 'postgresql':
        return f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
    elif dbtype == 'sqlite':
        return f"sqlite:///{database}"
    elif dbtype == 'oracle':
        return f"oracle+cx_oracle://{user}:{password}@{host}/{database}"
    elif dbtype == 'mssql':
        # Microsoft SQL Server usando pyodbc
        # Asegúrate de tener instalado: pip install pyodbc
        return f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        raise ValueError(f"Unsupported dbtype: {dbtype}")

def list_tables_and_relations(config):
    if config['dbtype'] == 'mongodb':
        from pymongo import MongoClient
        client = MongoClient(f"mongodb://{config['user']}:{config['password']}@{config['host']}/{config['database']}")
        db = client[config['database']]
        collections = db.list_collection_names()
        print("Collections:", collections)
        return

    url = get_database_url(config)
    engine = create_engine(url)
    inspector = inspect(engine)

    all_tables = inspector.get_table_names()
    print("Tables and their foreign key relations:\n")
    for table in all_tables:
        fks = inspector.get_foreign_keys(table)
        relations = [fk['referred_table'] for fk in fks if fk['referred_table'] is not None]
        if not relations:
            relations = [table]  # if no relation, show itself
        print(f"Table: {table}, Relations: {', '.join(relations)}")

# Example usage:

config = {
    'user': 'root',
    'password': '123456789',
    'host': 'localhost',
    'database': 'granjacob_uuid',
    'dbtype': 'mysql'  # mysql, postgresql, sqlite, oracle, mssql, mongodb
}


config_postgres = {
    'user': 'postgres',
    'password': '123456789',
    'host': 'localhost:7778',
    'database': 'granjacob',
    'dbtype': 'postgresql'  # mysql, postgresql, sqlite, oracle, mssql, mongodb
}

list_tables_and_relations(config_postgres)