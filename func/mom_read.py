

from bs4 import BeautifulSoup
import mysql.connector
import datetime

def ordenar_po_data(dicionario:dict):
    new_str = list(dicionario["dtgerado"])
    new_str[22] = ""
    return datetime.datetime.strptime("".join(new_str),"%Y-%m-%dT%H:%M:%S%z")
def str_to_datetime(data:str):
    new_str = list(data)
    new_str[22] = ""
    return datetime.datetime.strptime("".join(new_str),"%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)

def leitura_de_arquivo_mom(arquivo_x:str):
    # with open("registros/"+arquivo_x[:-4]+".txt",'w+') as t:
    #     t.write(f"\nFILE_OPENED:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    
    caminho= 'C:/prd/'
    arquivo = caminho + arquivo_x
    # with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
    #     t.write(f"\nREAD_BEGIN:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    operadores = [] 
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
    # operadores_nos = soup.find_all('operatordefinition')
    # operacoes={"volume_total":0.0,"numero_arvores":0.0,"consumo_combustivel":0.0,"engine_time":0.0,"distancia":0.0}
    
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
        if(trabalho.harvesterdata !=None):
            nova_operacao = {}
            nova_operacao["chave_operador"]= str(trabalho.operatorkey.string)
            nova_operacao["engine_time"]=float(trabalho.enginetime.string)
            nova_operacao["distancia"]=float(trabalho.drivendistance.string)
            nova_operacao["consumo_combustivel"]=float(trabalho.fuelconsumption.string)
            nova_operacao["volume_total"]=float(trabalho.harvesterdata.find(harvestedlogsvolumecategory="m3sob").string)
            nova_operacao["numero_arvores"]=float(trabalho.harvesterdata.numberofharvestedstems.string)
            nova_operacao["dtgerado"]=str(trabalho.monitoringstarttime.string)
            operadores.append(nova_operacao)
            
    # with open("log/logmom.txt",'a+') as t:
    #     t.write(f"\n{arquivo_x[:-4]} : {str(datetime.datetime.now())}")

    # with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
    #     t.write(f"\nREAD_COMPLETED:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
   
    '''
    Ordenando os registro para qual foi o ultimo
    '''
    mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
    con = mydb.cursor()
    operadores.sort(key=ordenar_po_data)

    for operacao_registro in operadores:
        
        ultima_operacao = operacao_registro
        data_da_ultima_operacao = str_to_datetime(ultima_operacao["dtgerado"])
        '''
        Verficando se as dadas do ultimo insert e do ultimo registro coicidem:
        '''
        con.execute(f"SELECT created_at FROM smartfleet.machine_operation where created_at ='{data_da_ultima_operacao.strftime('%Y-%m-%d %H:%M:%S')}'  order by created_at desc limit 1")
        myresult =con.fetchone()
        if myresult == None:
            # with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
            #     t.write(f"\nINSERT_BEGIN:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
            
            con.execute("SELECT operador_id,id FROM smartfleet.message_sent WHERE  form_id BETWEEN 10300 AND 10399 OR form_id BETWEEN 10700 AND 10799 OR form_id BETWEEN 11300 AND 11399 order by create_date desc limit 1")
            myresult =con.fetchone()
            if myresult:
                operador_ultima_apropriacao = myresult[0]
                id_ultima_desapropriacao = myresult[1]
                try:
                    sql = "INSERT INTO smartfleet.machine_operation(operator_id,message_sent_id,total_volume,harvestedstems,fuelconsumption,enginetime,drivendistance,machine_enginetime,machine_drivendistance,machine_fuelconsumption,created_at)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    val = (str(operador_ultima_apropriacao),str(id_ultima_desapropriacao),str(operacao_registro['volume_total']),str(operacao_registro['numero_arvores']),str(operacao_registro['consumo_combustivel']),str(operacao_registro['engine_time']),str(operacao_registro['distancia']),str(total_da_maquina['machineenginetime']),str(total_da_maquina['machinedrivendistance']),str(total_da_maquina['machinefuelconsumption']),data_da_ultima_operacao)
                    con.execute(sql,val)
                    mydb.commit()
                    
                except mysql.connector.Error as err:
                    pass
                    # t.write(f"\nINSERT_ERROR:{arquivo_x[:-4]} : {err}")
                # with open("registros/"+arquivo_x[:-4]+".txt",'a+') as t:
                #     t.write(f"\nINSERT_COMPLETED:{arquivo_x[:-4]} : {str(datetime.datetime.now())}")
    
    mydb.close()
