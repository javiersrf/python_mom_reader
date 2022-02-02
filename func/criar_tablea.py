import mysql.connector
from logfunc.logfunc import log
import os
def criar_tabela_caso_nao_exista():
    if not os.path.exists('prd'):
        os.mkdir('prd')
    if not os.path.exists('./registros'):
        os.mkdir('./registros')
    if not os.path.exists('./log'):
        os.mkdir('./log')
    try:
        mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
        con = mydb.cursor()
        con.execute("CREATE TABLE IF NOT EXISTS smartfleet.machine_operation(id BIGINT NOT NULL AUTO_INCREMENT,operador_id BIGINT NOT NULL,volume_total FLOAT NULL DEFAULT 0, quantidade_arvores INT NULL DEFAULT 0.0, cons_combus FLOAT NULL DEFAULT 0.0, temp_motor FLOAT NULL DEFAULT 0.0,distancia FLOAT NULL DEFAULT 0.0, temp_motor_maquina FLOAT NULL DEFAULT 0.0, distancia_maquina FLOAT NULL DEFAULT 0.0, cons_combus_maquina FLOAT NULL DEFAULT 0.0, create_date DATETIME NOT NULL,PRIMARY KEY (id));")
        mydb.close()
    except mysql.connector.Error as err:
        log("ERROR_CRIAR_TABELA:"+err.msg)
