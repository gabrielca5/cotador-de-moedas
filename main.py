import requests
import pandas as pd

class Conversor():
    def __init__(self, moeda_base ):
        self.url_base = "https://v6.exchangerate-api.com/v6/"
        self.chave = '9ea76630365566ebd22f032e'
        self.moeda_base = moeda_base
        self.url_final = f"{self.url_base}{self.chave}/latest/{self.moeda_base}"
    
    def obter_dados(self): 
        try:
            resposta = requests.get(self.url_final)    
            resposta.raise_for_status()
            return resposta.json()
        except requests.exceptions.HTTPError as erro_http:
            print(f"\nOcorreu um erro de HTTP: {erro_http}")
            print(f"Código de Status: {resposta.status_code}")
            print("Verifique se a sua chave de API está correta e se a URL foi montada certo.")
    
    
    def obter_taxa(self , moeda_alvo :str):
        dados = self.obter_dados() 
        if dados and 'conversion_rates' in dados:
            taxa = dados['conversion_rates'].get(moeda_alvo.upper())
            return taxa
        
    
    def mostrar_tabela(self):
        dados = self.obter_dados()
        if dados and 'conversion_rates' in dados:
            df = pd.DataFrame.from_dict(
                dados['conversion_rates'] ,
                orient= 'index' , 
                columns= ['Taxa']
            )
            print(df)
        else:
            print('Não foi possivel encontrar os dados de conversão')
            
        

    
    
            


Conversor = Conversor(moeda_base = 'USD')
Conversor.mostrar_tabela()

