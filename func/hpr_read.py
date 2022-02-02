



from os import error
from bs4 import BeautifulSoup
from datetime import datetime
from MySQLdb import _mysql




def leitura_de_arquivo_hpr(caminho:str,arquivo_x:str):
    arquivo = caminho + arquivo_x
    tipo_arvores = {}
    resultado_para_dtframe = []



    #Aqui abrimos o caminho passado como uma  arquivo para o python conseguir interpreta-lo
    with open(arquivo, 'r',encoding="utf8") as xml_file:
        data = xml_file.read()

    
    #Com o bs4, podemos interpretar o arquivo xml como uma classe python
    soup = BeautifulSoup(data, "lxml")
    

    #pegando informação da maquina / #Nó da máquina
    no_maquina = soup.machine
    
    operadores = {}

    ##registrando os operadorres
    operadores_nos = soup.find_all('operatordefinition')
    for op in operadores_nos:
        operadores[op.operatorkey.string]={"nome":op.contactinformation.firstname.string,"numero_arvores":0,"volume_arvores":0.0}


    arvores = soup.find_all('stem')

    for arvore_no in arvores:
        operadores[arvore_no.operatorkey.string]["numero_arvores"] +=1
        logs = arvores[0].find_all('log')
        for log_no in logs:
            for volume_no in log_no.find_all('logvolume'):
                if(volume_no["logvolumecategory"]=="m3 (price)"):
                    operadores[arvore_no.operatorkey.string]["volume_arvores"] +=float(volume_no.string)

    for registro in operadores.keys():
        resultado_para_dtframe.append(
        [registro,
        operadores[registro]["nome"],
        operadores[registro]["numero_arvores"],
        operadores[registro]["volume_arvores"],])
    with  open(f'./log/{arquivo_x[:-4]}.log',"w+") as t:
        t.write(str(datetime.now()))
    
leitura_de_arquivo_hpr('C:/Users/Javier Ferreira/Desktop/hprs/','HV10004_F0153_T003-150621-133335@06072021052312_15.hpr')