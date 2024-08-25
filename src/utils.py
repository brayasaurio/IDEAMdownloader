import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import warnings

warnings.filterwarnings("ignore")


def name_station(code):
    stations = pd.ExcelFile(r'IDEAM_Metadata\stations_catalog.xlsx')
    stations = stations.parse("catalog")
    name = stations[stations.Identificador == code].Ubicación.iloc[0]    
    return name

def variables_station(code):
    variable = pd.ExcelFile(r'IDEAM_Metadata\variables.xlsx')
    variable = variable.parse("Variables")
    name = name_station(code=code)
    variables = variable[variable.Ubicación == name]

    return list(variables["ID del conjunto de datos"])

def ideam_downloader(code,varible,waiting_time=60):

    edge_service  = Service(r'driver\msedgedriver.exe')
    options = webdriver.EdgeOptions()
    options.add_experimental_option("detach", True)

    browser = webdriver.Edge(service = edge_service, options=options)
    browser.maximize_window()
    browser.get("http://aquariuswebportal.ideam.gov.co")

    browser.implicitly_wait(waiting_time)

    browser.find_element(By.XPATH, '//nav/ul/li[4]/a/span').click()
    browser.find_element(By.XPATH, '//div[4]/div/div[2]/div[2]/div[2]/div/button').click()
    browser.find_element(By.XPATH, '//div[4]/div/div[2]/div[2]/div[2]/div/div/div[2]/input').send_keys(code)
    browser.find_element(By.XPATH, '//li[2]/a/span[2]').click()

    for _,i in enumerate(varible):
        try:
            browser.find_element(By.XPATH, '//div[4]/div/div[2]/div[2]/div[3]/div/button/div/div/div').click()
            browser.find_element(By.XPATH, '//div[4]/div/div[2]/div[2]/div[3]/div/div/div[2]/input').send_keys(i)
            browser.find_element(By.XPATH, '//div[4]/div/div[2]/div[2]/div[3]/div/div/div[3]/ul/li/a/span[2]').click()

            browser.find_element(By.XPATH, '//div[6]/ul/li[6]/a/span[2]').click()

            browser.find_element(By.XPATH, '//div/span/button/span').click()
            browser.find_element(By.XPATH, '//div[12]/div/button').click()
        except Exception as e:
            print(f"ha ocurrido un error de tipo {e}")
            browser.find_element(By.XPATH, '//div[4]/div/div[2]/div[2]/div[3]/div/button/div/div/div').click()

    return None