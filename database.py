from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import Column, Integer, String


class Base(DeclarativeBase):
    pass

class Link(Base):
    __tablename__ = 'core'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    short_code: Mapped[str] = mapped_column(String(9), nullable=False)
    short_url: Mapped[str] = mapped_column(String)

engine = create_engine('sqlite:///lincore.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# engine = create_engine('sqlite:///linkcore.db')
# metadata = MetaData()

# linkcore = Table(
#     'links', metadata,
#     Column('id', Integer, primary_key= True),
#     Column('idshort_code', String),
#     Column('link', String)
# )
# metadata.create_all(engine)