from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://usuario:senha@localhost:5432/sat_system_db"  # Substitua pelo seu usuário e senha
#DATABASE_URL = "postgresql://postgres:tlaush2020@localhost:5432/sat_system_db"  # Substitua pelo seu usuário e senha
#DATABASE_URL = "postgresql://postgres:tlaush2020@192.168.15.5:5432/sat_system_db"
#DATABASE_URL = "postgresql://postgres:tlaush2020@191.9.122.99:5432/sat_system_db"
DATABASE_URL = "postgresql://neondb_owner:npg_uOAVw76PYpTD@ep-black-butterfly-a87ca2ez-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
