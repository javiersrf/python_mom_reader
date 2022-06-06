import os
import mysql.connector
from .env import LOG_LOCAL, MAIN_LOCAL
class CaminhoDoArquivo:
    def __init__(self,caminho,data_criado,data_atualizado):
        self.caminho = caminho
        self.data_criada = data_criado
        self.data_atualizado = data_atualizado
    def __str__(self):
        return self.caminho+ "->"+ str(self.data_atualizado)
    def __repr__(self):
        return self.caminho+ "->"+ str(self.data_atualizado)


def get_arquivos_hpr(caminho:str):
    resultado = []
    arquivos =os.listdir(caminho)
    
    for arquivo in arquivos:
        if arquivo.endswith(".hpr") and (not os.path.exists(f"{arquivo[:-4]}.log")):
            resultado.append(arquivo)
        

    return resultado 
def my_func(e):
  return e.data_atualizado
def get_arquivo_mom():
    if not os.path.isdir(LOG_LOCAL):
        os.makedirs(LOG_LOCAL)
    try:
        mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
        con = mydb.cursor()
        sql_1 = "SELECT read_mom_status FROM smartfleet.reading_status ORDER BY updated_at DESC LIMIT 1;"
        con.execute(sql_1)
        status_de_leitura = con.fetchone()
        if status_de_leitura !=None and status_de_leitura[0] == 1:
            return None
        mydb.close()
    except Exception as e:
        return None
    caminho = MAIN_LOCAL
    resultado = []
    arquivos =os.listdir(caminho)
    
    for arquivo in arquivos:
        data_criacao = os.path.getctime(caminho+arquivo)
        data_atualizado = os.path.getmtime(caminho+arquivo)
        if arquivo.endswith(".mom") :
            resultado.append(CaminhoDoArquivo(caminho=arquivo,data_criado=data_criacao,data_atualizado=data_atualizado))
    resultado.sort(key=my_func,reverse=True,)
    if resultado:
        return [result.caminho for result in resultado]
    return None 

