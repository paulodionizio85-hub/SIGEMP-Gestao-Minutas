import sqlite3
import os

def visualizar_quadro_equipe():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'sigemp_sistema.db')
    
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    
    # Busca apenas os dados OPERACIONAIS (Minimizados)
    cursor.execute("SELECT codigo_ficticio, status FROM tb_minuta_tarefa")
    tarefas = cursor.fetchall()
    
    print("\n" + "="*40)
    print("📋 QUADRO DE TAREFAS - VISTA OPERACIONAL")
    print(f"{'CÓDIGO GAB':<15} | {'SITUAÇÃO ATUAL':<15}")
    print("-" * 40)
    
    if not tarefas:
        print("Nenhuma tarefa pendente no momento.")
    else:
        for t in tarefas:
            print(f"{t[0]:<15} | {t[1]:<15}")
            
    print("="*40)
    print("🔒 LGPD: Nomes das partes ocultados nesta vista.")
    conexao.close()

if __name__ == "__main__":
    visualizar_quadro_equipe()