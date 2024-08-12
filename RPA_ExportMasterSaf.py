from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import date, timedelta

driver = webdriver.Chrome()
driver.get("https://p.dfe.mastersaf.com.br/mvc/login")
driver.maximize_window()

user = "samuel.pereira"
password = ""

def loginMasterSaf():
  try:
      user_field = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div[1]/input[1]"))
      )
      user_field.send_keys(user)

      password_field = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div[1]/input[2]"))
      )
      password_field.send_keys(password)

      confirm_button = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/form/div[1]/input[4]"))
      )
      confirm_button.click()

  except Exception as e:
      print(f"Ocorreu um erro: {e}")
  return print("login realizado com sucesso")


def exportXMLs():

  loginMasterSaf()
  
  try:
     today = date.today()

     i = 1
     while i <= 3:
      listagemNFe = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/ul/li[2]/a"))
        )
      listagemNFe.click()
      sleep(2)

      daysToRemove = timedelta(days=i)
      calculated_date = today - daysToRemove
      calculated_date = calculated_date.strftime("%d%m%Y")

      periodo_inicial = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div[32]/div[2]/div[2]/div[2]/input[3]")
      periodo_inicial.send_keys(Keys.CONTROL+"A")
      periodo_inicial.send_keys(Keys.BACKSPACE)
      for number in calculated_date:
          periodo_inicial.send_keys(number)

      Keys.TAB

      periodo_final = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div[32]/div[2]/div[2]/div[2]/input[4]")
      periodo_final.send_keys(Keys.CONTROL+"A")
      periodo_final.send_keys(Keys.BACKSPACE)
      for number in calculated_date:
          periodo_final.send_keys(number)
      
      search_button = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[32]/div[2]/div[2]/div[3]/div/input"))
      )
      search_button.click()
      sleep(2)

      ChangeTo200 = WebDriverWait(driver, 10).until(
         EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[32]/div[3]/div[9]/div[5]/div/table/tbody/tr/td[2]/table/tbody/tr/td[8]/select/option[5]"))
      )
      ChangeTo200.click()
      sleep(5)

      selectButton = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div[32]/div[3]/div[9]/div[3]/div[2]/div/table/thead/tr/th[12]/div/div/input")
      selectButton.click()
      sleep(2)

      DownloadButton = WebDriverWait(driver, 10).until(
         EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[32]/div[3]/div[1]/a[3]"))
      )
      DownloadButton.click()
      sleep(3)

      confirmDownload = driver.find_element(by=By.ID, value="downloadEmMassa")
      confirmDownload.click()

      sleep(7)

      i = i + 1
    

  except Exception as e:
     print(f"Ocorreu um erro: {e}")  


exportXMLs()





sleep(999999)
