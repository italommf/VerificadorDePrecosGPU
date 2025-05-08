import gspread
import pandas as pd
from selenium.webdriver.common.by import By
from common.chromedriver import UndetectedChromeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import CAMINHO_CREDENCIAL

class Rpa(UndetectedChromeDriver):

    def raspar_valor(self, site, url):

        locator_valor_kabum_promo = (By.XPATH, '/html/body/div[1]/div/div[2]/main/article/section/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/h4')
        locator_valor_kabum_comum = (By.XPATH, '/html/body/div[1]/div/div[2]/main/article/section/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/h4')
       
        if site == 'kabum':

            self.driver.get(url)

            try:

                elemento = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator_valor_kabum_comum)
                ).text
            
            except TimeoutException:
            
                elemento = self.driver.find_element(*locator_valor_kabum_promo).text
                valor_formatado = 'Produto indisponível!'

            valor_formatado = float(elemento.replace('R$ ','').replace('.','').replace(',','.'))
            
            return valor_formatado
        
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
        intervalo = f"B1:{chr(65 + colunas)}{linhas}"  
        worksheet.batch_clear([intervalo])

        worksheet.update(worksheet_range_inicio, valores_sem_coluna_A)