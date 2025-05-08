import pandas as pd
from common.page import Rpa
from datetime import datetime
from config.settings import NOME_PLANILHA, CAMINHO_CREDENCIAL


rpa = Rpa(headless = True)

url = 'https://www.kabum.com.br/produto/576423/placa-de-video-rx-7800xt-gaming-16g-xfx-speedster-qick319-amd-radeon-16gb-ddr6-hdmi-3xdp-3-fan-rx-78tqickf9'

data_hora_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")
print(f'Inciando Verificador de Preços! Data/Hora atual da execução: {data_hora_atual}')

print('Obtendo Planilha de Controle')
planilha_de_controle = rpa.obter_worksheet_dataframe(
    '1qbo5NnHHlcoRCCBg9w79FDq31YXO7_VDWG48y-ZoE6Y',
    'Controle - Valor Atual'
)

print('Obtendo planilha Histórico de Preços')
historico_de_precos = rpa.obter_worksheet_dataframe(
    '1qbo5NnHHlcoRCCBg9w79FDq31YXO7_VDWG48y-ZoE6Y',
    'Histórico de Preços'
)

aba_controle = rpa.obter_worksheet("Controle - Valor Atual")
aba_historico_de_precos = rpa.obter_worksheet("Histórico de Preços")

if data_hora_atual not in historico_de_precos.columns:
    historico_de_precos[data_hora_atual] = None

for index, linha in planilha_de_controle.iterrows():
    
    preco = rpa.raspar_valor(
        site =  linha['Site'].lower(), 
        url =   linha['URL']
    )

    planilha_de_controle.at[index, 'Valor Atual'] = preco
    historico_de_precos.at[index, data_hora_atual] = preco

    print(f"{linha['Produto']} - R$ {preco}")

rpa.atualizar_aba_com_dataframe(aba_controle, planilha_de_controle)
rpa.atualizar_aba_com_dataframe(aba_historico_de_precos, historico_de_precos)
