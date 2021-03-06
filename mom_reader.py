from func.mom_read import leitura_de_arquivo_mom
from func.buscador_de_arquivos import get_arquivo_mom
import sched, time


event_schedule = sched.scheduler(time.time, time.sleep)



def app():
    '''
    criar tabela para registro caso nao haja uma
    '''
    # Funcao que verifica quais arquivos devem ser lidos e tradados
    # aqui devera ser implementado a funcao que define se o arquivo é novo ou não
    arquivo_mom_valido = get_arquivo_mom()
    if arquivo_mom_valido:
        for x in arquivo_mom_valido:
            leitura_de_arquivo_mom(x)
    
    event_schedule.enter(25, 1, app,)
   
    
event_schedule.enter(10, 1, app,)
event_schedule.run()