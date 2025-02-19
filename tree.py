import os

def listar_estrutura(diretorio, nivel=0):
    """Lista todos os arquivos e diretórios do projeto."""
    try:
        for item in os.listdir(diretorio):
            caminho_completo = os.path.join(diretorio, item)
            if os.path.isdir(caminho_completo):
                print("  " * nivel + f"📂 {item}/")
                listar_estrutura(caminho_completo, nivel + 1)
            else:
                print("  " * nivel + f"📄 {item}")
    except PermissionError:
        print("  " * nivel + "🚫 [Sem Permissão]")

# Obtém a raiz do projeto
raiz_projeto = os.path.abspath(os.getcwd())

print(f"\n🗂️ Estrutura do projeto: {raiz_projeto}\n")
listar_estrutura(raiz_projeto)
