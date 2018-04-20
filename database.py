"""
Database setup and table creation
"""
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, String, Float


ENGINE = create_engine('sqlite:////tmp/cat.db', convert_unicode=True, echo=True)

METADATA = MetaData(bind=ENGINE)
# Create DB tables here (for now)
CAT_RESULTS = Table('cat_results', METADATA,
                    Column('image_url', String, primary_key=True),
                    Column('is_cat', Boolean),
                    Column('created', Float),
                    Column('last_modified', Float), )

METADATA.create_all(ENGINE)
