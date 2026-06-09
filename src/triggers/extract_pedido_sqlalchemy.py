import logging
import os
import time
import azure.functions as func

from sqlalchemy import create_engine
from sqlalchemy import text

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer",
                   run_on_startup=False, use_monitor=False)
def extract_pedido_sqlalchemy(myTimer: func.TimerRequest) -> None:
        
    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_pass = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info(f'Servidor: {sql_server}, \nDatabase: {sql_database}, \nUsuário: {sql_user}, \nSenha: {sql_pass}')

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        f"mssql+pyodbc://{sql_user}:{sql_pass}"
        f"@{sql_server}/{sql_database}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&Encrypt=yes"
        "&TrustServerCertificate=no"
    )

    tempos = []

    try:

        engine = create_engine(conn_str)

        # Executa o teste 2 vezes
        for i in range(2):

            inicio = time.perf_counter()

            # Estabelece a conexão com o banco de dados usando SQLAlchemy
            with engine.connect() as conn:

                query = "select top 5 * from erp.pedido_item"

                # Executa a consulta SQL
                resultado = conn.execute(
                    text(query)
                )

                # Busca todos os resultados da consulta
                rows = resultado.fetchall()

            fim = time.perf_counter()

            tempo = fim - inicio

            tempos.append(tempo)

            logging.info(
                f"SQLAlchemy - Execução {i+1}: {tempo:.6f} segundos & Registros retornados: {len(rows)}"
            )

        media = sum(tempos) / len(tempos)

        logging.info(
            f"SQLAlchemy - Tempo médio: {media:.6f} segundos"
        )

    except Exception as e:
        logging.error(f"Erro ao ler erp.pedido: {str(e)}")
        raise