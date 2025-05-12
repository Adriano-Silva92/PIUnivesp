import os  # Importa o módulo 'os' para acessar variáveis de ambiente do sistema

# Tenta obter o valor da variável de ambiente 'DJANGO_ENV'.
# Se não estiver definida, assume 'dev' (desenvolvimento) como padrão.
env = os.getenv("DJANGO_ENV", "dev")

if env == "prod": # Verifica se o ambiente é 'prod' (produção)
    from .prod import * # Importa todas as configurações do arquivo 'prod.py'

elif env == "dev": # Se o ambiente for 'dev' (desenvolvimento)
    from .dev import *# Importa todas as configurações do arquivo 'dev.py'

else: # Se o valor da variável for diferente de 'prod' ou 'dev'
    # Lança um erro informando que o valor de DJANGO_ENV é inválido
    raise ValueError(f"Ambiente inválido: DJANGO_ENV={env}")

