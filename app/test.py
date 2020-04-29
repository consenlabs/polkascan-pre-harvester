from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func

engine = create_engine(DB_CONNECTION, echo=DEBUG, isolation_level="READ_UNCOMMITTED")
session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
session = scoped_session(session_factory)

extrinsic = Extrinsic.query(db_session).filter_by(block_id=2064961,module_id='timestamp',call_id='set').first()

datetime = extrinsic.params[0]['value'].as_string()
if not datetime:
    print('#{} datetime not found, skip'.format(nr))
    continue

print(datetime)
