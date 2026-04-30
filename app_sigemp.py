import streamlit as st
import sqlite3
import os
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO E CONEXÃO COM BANCO DE DADOS
# ==========================================
def conectar_banco():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'sigemp_sistema.db')
    conexao = sqlite3.connect(caminho_banco)
    
    # Garante que as tabelas existam logo ao abrir o app
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tb_usuario (id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, nome_usuario TEXT NOT NULL, senha_hash TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tb_processo_real (id_processo INTEGER PRIMARY KEY AUTOINCREMENT, numero_pje TEXT NOT NULL, nome_autor TEXT, nome_reu TEXT, segredo_justica INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tb_minuta_tarefa (id_minuta INTEGER PRIMARY KEY AUTOINCREMENT, id_processo INTEGER, id_usuario INTEGER, codigo_ficticio TEXT NOT NULL, status TEXT DEFAULT 'Triagem', FOREIGN KEY (id_processo) REFERENCES tb_processo_real(id_processo), FOREIGN KEY (id_usuario) REFERENCES tb_usuario(id_usuario))''')
    conexao.commit()
    
    return conexao

# ==========================================
# 2. LÓGICA DE NEGÓCIO (BACKEND)
# ==========================================
def cadastrar_processo(numero_pje, nome_autor, nome_reu):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Salva na Base Segura
    cursor.execute('INSERT INTO tb_processo_real (numero_pje, nome_autor, nome_reu) VALUES (?, ?, ?)', (numero_pje, nome_autor, nome_reu))
    id_gerado = cursor.lastrowid
    
    # Lógica LGPD: Pseudonimização
    ano_atual = datetime.now().year
    codigo_gab = f"GAB-{ano_atual}/{id_gerado:03d}"
    
    # Salva na Base Operacional
    cursor.execute('INSERT INTO tb_minuta_tarefa (id_processo, id_usuario, codigo_ficticio, status) VALUES (?, ?, ?, ?)', (id_gerado, 1, codigo_gab, 'Triagem'))
    
    conexao.commit()
    conexao.close()
    return codigo_gab

def buscar_tarefas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    # Busca apenas tarefas que AINDA NÃO foram concluídas
    cursor.execute("SELECT codigo_ficticio, status FROM tb_minuta_tarefa WHERE status != 'Concluído'")
    tarefas = cursor.fetchall()
    conexao.close()
    return tarefas

def atualizar_status(codigo, novo_status):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE tb_minuta_tarefa 
        SET status = ? 
        WHERE codigo_ficticio = ?
    ''', (novo_status, codigo))
    conexao.commit()
    conexao.close()

# ==========================================
# 3. CAMADA DE APRESENTAÇÃO (FRONTEND - WEB)
# ==========================================
st.set_page_config(page_title="SIGEMP - TJDFT", layout="wide")
st.title("⚖️ SIGEMP - Gestão de Minutas")
st.markdown("**Visão Operacional (LGPD Ativa)** - *Nomes ocultos na interface*")

# --- BARRA LATERAL (CADASTRO) ---
with st.sidebar:
    st.header("📥 Novo Processo")
    # ATUALIZAÇÃO: clear_on_submit=True garante a limpeza dos dados sensíveis após o envio
    with st.form("form_cadastro", clear_on_submit=True):
        pje_input = st.text_input("Número do PJe")
        autor_input = st.text_input("Nome do Autor (Sigiloso)")
        reu_input = st.text_input("Nome do Réu (Sigiloso)")
        submit = st.form_submit_button("Cadastrar e Pseudonimizar")
        
        if submit and pje_input:
            codigo = cadastrar_processo(pje_input, autor_input, reu_input)
            st.success(f"GAB-ID: {codigo} criado!")
            st.rerun()

# --- ABAS PRINCIPAIS DA APLICAÇÃO ---
aba_kanban, aba_estatisticas = st.tabs(["📋 Quadro Kanban", "📊 Estatísticas e Arquivo"])

# --- ABA 1: QUADRO KANBAN ---
with aba_kanban:
    tarefas = buscar_tarefas()

    if not tarefas:
        st.info("🎉 Nenhuma tarefa pendente no gabinete! Tudo em dia.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📥 Triagem")
            for t in tarefas:
                if t[1] == 'Triagem':
                    with st.container(border=True):
                        st.markdown(f"📄 **{t[0]}**")
                        if st.button("▶️ Iniciar Minuta", key=f"btn_ini_{t[0]}"):
                            atualizar_status(t[0], 'Fazendo')
                            st.rerun()
                    
        with col2:
            st.subheader("⚙️ Fazendo")
            for t in tarefas:
                if t[1] == 'Fazendo':
                    with st.container(border=True):
                        st.markdown(f"✍️ **{t[0]}**")
                        if st.button("⏩ Enviar p/ Revisão", key=f"btn_rev_{t[0]}"):
                            atualizar_status(t[0], 'Revisão')
                            st.rerun()
                    
        with col3:
            st.subheader("✅ Em Revisão")
            for t in tarefas:
                if t[1] == 'Revisão':
                    with st.container(border=True):
                        st.markdown(f"🔎 **{t[0]}**")
                        if st.button("✔️ Finalizar", key=f"btn_fin_{t[0]}"):
                            atualizar_status(t[0], 'Concluído')
                            st.rerun()

# --- ABA 2: ESTATÍSTICAS E ARQUIVO ---
with aba_estatisticas:
    st.subheader("Desempenho do Gabinete")
    
    # Busca dados agrupados no banco
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM tb_minuta_tarefa GROUP BY status")
    dados_stats = cursor.fetchall()
    
    # Prepara o dicionário com valores zerados por padrão
    stats_dict = {'Triagem': 0, 'Fazendo': 0, 'Revisão': 0, 'Concluído': 0}
    for item in dados_stats:
        stats_dict[item[0]] = item[1]
        
    # Exibe as métricas no topo
    col_st1, col_st2, col_st3, col_st4 = st.columns(4)
    col_st1.metric("Na Triagem", stats_dict['Triagem'])
    col_st2.metric("Em Elaboração", stats_dict['Fazendo'])
    col_st3.metric("Em Revisão", stats_dict['Revisão'])
    col_st4.metric("✔️ Total Concluído", stats_dict['Concluído'])
    
    st.divider()
    
    # Busca apenas os concluídos para exibir no histórico
    st.subheader("🗄️ Arquivo de Processos Finalizados")
    cursor.execute("SELECT codigo_ficticio FROM tb_minuta_tarefa WHERE status = 'Concluído'")
    concluidos = cursor.fetchall()
    conexao.close()
    
    if concluidos:
        for c in concluidos:
            st.success(f"Processo {c[0]} finalizado e arquivado.")
    else:
        st.info("Nenhum processo arquivado ainda.")