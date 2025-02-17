from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados
DATABASE_URL = "postgresql://postgres:tlaush2020@192.168.15.5:5432/sat_system_db"


# Cria a engine de conexão
engine = create_engine(DATABASE_URL)

# Tenta conectar ao banco de dados
try:
    connection = engine.connect()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    connection.close()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")