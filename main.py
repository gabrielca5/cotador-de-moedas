import requests
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dicionário com nomes das moedas em português
NOMES_MOEDAS = {
    'AED': 'Dirham dos Emirados Árabes Unidos',
    'AFN': 'Afegani Afegão',
    'ALL': 'Lek Albanês',
    'AMD': 'Dram Armênio',
    'ANG': 'Florim das Antilhas Holandesas',
    'AOA': 'Kwanza Angolano',
    'ARS': 'Peso Argentino',
    'AUD': 'Dólar Australiano',
    'AWG': 'Florim de Aruba',
    'AZN': 'Manat Azerbaijano',
    'BAM': 'Marco Conversível da Bósnia-Herzegovina',
    'BBD': 'Dólar de Barbados',
    'BDT': 'Taka de Bangladesh',
    'BGN': 'Lev Búlgaro',
    'BHD': 'Dinar do Bahrein',
    'BIF': 'Franco do Burundi',
    'BMD': 'Dólar das Bermudas',
    'BND': 'Dólar de Brunei',
    'BOB': 'Boliviano',
    'BRL': 'Real Brasileiro',
    'BSD': 'Dólar das Bahamas',
    'BTN': 'Ngultrum do Butão',
    'BWP': 'Pula de Botswana',
    'BYN': 'Rublo Bielorrusso',
    'BZD': 'Dólar de Belize',
    'CAD': 'Dólar Canadense',
    'CDF': 'Franco Congolês',
    'CHF': 'Franco Suíço',
    'CLP': 'Peso Chileno',
    'CNY': 'Yuan Chinês',
    'COP': 'Peso Colombiano',
    'CRC': 'Colón da Costa Rica',
    'CUP': 'Peso Cubano',
    'CVE': 'Escudo de Cabo Verde',
    'CZK': 'Coroa Tcheca',
    'DJF': 'Franco do Djibuti',
    'DKK': 'Coroa Dinamarquesa',
    'DOP': 'Peso Dominicano',
    'DZD': 'Dinar Argelino',
    'EGP': 'Libra Egípcia',
    'ERN': 'Nakfa da Eritreia',
    'ETB': 'Birr Etíope',
    'EUR': 'Euro',
    'FJD': 'Dólar de Fiji',
    'FKP': 'Libra das Ilhas Falkland',
    'FOK': 'Coroa das Ilhas Faroe',
    'GBP': 'Libra Esterlina',
    'GEL': 'Lari Georgiano',
    'GGP': 'Libra de Guernsey',
    'GHS': 'Cedi de Gana',
    'GIP': 'Libra de Gibraltar',
    'GMD': 'Dalasi da Gâmbia',
    'GNF': 'Franco da Guiné',
    'GTQ': 'Quetzal Guatemalteco',
    'GYD': 'Dólar da Guiana',
    'HKD': 'Dólar de Hong Kong',
    'HNL': 'Lempira de Honduras',
    'HRK': 'Kuna Croata',
    'HTG': 'Gourde Haitiano',
    'HUF': 'Forint Húngaro',
    'IDR': 'Rupia Indonésia',
    'ILS': 'Novo Shekel Israelense',
    'IMP': 'Libra da Ilha de Man',
    'INR': 'Rupia Indiana',
    'IQD': 'Dinar Iraquiano',
    'IRR': 'Rial Iraniano',
    'ISK': 'Coroa Islandesa',
    'JEP': 'Libra de Jersey',
    'JMD': 'Dólar Jamaicano',
    'JOD': 'Dinar Jordaniano',
    'JPY': 'Iene Japonês',
    'KES': 'Xelim Queniano',
    'KGS': 'Som Quirguiz',
    'KHR': 'Riel Cambojano',
    'KMF': 'Franco Comorense',
    'KPW': 'Won Norte-Coreano',
    'KRW': 'Won Sul-Coreano',
    'KWD': 'Dinar Kuwaitiano',
    'KYD': 'Dólar das Ilhas Cayman',
    'KZT': 'Tenge Cazaque',
    'LAK': 'Kip Laosiano',
    'LBP': 'Libra Libanesa',
    'LKR': 'Rupia do Sri Lanka',
    'LRD': 'Dólar Liberiano',
    'LSL': 'Loti do Lesoto',
    'LYD': 'Dinar Líbio',
    'MAD': 'Dirham Marroquino',
    'MDL': 'Leu Moldavo',
    'MGA': 'Ariary Malgaxe',
    'MKD': 'Denar Macedônio',
    'MMK': 'Kyat de Myanmar',
    'MNT': 'Tugrik Mongol',
    'MOP': 'Pataca de Macau',
    'MRU': 'Ouguiya Mauritana',
    'MUR': 'Rupia Mauriciana',
    'MVR': 'Rufiyaa das Maldivas',
    'MWK': 'Kwacha do Malawi',
    'MXN': 'Peso Mexicano',
    'MYR': 'Ringgit Malaio',
    'MZN': 'Metical Moçambicano',
    'NAD': 'Dólar Namibiano',
    'NGN': 'Naira Nigeriana',
    'NIO': 'Córdoba Nicaraguense',
    'NOK': 'Coroa Norueguesa',
    'NPR': 'Rupia Nepalesa',
    'NZD': 'Dólar Neozelandês',
    'OMR': 'Rial Omanense',
    'PAB': 'Balboa do Panamá',
    'PEN': 'Sol Peruano',
    'PGK': 'Kina de Papua-Nova Guiné',
    'PHP': 'Peso Filipino',
    'PKR': 'Rupia Paquistanesa',
    'PLN': 'Zloty Polonês',
    'PYG': 'Guarani Paraguaio',
    'QAR': 'Rial Catarense',
    'RON': 'Leu Romeno',
    'RSD': 'Dinar Sérvio',
    'RUB': 'Rublo Russo',
    'RWF': 'Franco Ruandês',
    'SAR': 'Rial Saudita',
    'SBD': 'Dólar das Ilhas Salomão',
    'SCR': 'Rupia de Seychelles',
    'SDG': 'Libra Sudanesa',
    'SEK': 'Coroa Sueca',
    'SGD': 'Dólar de Singapura',
    'SHP': 'Libra de Santa Helena',
    'SLE': 'Leone de Serra Leoa',
    'SLL': 'Leone de Serra Leoa',
    'SOS': 'Xelim Somali',
    'SRD': 'Dólar do Suriname',
    'STN': 'Dobra de São Tomé e Príncipe',
    'SYP': 'Libra Síria',
    'SZL': 'Lilangeni da Suazilândia',
    'THB': 'Baht Tailandês',
    'TJS': 'Somoni Tadjique',
    'TMT': 'Manat Turcomeno',
    'TND': 'Dinar Tunisiano',
    'TOP': 'Pa\'anga de Tonga',
    'TRY': 'Lira Turca',
    'TTD': 'Dólar de Trinidad e Tobago',
    'TVD': 'Dólar de Tuvalu',
    'TWD': 'Dólar de Taiwan',
    'TZS': 'Xelim Tanzaniano',
    'UAH': 'Hryvnia Ucraniana',
    'UGX': 'Xelim Ugandense',
    'USD': 'Dólar Americano',
    'UYU': 'Peso Uruguaio',
    'UZS': 'Som Uzbeque',
    'VES': 'Bolívar Venezuelano',
    'VND': 'Dong Vietnamita',
    'VUV': 'Vatu de Vanuatu',
    'WST': 'Tala Samoano',
    'XAF': 'Franco CFA Central',
    'XCD': 'Dólar do Caribe Oriental',
    'XDR': 'Direitos Especiais de Saque',
    'XOF': 'Franco CFA Ocidental',
    'XPF': 'Franco CFP',
    'YER': 'Rial Iemenita',
    'ZAR': 'Rand Sul-Africano',
    'ZMW': 'Kwacha Zambiano',
    'ZWL': 'Dólar do Zimbábue'
}

