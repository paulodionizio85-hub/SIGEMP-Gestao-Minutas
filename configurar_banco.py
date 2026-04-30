import sqlite3

# Conecta ao arquivo de banco de dados (se não existir, ele cria na hora)
conexao = sqlite3.connect('sigemp_sistema.db')
cursor = conexao.cursor()

print("Iniciando a estruturação das tabelas seguindo a LGPD...")

# 1. Tabela de Usuários (Equipe)
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL,
    senha_hash TEXT NOT NULL
)
''')

# 2. Tabela de Processos Reais (Base Segura - Dados Sensíveis)
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_processo_real (
    id_processo INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_pje TEXT NOT NULL,
    nome_autor TEXT,
    nome_reu TEXT,
    segredo_justica INTEGER DEFAULT 0
)
''')

# 3. Tabela de Minutas (Base Operacional - Pseudonimizada)
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_minuta_tarefa (
    id_minuta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_processo INTEGER,
    id_usuario INTEGER,
    codigo_ficticio TEXT NOT NULL,
    status TEXT DEFAULT 'Triagem',
    FOREIGN KEY (id_processo) REFERENCES tb_processo_real(id_processo),
    FOREIGN KEY (id_usuario) REFERENCES tb_usuario(id_usuario)
)
''')

conexao.commit()
conexao.close()
print("Banco de Dados SIGEMP configurado com sucesso!")