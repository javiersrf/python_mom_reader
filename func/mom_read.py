
from os import error,remove
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from logfunc.logfunc import log



def leitura_de_arquivo_mom(arquivo_x:str):
    with open("registros/"+arquivo_x[:-4]+".txt",'w+') as t:
        t.write(f"\nFILE_OPENED:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
    caminho= 'C:/prd/'
    arquivo = caminho + arquivo_x
    with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
        t.write(f"\nREAD_BEGIN:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    operadores = {}
    operacoes = {}
    total_da_maquina = {}
    '''
    Aqui abrimos o caminho passado como uma  arquivo para o python conseguir interpreta-lo
    '''
    with open(arquivo, 'r',encoding="utf8") as xml_file: 
        data = xml_file.read()
    '''
    Com o bs4, podemos interpretar o arquivo xml como uma classe python
    '''
    soup = BeautifulSoup(data, "lxml")
    '''
    pegando informação da maquina / #Nó da máquina
    '''
    no_maquina = soup.machine
    '''
    registrando os operadorres
    '''
    operadores_nos = soup.find_all('operatordefinition')
    # for op in operadores_nos:
    operacoes={"volume_total":0.0,"numero_arvores":0.0,"consumo_combustivel":0.0,"engine_time":0.0,"distancia":0.0}
        
    '''
    valores totais da maquina
    '''
    total_da_maquina["machineenginetime"] =soup.find('machineenginetime').string
    total_da_maquina["machinedrivendistance"] =soup.find('machinedrivendistance').string
    total_da_maquina["machinefuelconsumption"] =soup.find('machinefuelconsumption').string
    no_trabalho_realizado = soup.find_all("individualmachineworktime")
    '''
    valores de trabalho do operador
    '''
    for trabalho in no_trabalho_realizado:
        operacoes["engine_time"]+=float(trabalho.enginetime.string)
        operacoes["distancia"]+=float(trabalho.drivendistance.string)
        operacoes["consumo_combustivel"]+=float(trabalho.fuelconsumption.string)
        if(trabalho.harvesterdata !=None):
            operacoes["volume_total"]+=float(trabalho.harvesterdata.find(harvestedlogsvolumecategory="m3sob").string)
            operacoes["numero_arvores"]+=float(trabalho.harvesterdata.numberofharvestedstems.string)
    



    with open("log/logmom.txt",'a+') as t:
        t.write(f"\n{arquivo_x[:-4]} : {str(datetime.datetime.now())}")

    with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
        t.write(f"\nREAD_COMPLETED:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")

    '''
    Selecionando o código do ultimo operador  (última apropriação)
    '''
    with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
        t.write(f"\nINSERT_BEGIN:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    con = mydb.cursor()
    con.execute("SELECT operador_id FROM smartfleet.message_sent WHERE  form_id BETWEEN 10300 AND 10399 OR form_id BETWEEN 10700 AND 10799 OR form_id BETWEEN 11300 AND 11399 order by create_date desc limit 1")
    myresult =con.fetchone()
    if myresult:
        operador_ultima_apropriacao = myresult[0]
           
   
    try:
        sql = "INSERT INTO smartfleet.machine_operation(operador_id,volume_total,quantidade_arvores,cons_combus,temp_motor,distancia,temp_motor_maquina,distancia_maquina,cons_combus_maquina,create_date)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,SYSDATE());"
        val = (str(operador_ultima_apropriacao),str(operacoes['volume_total']),str(operacoes['numero_arvores']),str(operacoes['consumo_combustivel']),str(operacoes['engine_time']),str(operacoes['distancia']),str(total_da_maquina['machineenginetime']),str(total_da_maquina['machinedrivendistance']),str(total_da_maquina['machinefuelconsumption']))
        con = mydb.cursor()
        con.execute(sql,val)
        mydb.commit()
        mydb.close()
    except mysql.connector.Error as err:
        log("INSERT_ERROR:"+err.msg)
    with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
        t.write(f"\nINSERT_COMPLETED:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    remove(arquivo)
# leitura_de_arquivo_mom('C:/Users/Javier Ferreira/Desktop/mom/','FLORESTAL_BARRA_01-060122-180129.mom')