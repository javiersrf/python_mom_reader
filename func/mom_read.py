from bs4 import BeautifulSoup
import mysql.connector
import datetime
import os
import logging
from .env import LOG_LOCAL, MAIN_LOCAL, M3, DATABASE, DATABASE_PASSWORD, HOST, USER


def ordenar_por_data(dicionario:dict):
    new_str = list(dicionario["dtgerado"])
    new_str[22] = ""
    return datetime.datetime.strptime("".join(new_str),"%Y-%m-%dT%H:%M:%S%z")

def str_to_datetime(data:str):
    new_str = list(data)
    new_str[22] = ""
    return datetime.datetime.strptime("".join(new_str),"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)

def leitura_de_arquivo_mom(arquivo_x:str):
    logging.basicConfig(filename = LOG_LOCAL + arquivo_x[:-3] + 'txt', format= '%(asctime)s|%(levelname)s|%(message)s|', filemode='+a', level=logging.DEBUG)
    logging.info("Init reading of file " + arquivo_x)
    caminho= MAIN_LOCAL
    arquivo = caminho + arquivo_x
    operadores = [] 
    total_da_maquina = {}
    logging.info("Checking for mysql connection")
    try:
        mydb = mysql.connector.connect(host=HOST, user=USER, password=DATABASE_PASSWORD, database=DATABASE)
        con = mydb.cursor()
        sql = "UPDATE smartfleet.reading_status SET read_mom_status = 1, updated_at = current_date() where 1=1;"
        con.execute(sql)
        mydb.commit()
        mydb.close()
    except Exception as excpt:
        logging.error("Mysql connection error")
        logging.exception(msg= excpt)
 
    '''
    Aqui abrimos o caminho passado como uma  arquivo para o python conseguir interpreta-lo
    '''
    logging.info("Opening mom file")
    try:
        with open(arquivo, 'r',encoding="utf8") as xml_file: 
            data = xml_file.read()
    except Exception as excpt:
        logging.error("Error opening mom file")
        logging.exception(msg= excpt)
    '''
    Com o bs4, podemos interpretar o arquivo xml como uma classe python
    '''
    logging.info("Passing mom data with BS4")
    try:
        soup = BeautifulSoup(data, "lxml")
    except Exception as excpt:
        logging.error("Error opening mom file")
        logging.exception(msg= excpt)
    '''
    pegando informação da maquina / #Nó da máquina
    '''
    '''
    registrando os operadorres
    '''
    '''
    valores totais da maquina
    '''
    logging.info("Getting machine data")
    total_da_maquina["machineenginetime"] = soup.find('machineenginetime').string
    total_da_maquina["machinedrivendistance"] = soup.find('machinedrivendistance').string
    total_da_maquina["machinefuelconsumption"] = soup.find('machinefuelconsumption').string

    logging.info("machineenginetime :" + total_da_maquina["machineenginetime"])
    logging.info("machinedrivendistance :" + total_da_maquina["machinedrivendistance"])
    logging.info("machinefuelconsumption :" + total_da_maquina["machinefuelconsumption"])
    
    no_trabalho_realizado = soup.find_all("individualmachineworktime")
    logging.info("individualmachineworktime size: " + str(len(no_trabalho_realizado)))
    '''
    valores de trabalho do operador
    '''
    for trabalho in no_trabalho_realizado:
        if(trabalho.harvesterdata != None):
            try:
                nova_operacao = {}
                nova_operacao["chave_operador"]= str(trabalho.operatorkey.string)
                nova_operacao["engine_time"]=float(trabalho.enginetime.string)
                nova_operacao["distancia"]=float(trabalho.drivendistance.string)
                nova_operacao["consumo_combustivel"]=float(trabalho.fuelconsumption.string)
                nova_operacao["volume_total"]=float(trabalho.harvesterdata.find(harvestedlogsvolumecategory = M3).string)
                nova_operacao["numero_arvores"]=float(trabalho.harvesterdata.numberofharvestedstems.string)
                nova_operacao["dtgerado"]=str(trabalho.monitoringstarttime.string)
                operadores.append(nova_operacao)
            except Exception as excpt:
                logging.error("Error reading individual machine work time")
                logging.exception(msg= excpt)
        else:
            logging.debug('No harvester data found')
            
   
    '''
    Ordenando os registro para qual foi o ultimo
    '''
    logging.info("opening new connection in mysql")
    try:
        mydb = mysql.connector.connect(host=HOST, user=USER, password=DATABASE_PASSWORD, database=DATABASE)
        con = mydb.cursor()
        if operadores:
            operadores.sort(key=ordenar_por_data)
    except Exception as excpt:
        logging.error("New Mysql connection error")
        logging.exception(msg= excpt)
    
    logging.info("Starting insert database info")
    for operacao_registro in operadores:
        ultima_operacao = operacao_registro
        data_da_ultima_operacao = str_to_datetime(ultima_operacao["dtgerado"])
        logging.info("Getting last operation data info: " + data_da_ultima_operacao.strftime('%Y-%m-%d %H:%M:%S'))
        '''
        Verficando se as dadas do ultimo insert e do ultimo registro coicidem:
        '''
        con.execute(f"SELECT created_at FROM smartfleet.machine_operation where created_at ='{data_da_ultima_operacao.strftime('%Y-%m-%d %H:%M:%S')}' order by created_at desc limit 1;")
        myresult =con.fetchone()
        logging.info("Checking if register already exists in table: " + str(myresult == None))
        if myresult == None:     
            con.execute("SELECT operador_id,id FROM smartfleet.message_sent WHERE  form_id BETWEEN 10300 AND 10399 OR form_id BETWEEN 10700 AND 10799 OR form_id BETWEEN 11300 AND 11399 order by create_date desc limit 1")
            logging.info("Checking last operator apropriation id")
            myresult_operador =con.fetchone()
            if myresult_operador:
                operador_ultima_apropriacao = myresult_operador[0]
                id_ultima_desapropriacao = myresult_operador[1]
                logging.info("Last operator apropriation id: " + str(operador_ultima_apropriacao))
                try:
                    sql = "INSERT INTO smartfleet.machine_operation(operator_id,message_sent_id,total_volume,harvestedstems,fuelconsumption,enginetime,drivendistance,machine_enginetime,machine_drivendistance,machine_fuelconsumption,created_at)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    val = (str(operador_ultima_apropriacao),str(id_ultima_desapropriacao),str(operacao_registro['volume_total']),str(operacao_registro['numero_arvores']),str(operacao_registro['consumo_combustivel']),str(operacao_registro['engine_time']),str(operacao_registro['distancia']),str(total_da_maquina['machineenginetime']),str(total_da_maquina['machinedrivendistance']),str(total_da_maquina['machinefuelconsumption']),data_da_ultima_operacao)
                    con.execute(sql,val)
                    mydb.commit()
                except mysql.connector.Error as excpt:
                    logging.error("Error inserting machine_operation data ")
                    logging.exception(msg= excpt)
            else:
                logging.info("Any last operator apropriation")
    logging.info("Ending insert database info")
    sql = "UPDATE smartfleet.reading_status SET read_mom_status = 0, updated_at = current_date() where 1=1;"
    try:
        con.execute(sql)
        mydb.commit()
        mydb.close()
    except Exception as excpt:
        logging.error("Error closing status reading of mom file")
        logging.exception(msg= excpt)
    try:
        os.remove(arquivo)
    except Exception as excpt:
        logging.error("Error on remove mom file")
        logging.exception(msg= excpt)
    finally:
        logging.info("Ending reading mom file")


