import logging
import os
import azure.functions as func
import pyodbc


bp = func.Blueprint()

@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer",
                   run_on_startup=False, use_monitor=False)
def extract_fornecedor(myTimer: func.TimerRequest) -> None:
        
    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_pass = os.getenv("SQL_PASSWORD_SOURCE")
        
    sql_server_aluno = os.getenv("SQL_SERVER_SOURCE_ALUNO")
    sql_database_aluno = os.getenv("SQL_DATABASE_SOURCE_ALUNO")
    sql_user_aluno = os.getenv("SQL_USER_SOURCE_ALUNO")
    sql_pass_aluno = os.getenv("SQL_PASSWORD_SOURCE_ALUNO")

    logging.info(f'Banco de dados do Professor:')
    logging.info(f'Servidor: {sql_server}, \nDatabase: {sql_database}, \nUsuário: {sql_user}, \nSenha: {sql_pass}')

    logging.info(f'Banco de dados do Aluno:')
    logging.info(f'Servidor: {sql_server_aluno}, \nDatabase: {sql_database_aluno}, \nUsuário: {sql_user_aluno}, \nSenha: {sql_pass_aluno}')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    conn_str_aluno = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server_aluno};"
        f"DATABASE={sql_database_aluno};"
        f"UID={sql_user_aluno};"
        f"PWD={sql_pass_aluno};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )



    with pyodbc.connect(conn_str) as conn_origem, \
        pyodbc.connect(conn_str_aluno) as conn_destino:

        cursor_origem = conn_origem.cursor()
        cursor_destino = conn_destino.cursor()

        cursor_destino.fast_executemany = True

        # Lista todas as tabelas do banco origem
        cursor_origem.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)

        tabelas = cursor_origem.fetchall()

        for schema, tabela in tabelas:

            nome_completo = f"[{schema}].[{tabela}]"

            logging.info(f"Processando {nome_completo}")

            try:

                # Busca os dados
                cursor_origem.execute(
                    f"SELECT * FROM {nome_completo}"
                )

                colunas = [
                    coluna[0]
                    for coluna in cursor_origem.description
                ]

                placeholders = ",".join(
                    ["?"] * len(colunas)
                )

                insert_sql = f"""
                    SET IDENTITY_INSERT [dbo].[{tabela}] ON
                    
                    INSERT INTO [dbo].[{tabela}]
                    ({",".join(f'[{c}]' for c in colunas)})
                    VALUES ({placeholders})
                    
                    SET IDENTITY_INSERT [dbo].[{tabela}] OFF
                """

                total = 0

                while True:

                    rows = cursor_origem.fetchmany(1000)

                    if not rows:
                        break

                    cursor_destino.executemany(
                        insert_sql,
                        rows
                    )

                    conn_destino.commit()

                    total += len(rows)

                logging.info(
                    f"{total} registros copiados para {nome_completo}"
                )

            except Exception as e:
                logging.error(
                    f"Erro ao copiar {nome_completo}: {e}"
                )