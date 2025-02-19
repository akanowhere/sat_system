from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import socket
import requests

# URL de conexão com o banco de dados
#DATABASE_URL = "postgresql://postgres:tlaush2020@192.168.15.5:5432/sat_system_db"
DATABASE_URL = "postgresql://postgres:tlaush2020@191.9.122.99:5432/sat_system_db"
#DATABASE_URL = "postgresql://postgres:tlaush2020@[2804:7f0:b84d:7001:2cac:75eb:17ba:90]:5432/sat_system_db"
#DATABASE_URL = "postgresql://neondb_owner:npg_uOAVw76PYpTD@ep-black-butterfly-a87ca2ez-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"


# Obtém o IP público
ip_publico = requests.get('https://api.ipify.org').text

# Exibe o IP público no Streamlit
print(ip_publico)



# Cria a engine de conexão
engine = create_engine(DATABASE_URL)

# Tenta conectar ao banco de dados
try:
    connection = engine.connect()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    connection.close()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")