def obter_lista_moedas():
    """Obter todas as moedas disponíveis da API"""
    try:
        conversor = Conversor('USD')
        dados = conversor.obter_dados()
        
        if dados and 'conversion_rates' in dados:
            moedas_codigo = list(dados['conversion_rates'].keys())
            moedas_codigo.sort()
            
            # Criar lista de tuplas (codigo, nome)
            moedas_com_nomes = []
            for codigo in moedas_codigo:
                nome = NOMES_MOEDAS.get(codigo, codigo)
                moedas_com_nomes.append((codigo, nome))
            
            return moedas_com_nomes
        else:
            return []
    except Exception as e:
        print(f"Erro ao obter moedas: {e}")
        return []

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
            

    
@app.route('/', methods=['GET', 'POST'])
def home_page():
    # Obter lista de moedas disponíveis
    moedas = obter_lista_moedas()
    
    # Valores padrão
    moeda_base_selecionada = 'BRL'
    moeda_alvo_selecionada = 'USD'
    valor_digitado = None
    resultado = None
    taxa = None
    erro = None
    
    if request.method == 'POST':
        try:
            moeda_base_selecionada = request.form.get('moeda_base')
            moeda_alvo_selecionada = request.form.get('moeda_alvo')
            valor_digitado = float(request.form.get('valor'))
            
            # Realizar conversão
            conversor = Conversor(moeda_base_selecionada)
            taxa = conversor.obter_taxa(moeda_alvo_selecionada)
            
            if taxa:
                resultado = valor_digitado * taxa
            else:
                erro = "Não foi possível obter a taxa de conversão"
                
        except ValueError:
            erro = "Por favor, digite um valor válido"
        except Exception as e:
            erro = f"Erro na conversão: {str(e)}"
    
    return render_template('index.html', 
                         moedas=moedas,
                         moeda_base_selecionada=moeda_base_selecionada,
                         moeda_alvo_selecionada=moeda_alvo_selecionada,
                         valor_digitado=valor_digitado,
                         resultado=resultado,
                         taxa=taxa,                         erro=erro)

if __name__ == '__main__':
    app.run(debug=True)
