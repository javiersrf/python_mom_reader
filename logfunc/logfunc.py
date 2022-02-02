from datetime import datetime
def log(mensagem:str):
    with open("log.txt","a") as f:
        f.write(mensagem+f"\nlog {datetime.now()}\n")