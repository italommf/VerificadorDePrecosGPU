import gspread
import pandas as pd
from gspread.utils import rowcol_to_a1
from selenium.webdriver.common.by import By
from common.chromedriver import UndetectedChromeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import CellFormat, format_cell_range, NumberFormat
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.settings import CAMINHO_CREDENCIAL

class Rpa(UndetectedChromeDriver):

    def raspar_valor(self, site, url):

        locators = {
            'locator_valor_kabum_1': (By.XPATH, '/html/body/div[1]/div/div[2]/main/article/section/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/h4'),
            'locator_valor_kabum_2': (By.XPATH, '/html/body/div[1]/div/div[2]/main/article/section/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/h4'),
            'locator_valor_kabum_3': (By.XPATH, '/html/body/div[1]/div/div[2]/main/article/section/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[3]/div[1]/div/h4'),
            'locator_valor_kabum_4': (By.CSS_SELECTOR, '#blocoValores > div.sc-a24aba34-3.hSVqxN > div.sc-a24aba34-1.cpLDBn > div > h4'),
        }

        if site == 'kabum':

            self.driver.get(url)

            try:

                elemento = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(locators['locator_valor_kabum_1'])
                ).text
            
            except (TimeoutException, NoSuchElementException):
                
                for nome, locator in locators.items():

                    try:
                        elemento = self.driver.find_element(*locator).text
                        break
                    except (TimeoutException, NoSuchElementException):
                        continue 

            try:
                if elemento:
                    return elemento
            except:
                return 'Produto indisponível!'
  
    def conectar_google_sheets(self, nome_arquivo_credenciais, nome_planilha):
        
        escopo = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(nome_arquivo_credenciais, escopo)
        cliente = gspread.authorize(creds)

        return cliente.open(nome_planilha)
    
    def obter_worksheet_dataframe(self, workbook_key, worksheet_title, has_header = True, row_header = 0, list_formatter = False, credentials_path = CAMINHO_CREDENCIAL):

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        worksheet = client.open_by_key(workbook_key).worksheet(worksheet_title)
        raw_data = worksheet.get_all_values()

        if list_formatter:
            return raw_data

        header = raw_data.pop(row_header) if has_header else None
        return pd.DataFrame(raw_data, columns = header)
    
    def obter_worksheet(self, nome_aba):
        
        planilha = self.conectar_google_sheets(CAMINHO_CREDENCIAL, "Verificador de Preços - GPU")
        return planilha.worksheet(nome_aba)

    def atualizar_aba_com_dataframe(self, worksheet, dataframe):

        valores = [dataframe.columns.tolist()] + dataframe.values.tolist()

        valores_sem_coluna_A = [linha[1:] for linha in valores]

        worksheet_range_inicio = "B1"

        colunas = len(valores_sem_coluna_A[0])
        linhas = len(valores_sem_coluna_A)     
        ultima_celula = rowcol_to_a1(linhas, colunas + 1)  # +1 para começar de B
        intervalo = f"B1:{ultima_celula}"
        worksheet.batch_clear([intervalo])

        formato_moeda = CellFormat(
            numberFormat = NumberFormat(type='CURRENCY', pattern='R$ #,##0.00')
        )

        format_cell_range(worksheet, intervalo, formato_moeda)

        worksheet.update(worksheet_range_inicio, valores_sem_coluna_A)

    def converter_valor_para_float(self, valor):
        
        try:
            if not ',' in valor:
                return float(str(valor).replace("R$", "").replace(",", ".").strip())

            return float(str(valor).replace("R$ ", "").replace(".", "").replace(",", ".").strip())
        except:
            return None

    def converter_valor_para_real(self, valor):
        
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


    def obter_planilhas(self):

        print('Obtendo Planilha de Controle')
        planilha_de_controle = self.obter_worksheet_dataframe(
            '1qbo5NnHHlcoRCCBg9w79FDq31YXO7_VDWG48y-ZoE6Y',
            'Controle - Valor Atual'
        )

        print('Obtendo planilha Histórico de Preços')
        historico_de_precos = self.obter_worksheet_dataframe(
            '1qbo5NnHHlcoRCCBg9w79FDq31YXO7_VDWG48y-ZoE6Y',
            'Histórico de Preços'
        )

        dataframes = {
            'Planilha de Controle': planilha_de_controle,
            'Histórico de Preços': historico_de_precos
        }
        return dataframes