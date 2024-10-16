from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Create a SQLite in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DBContext:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()


class ConnectionPool:
    _connection_str = SQLALCHEMY_DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    _session_maker = sessionmaker(bind=engine, expire_on_commit=False, autocommit=False)

    @classmethod
    def open_session(cls) -> DBContext:
        return DBContext(session=cls._session_maker())

    @classmethod
    def new_session(cls) -> Session:
        return cls._session_maker()