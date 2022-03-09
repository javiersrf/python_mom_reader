import os
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
def myFunc(e):
  return e.data_atualizado
def get_arquivo_mom():
    caminho = 'C:/prd/'
    resultado = []
    arquivos =os.listdir(caminho)
    
    for arquivo in arquivos:
        data_criacao = os.path.getctime(caminho+arquivo)
        data_atualizado = os.path.getmtime(caminho+arquivo)
        if arquivo.endswith(".mom") :
            resultado.append(CaminhoDoArquivo(caminho=arquivo,data_criado=data_criacao,data_atualizado=data_atualizado))
    resultado.sort(key=myFunc,reverse=True,)
    if resultado:
        return [result.caminho for result in resultado]
    return None 

