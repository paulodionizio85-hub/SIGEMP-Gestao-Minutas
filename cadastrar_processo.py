import sqlite3
import os
from datetime import datetime

def cadastrar_novo_processo(numero_pje, nome_autor, nome_reu):
    # 1. GARANTIR O CAMINHO CORRETO DO BANCO
    # Isso localiza a pasta onde este script está salvo
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'sigemp_sistema.db')
    
    try:
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()
        
        # 2. SALVAR NA BASE SEGURA (DADOS REAIS)
        # O nome real fica guardado apenas aqui.
        cursor.execute('''
            INSERT INTO tb_processo_real (numero_pje, nome_autor, nome_reu)
            VALUES (?, ?, ?)
        ''', (numero_pje, nome_autor, nome_reu))
        
        # Recupera o ID numérico que o banco acabou de criar
        id_gerado = cursor.lastrowid
        
        # 3. LÓGICA DE PSEUDONIMIZAÇÃO (LGPD)
        # Gera o código que a equipe verá no dia a dia.
        ano_atual = datetime.now().year
        codigo_gab = f"GAB-{ano_atual}/{id_gerado:03d}"
        
        # 4. SALVAR NA BASE OPERACIONAL (DADOS MINIMIZADOS)
        # Vinculamos ao Usuário 1 e criamos o card de 'Triagem'.
        cursor.execute('''
            INSERT INTO tb_minuta_tarefa (id_processo, id_usuario, codigo_ficticio, status)
            VALUES (?, ?, ?, ?)
        ''', (id_gerado, 1, codigo_gab, 'Triagem'))
        
        conexao.commit()
        conexao.close()
        
        print("\n" + "="*30)
        print("✅ PROCESSO REGISTRADO COM SUCESSO!")
        print(f"📍 Código para a equipe: {codigo_gab}")
        print(f"🔒 Nome real ocultado na base segura.")
        print("="*30)

    except sqlite3.OperationalError as e:
        print(f"\n❌ ERRO DE BANCO: {e}")
        print("Certifique-se de ter rodado o 'configurar_banco.py' primeiro!")

# --- INTERFACE DE TESTE NO TERMINAL ---
if __name__ == "__main__":
    print("\n--- ⚖️ CADASTRO DE PROCESSO SIGEMP ---")
    pje = input("Digite o Número do PJe: ")
    autor = input("Digite o Nome do Autor: ")
    reu = input("Digite o Nome do Réu: ")

    cadastrar_novo_processo(pje, autor, reu)