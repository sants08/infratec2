import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Senha em texto puro (sem %23 ou %3A)
senha_raw = "Infratec#7:02"
senha_encoded = quote_plus(senha_raw)

# URL formatada corretamente
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql://postgres:{senha_encoded}@db.nnaubbzmcplmdxndudjc.supabase.co:5432/postgres"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()