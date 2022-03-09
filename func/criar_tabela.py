import mysql.connector
from logfunc.logfunc import log
import os
def criar_tabela_caso_nao_exista():
    if not os.path.exists('C:/prd'):
        os.mkdir('C:/prd')
    if not os.path.exists('./registros'):
        os.mkdir('./registros')
    if not os.path.exists('./log'):
        os.mkdir('./log')
    try:
        mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
        con = mydb.cursor()
        con.execute("CREATE TABLE machine_operation(  id BIGINT NOT NULL AUTO_INCREMENT,operator_id BIGINT NOT NULL,message_sent_id BIGINT NULL, total_volume FLOAT NULL DEFAULT 0,harvestedstems INT NULL DEFAULT 0.0,fuelconsumption FLOAT NULL DEFAULT 0.0,enginetime FLOAT NULL DEFAULT 0.0, drivendistance FLOAT NULL DEFAULT 0.0, machine_enginetime FLOAT NULL DEFAULT 0.0,  machine_drivendistance FLOAT NULL DEFAULT 0.0, machine_fuelconsumption FLOAT NULL DEFAULT 0.0, created_at DATETIME NOT NULL, sent tinyint DEFAULT FALSE, PRIMARY KEY (id));")
        mydb.close()
    except mysql.connector.Error as err:
        log("ERROR_CRIAR_TABELA:"+err.msg)
