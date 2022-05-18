

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
    caminho= 'C:/prd/'
    arquivo = caminho + arquivo_x
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
   
    '''
    Ordenando os registro para qual foi o ultimo
    '''
    operadores.sort(key=ordenar_po_data)
    for x in operadores:
        print(x)


leitura_de_arquivo_mom('9112062609_20220412_170229.mom')