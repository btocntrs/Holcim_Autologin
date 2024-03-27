from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import pytesseract

from PIL import Image

# Inicializa el navegador Firefox con las opciones configuradas
driver = webdriver.Firefox()

driver.get("https://www.laseritsconline.com:47449/irj/portal/")

user_id_field = driver.find_element(By.ID, 'logonuidfield')
user_id_field.send_keys('4312283G')

def save_captcha():
    # Localiza el elemento HTML que contiene la imagen por su atributo src
    imagen_element = driver.find_element(By.CSS_SELECTOR, "img[src='/irj/servlet/prt/portal/prtroot/com.sap.portal.runtime.logon.ServletImageToken']")

    #Tomar un escreenshoot del elemento y nombrar el archivo como captcha
    imagen_element.screenshot("captcha.png")
    
def get_text_captcha(src):
    # Abre la imagen en la que deseas realizar OCR
    imagen = Image.open(src)

    # Realiza OCR en la imagen. Se asegura que todas las letras sean minúsculas y elimina los espacios.
    return pytesseract.image_to_string(imagen).lower().replace(" ", "")

def read_frames():
    # Encuentra todos los elementos <iframe> dentro del frame actual
    frames = driver.find_elements(By.TAG_NAME, "iframe")

    # Itera a través de los frames y obtén sus IDs
    for frame in frames:
        frame_id = frame.get_attribute("id")
        print(f"ID del frame: {frame_id}")

while True:
    save_captcha()
    
    texto_captcha = get_text_captcha("captcha.png")
    captcha_response_field = driver.find_element(By.NAME, "j_captcha_response")
    captcha_response_field.send_keys(texto_captcha)
    
    utilizar_token_btn = driver.find_element(By.ID, "btnSubmitUtilizarToken")
    utilizar_token_btn.click()    
    
    try:
        password_field = driver.find_element(By.ID, "logonpassfield")
        password_field.send_keys("GrupoIS2024.")

        token_field = driver.find_element(By.ID, "logontoken")
        token_field.send_keys("768881")

        access_btn = driver.find_element(By.NAME, "uidPasswordLogon")
        access_btn.click()
        break
    except NoSuchElementException:
        print("Intento erroneo de captcha.")


driver.switch_to.frame("ivuFrm_page0ivu3")

pedidos_btn = driver.find_element(By.LINK_TEXT, "Facturación Electrónica")
pedidos_btn.click() 