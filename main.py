import pytz
from common.page import Rpa
from datetime import datetime
from config.settings import NOME_PLANILHA, CAMINHO_CREDENCIAL

rpa = Rpa(headless = True)

url = 'https://www.kabum.com.br/produto/576423/placa-de-video-rx-7800xt-gaming-16g-xfx-speedster-qick319-amd-radeon-16gb-ddr6-hdmi-3xdp-3-fan-rx-78tqickf9'

fuso_natal = pytz.timezone('America/Recife')
data_hora_atual = datetime.now(fuso_natal).strftime("%d/%m - %H:%M")
print(f'Inciando Verificador de Preços! Data/Hora atual da execução: {data_hora_atual}')

dfs = rpa.obter_planilhas()

worksheet_controle = rpa.obter_worksheet("Controle - Valor Atual")
worksheet_historico = rpa.obter_worksheet("Histórico de Preços")

if data_hora_atual not in dfs['Histórico de Preços'].columns:
    dfs['Histórico de Preços'][data_hora_atual] = None

for index, linha in dfs['Planilha de Controle'].iterrows():
    
    preco = rpa.raspar_valor(
        site =  linha['Site'].lower(), 
        url =   linha['URL']
    )

    dfs['Planilha de Controle'].at[index, 'Valor Atual'] = str(preco)
    dfs['Histórico de Preços'].at[index, data_hora_atual] = str(preco)

    print(f"{linha['Produto']} - R$ {preco}")

colunas_para_menor_maior_valor = dfs['Histórico de Preços'].columns[1:]
df_valores = dfs['Histórico de Preços'][colunas_para_menor_maior_valor].applymap(rpa.converter_valor_para_float)

dfs['Planilha de Controle']["Menor Valor Registrado"] = df_valores.min(axis=1)
dfs['Planilha de Controle']["Menor Valor Registrado"] = dfs['Planilha de Controle']["Menor Valor Registrado"].apply(rpa.converter_valor_para_real)

dfs['Planilha de Controle']["Maior Valor Registrado"] = df_valores.max(axis=1)
dfs['Planilha de Controle']["Maior Valor Registrado"] = dfs['Planilha de Controle']["Maior Valor Registrado"].apply(rpa.converter_valor_para_real)

rpa.atualizar_aba_com_dataframe(worksheet_controle, dfs['Planilha de Controle'])
rpa.atualizar_aba_com_dataframe(worksheet_historico, dfs['Histórico de Preços'])
