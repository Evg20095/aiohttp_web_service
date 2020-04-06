import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

log_pass_table = Table(
    'log_pass_table', meta,
    
    Column('Logins',  String(50), nullable=False),
    Column('Passwords', String(50), nullable=False)
)

log_links_table = Table(
    'log_links_table', meta,
    
    Column('Logins',  String(50), nullable=False),
    Column('Links', String(200), nullable=False)
)

async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine
    
async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()