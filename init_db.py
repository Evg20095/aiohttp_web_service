from sqlalchemy import create_engine, MetaData

from aiohttp_polls.settings import config
from aiohttp_polls.db import log_pass_table, log_links_table


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[log_pass_table, log_links_table])
    
def sample_data(engine):
    conn = engine.connect()
    
    conn.execute(log_pass_table.insert(), [
        {'Logins': 'Evgeny',
         'Passwords': 'Zhemkov20095'}
    ])

    conn.close()


if __name__ == "__main__":
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)