# citas v5.0.0

# credidentials

PLACE = 'R' ,# H for Haiti   , D for distio federal R for rio de janeiro and S for sao paulo 

randevou1 = {
    "email" : "monfleurijoue@gmail.com",
    "password" : "Cetoutejho@1",
    "type" : 'L' ,         # tip viza chwazi: "C" pou conn permiso, "S" pou sin, "L" pou legalizasyon
    "firstName" : "abcdfgfefg",
    "lastName" : "efffgghijkl",
    "paspo" : "XXXXXX" ,
    "NUT" : "XXX",
    "ID_NUMBER" : "1214438415",
    "day_to_choose" : "1",
    "day_to_choose_s" : "2"        # 0 to choose the first day or 2 for the third day
}




# credidentials
email1 = "monfleurijoue@gmail.com"
password1 = "Cetoutejho@1"
type1 = 'L'          # tip viza chwazi: "C" pou conn permiso, "S" pou sin, "L" pou legalizasyon
firstName1 = "abcdfgfefg"
lastName1 = "efffgghijkl"
paspo1 = "XXXXXX" 
NUT1 = "XXX"
ID_NUMBER1= "1214438415"
PLACE1 = 'R' # H for Haiti   , D for distio federal R for rio de janeiro and S for sao paulo 
day_to_choose1 = 1
day_to_choose_s1 = 2        # 0 to choose the first day or 2 for the third day



import threading
import smtplib
from flask import Flask, request
import threading
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import requests
import re
from selenium.webdriver.common.keys import Keys
import sys

import undetected_chromedriver as uc
from multiprocessing import Pool, current_process
import time
import os
import shutil
import tempfile
from selenium.common.exceptions import WebDriverException

driver = None
temp_dir_path = None


wait = WebDriverWait(driver, 60)

def download_and_patch_driver_once():
    """Download and patch chromedriver only once."""
    print("Downloading and patching chromedriver...")
    patcher = uc.Patcher()
    patcher.auto()
    print(f"Patched chromedriver: {patcher.executable_path}")
    return patcher.executable_path

def init_worker(patched_executable_path):
    """Initialize Chrome for each worker (visible in VNC)."""
    global driver, temp_dir_path
    process_name = current_process().name
    print(f"[{process_name}] Starting Chrome instance...")

    temp_dir_path = tempfile.mkdtemp()
    worker_driver_path = os.path.join(temp_dir_path, "chromedriver")

    try:
        shutil.copy(patched_executable_path, worker_driver_path)

        options = uc.ChromeOptions()
        # REMOVE headless mode
        # options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-driver-check")
        options.add_argument(f"--user-data-dir={os.path.join(temp_dir_path, 'profile')}")

        driver = uc.Chrome(
            options=options,
            driver_executable_path=worker_driver_path
        )

        print(f"[{process_name}] Chrome launched successfully.")

    except WebDriverException as e:
        print(f"[{process_name}] Failed to start driver: {e}")
        driver = None

def get_title_task(url):
    """Each worker gets page title."""
    global driver
    process_name = current_process().name
    if not driver:
        return f"[{process_name}] Driver not initialized."

    try:
        print(f"[{process_name}] Navigating to {url}")
        driver.get(url)
        time.sleep(3)
        title = driver.title
        print(f"[{process_name}] Page title: {title}")
        return f"Title from {url}: {title}"
    except Exception as e:
        return f"[{process_name}] Error: {e}"

def take_screenshot_task(url, filename):
    """Each worker takes a screenshot."""
    global driver
    process_name = current_process().name
    if not driver:
        return f"[{process_name}] Driver not initialized."

    try:
        print(f"[{process_name}] Taking screenshot of {url}")
        driver.get(url)
        time.sleep(5)
        driver.save_screenshot(filename)
        print(f"[{process_name}] Screenshot saved: {filename}")
        return f"Screenshot of {url} saved to {filename}"
    except Exception as e:
        return f"[{process_name}] Error: {e}"

def cleanup_worker(_):
    """Close Chrome and clean temp files."""
    global driver, temp_dir_path
    process_name = current_process().name
    if driver:
        driver.quit()
        print(f"[{process_name}] driver closed.")
        driver = None
    if temp_dir_path and os.path.exists(temp_dir_path):
        shutil.rmtree(temp_dir_path, ignore_errors=True)
        print(f"[{process_name}] Temp folder deleted.")
        temp_dir_path = None






def clean_text(text):
    # Remove all spaces
    text_no_spaces = re.sub(r"\s+", "", text)

    # Process each character
    cleaned_chars = []
    for char in text_no_spaces:
        if char == 'P':
            cleaned_chars.append('P')  # Keep P uppercase
        elif char.lower() == 'o':
            cleaned_chars.append('0')  # Convert o/O to 0
        else:
            cleaned_chars.append(char.lower())  # Everything else to lowercase

    # Join characters back into a string
    cleaned_text = ''.join(cleaned_chars)
    return cleaned_text


def solve(f):
	with open(f, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read()).decode('ascii')
		url = 'https://api.apitruecaptcha.org/one/gettext'

		data = { 
			'userid':'LILMAX', 
			'apikey':'8PAcj0csaLnf3djh6MFr',  
			'data':encoded_string
		}
		response = requests.post(url = url, json = data)
		data = response.json()
		return data
        

def final_captcha():
        wait = WebDriverWait(driver, 30)
        img0 = 'center > img'
        img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, img0)))

        time.sleep(1)
        img.screenshot('captcha.png')
        print("✅ Screenshot taken")
        result = solve('captcha.png')

        # If result is a dictionary with a 'result' key
        if isinstance(result, dict) and 'result' in result:
            print(result['result'])
        else:
            print(result)
        text4 = (result['result'])

        cleanText = clean_text(text4)
        print('clean text', cleanText)

        wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(cleanText)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[normalize-space()='Aceptar']" ).click()


def image_changed():
        try:
            # Wait for the captcha image to be present (up to 30 seconds)
            captcha2 = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#up > div:nth-child(1) > div > div > div > div > div > center > img'))
            )
            print('image selector present')

            # Store the initial src
            initial_src = captcha2.get_attribute("src")

            try:
                # Wait max 3 seconds for the src to change
                WebDriverWait(driver, 2).until(
                    lambda d: captcha2.get_attribute("src") != initial_src
                )
                print("Captcha updated — proceeding")
            except Exception:
                print("Captcha did not change in 3 seconds — skipping")

        except Exception:
            print("Captcha image not found — skipping")






def err1():
    # retry loop for captcha errors
    at = 0
    atm = 30
    err_selector = 'div[role="alert"].el-notification.right'

    while at < atm:
        try:
            # check if error popup appears
            wait2 = WebDriverWait(driver, 1)
            wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, err_selector)))
            print('❌ Error detected on captcha')

            print(f'🔄 Retry #{at + 1}')
           

            try:
                print('proccessing image changed')
                # Wait for the captcha image to be present (up to 30 seconds)
                captcha2 = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#up > div:nth-child(1) > div > div > div > div > div > center > img'))
                )
                print('image selector present')

                # Store the initial src
                initial_src = captcha2.get_attribute("src")

                try:
                    # Wait max 3 seconds for the src to change
                    WebDriverWait(driver, 1).until(
                        lambda d: captcha2.get_attribute("src") != initial_src
                    )
                    print("Captcha updated — proceeding")
                except Exception:
                    print("Captcha did not change in 3 seconds — skipping")

            except Exception:
                    print("Captcha image not found — skipping")

            # wait until error disappears before retrying
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, err_selector))
            )
            print('✅ Error popup disappeared')

            # final check for captcha success
            final_captcha()

            at += 1  # increment retry counter
            print('✔️ Captcha attempt passed')




        except Exception as e:
                print("➡️ No error popup, captcha probably passed.")
                break  # exit if no error found

        ("🏁 Retry loop finished")

        





def err():
    # retry loop for captcha errors
    at = 0
    atm = 30
    err_selector = 'div[role="alert"].el-notification.right'

    while at < atm:
        try:
            # check if error popup appears
            wait2 = WebDriverWait(driver, 2)
            wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, err_selector)))
            print('❌ Error detected on captcha')

            print(f'🔄 Retry #{at + 1}')
            time.sleep(0.5)

            # only re-solve captcha
            image_changed()

            # wait until error disappears before retrying
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, err_selector))
            )
            print('✅ Error popup disappeared')

            # final check for captcha success
            final_captcha()

            at += 1  # increment retry counter
            print('✔️ Captcha attempt passed')

        except Exception as e:
            print(f"➡️ No error popup, captcha probably passed. Msg: {e}")
            break  # exit if no error found

    print("🏁 Retry loop finished")

        

def choose_date(day_to_choose,day_to_choose_s):
    i = 0
    im = 5

    while i < im:
        try:
            time.sleep(1)
            elements = driver.find_elements(By.CSS_SELECTOR, 
                ".fc-day-grid-event.fc-h-event.fc-event.fc-start.fc-end.classPointer"
            )

            if len(elements) < 2:
                print("Element not present, skipping...")

                # Aceptar
                try:
                    acc = "//button[normalize-space()='Aceptar']"
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, acc)))
                    driver.find_element(By.XPATH, acc).click()
                    print("Clicked 'Aceptar'")
                except:
                    print("Aceptar not found")

                # Click next months
                next_button_selector = ".fc-next-button"
                for a in range(5):
                    try:
                        WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector))
                        )
                        driver.find_element(By.CSS_SELECTOR, next_button_selector).click()
                        print(f"Month click #{a+1}")
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"Error clicking next month: {e}")
                        break

                # Final captcha once per loop
                final_captcha()

                # Only start thread once
                err1()
                # Try clicking a date again after captcha
                elements = driver.find_elements(By.CSS_SELECTOR, 
                    ".fc-day-grid-event.fc-h-event.fc-event.fc-start.fc-end.classPointer"
                )
                try:
                    time.sleep(1)
                    elements[day_to_choose_s].click()
                    print("✅ Clicked the target element successfully")
                    final_captcha()
                    err1()
                    choose_time()
                    break
                except Exception as s:
                    print(f"Error selecting date: {s}")
                    i += 1

            else:
                # Click directly
                try:
                    elements[day_to_choose].click()
                    print("✅ Clicked the target element successfully")
                    break
                except Exception as s:
                    print(f"Error selecting date: {s}")
                    i += 1

        except Exception as e:
            print(f"No date found, error: {e}")
            break


                 


def choose_time():
        # element11a
        element11a = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.el-col.el-col-24 .el-button.schedule-date-cmp'))
        )
        element11a.click()
        print('Element clicked!')

        # element12a
        element12a = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.el-col.el-col-24 .el-button.schedule-date-cmp'))
        )
        element12a.click()
        print('Element clicked!')

        # Wait for the primary button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.el-button.el-button--primary'))
        )

        # Click the primary button
        button2 = driver.find_element(By.CSS_SELECTOR, '.el-button.el-button--primary')
        button2.click()
        print('last Button clicked!')

        # Wait for success element
        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#up > div:nth-child(1) > div > div > div > div > div > div.container-fluid.h-100 > div > div > div > button'))
        )
        print('radevou pran ak sikse')

        # Take a screenshot
        driver.save_screenshot('screenshot2.png')
        print('📸 Screenshot saved!')


# sin permiso

def sin_permiso():

    # second step
    a7= "//label[contains(., 'Visas')]"
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, a7) ))
    driver.find_element(By.XPATH, a7).click()
    print('visas clicked')

    a8 = "//button[contains(text(), 'Agregar')]"
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, a8)))
    time.sleep(1)
    driver.find_element(By.XPATH,a8).click()
    wait.until(EC.presence_of_element_located((By.NAME, 'name')))
    driver.find_element(By.NAME, 'name').click()

    time.sleep(1)
    a9 = '[role="option"], .vs__dropdown-option, .vs__dropdown-menu div'
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, a9)))
    a9a = driver.find_elements(By.CSS_SELECTOR,a9)
    
    for option9 in a9a:
         text = option9.text
         if text.strip() == 'Sin permiso del INM':
              option9.click()
              print('sin permiso clicked')
              break
         
    time.sleep(2)

    a10 = 'formalitites_subtype_id'
    wait.until(EC.presence_of_element_located((By.NAME, 'formalitites_subtype_id')))
    a10a = driver.find_element(By.NAME, 'formalitites_subtype_id')
    a10a.click()

    time.sleep(2)
    # Find and click the dropdown toggle

    # Wait for options to appear
    options_locator = (By.CSS_SELECTOR, '[role="option"], .vs__dropdown-option, .vs__dropdown-menu div')
    wait.until(EC.presence_of_all_elements_located(options_locator))

    time.sleep(1)  # wait a bit to ensure options fully load

    # Get all options
    options = driver.find_elements(*options_locator)

    # Loop through and click the matching text
    for option in options:
        text = option.text.strip()
        if text == 'Visitante sin permiso para realizar actividades remuneradas':
            option.click()
            break
            
    time.sleep(1)    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continuar')]").click()
    print('second step passed')
    type



# conn permiso
def conn_permiso(paspo,NUT):

    # second step
    a7= "//label[contains(., 'Visas')]"
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, a7) ))
    driver.find_element(By.XPATH, a7).click()
    print('visas clicked')

    a8 = "//button[contains(text(), 'Agregar')]"
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, a8)))
    time.sleep(1)
    driver.find_element(By.XPATH,a8).click()


    wait.until(EC.presence_of_element_located((By.NAME, 'name')))
    driver.find_element(By.NAME, 'name').click()

    # Sleep for 1 second
    time.sleep(1)

    # Wait for options to appear
    options_locator = (By.CSS_SELECTOR, '[role="option"], .vs__dropdown-option, .vs__dropdown-menu div')
    WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located(options_locator))

    # Get all options
    options6 = driver.find_elements(*options_locator)

    # Loop through and click the matching text
    for option6 in options6:
        text = option6.text
        if text.strip() == 'Con permiso del INM (Validación vía servicio web con el INM)':
            option6.click()
            break

    print('con permiso clicked')
    

    ################################################################################################
    # Wait for passportNumber inputs
    passportnumber = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.NAME, 'passportNumber'))
    )

    # Choose the first one (index 0)
    targetpassport = passportnumber[0]
    print('found')
    targetpassport.send_keys(paspo)

    # Wait again for passportNumber inputs
    nut = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.NAME, 'passportNumber'))
    )

    # Choose the second one (index 1)
    targetnut = nut[1]
    targetnut.send_keys(NUT)
                
    time.sleep(1)    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continuar')]").click()
    print('second step passed')
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Continuar')]").click()




def legalisation():
        

        # second step
        a7= "//label[contains(., 'Certificados, Legalizaciones y Visados')]"
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, a7) ))
        driver.find_element(By.XPATH, a7).click()
        print('legalization clicked')

        a8 = "//button[contains(text(), 'Agregar')]"
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, a8)))
        time.sleep(1)
        driver.find_element(By.XPATH,a8).click()
        
        wait.until(EC.presence_of_element_located((By.NAME, 'name')))
        driver.find_element(By.NAME, 'name').click()

        time.sleep(1)
        a9 = '[role="option"], .vs__dropdown-option, .vs__dropdown-menu div'
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, a9)))
        a9a = driver.find_elements(By.CSS_SELECTOR,a9)
        
        for option9 in a9a:
            text = option9.text
            if text.strip() == 'Certificados':
                option9.click()
                print('Certificados clicked')
                break
            
        time.sleep(2)

        a10 = 'formalitites_subtype_id'
        wait.until(EC.presence_of_element_located((By.NAME, 'formalitites_subtype_id')))
        a10a = driver.find_element(By.NAME, 'formalitites_subtype_id')
        a10a.click()

        time.sleep(2)
        # Find and click the dropdown toggle

        # Wait for options to appear
        options_locator = (By.CSS_SELECTOR, '[role="option"], .vs__dropdown-option, .vs__dropdown-menu div')
        wait.until(EC.presence_of_all_elements_located(options_locator))

        time.sleep(1)  # wait a bit to ensure options fully load

        # Get all options
        options = driver.find_elements(*options_locator)

        # Loop through and click the matching text
        options[0].click()
                
        time.sleep(1)    
        driver.find_element(By.XPATH, "//button[contains(text(), 'Continuar')]").click()
        print('second step passed')




def identidad(ID_NUMBER):
    # identidad
    time.sleep(3)
    print('waited')
    a11 = '.v-select[name="doc_probatorio_id"] .vs__dropdown-toggle'
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, a11)))
    driver.find_element(By.CSS_SELECTOR,a11).click()
    time.sleep(1)


    # choose
    a12 = '.vs__dropdown-option'
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, a12) ))
    time.sleep(1)
    a12a = driver.find_elements(By.CSS_SELECTOR, a12)
    a12a[0].click()

    # ID number
    a13 = 'value_1'
    wait.until(EC.presence_of_element_located((By.NAME, a13)))
    driver.find_element(By.NAME, a13).send_keys(ID_NUMBER)

    # --- First date ---
    a14 = 'value_2'
    wait.until(EC.presence_of_element_located((By.NAME, a14)))
    driver.find_element(By.NAME,a14).click()

    
    # Year
    year_dropdown1 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-datepicker-year'))
    )
    time.sleep(0.5)  # small pause

    options2 = year_dropdown1.find_elements(By.CSS_SELECTOR, 'option')
    for option in options2:
        if option.text.strip() == '1987':
            option.click()
            break

    # Month
    month_dropdown1 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-datepicker-month'))
    )
    time.sleep(0.5)

    options2a = month_dropdown1.find_elements(By.CSS_SELECTOR, 'option')
    for option in options2a:
        if option.text.strip() == 'Feb':
            option.click()
            break

    # Day
    days2a = driver.find_elements(By.CSS_SELECTOR, '.ui-datepicker-calendar a')
    for day in days2a:
        if day.text.strip() == '16':
            day.click()
            break

    time.sleep(1)

    # --- Second date ---
    date1b = driver.find_element(By.NAME, 'value_3')
    date1b.click()

    # Year
    year_dropdown1b = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-datepicker-year'))
    )
    time.sleep(0.5)

    options2b = year_dropdown1b.find_elements(By.CSS_SELECTOR, 'option')
    for option in options2b:
        if option.text.strip() == '1987':
            option.click()
            break

    # Month
    month_dropdown1b = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-datepicker-month'))
    )
    time.sleep(0.5)

    options2ab = month_dropdown1b.find_elements(By.CSS_SELECTOR, 'option')
    for option in options2ab:
        if option.text.strip() == 'Feb':
            option.click()
            break

    # Day
    days2ab = driver.find_elements(By.CSS_SELECTOR, '.ui-datepicker-calendar a')
    for day in days2ab:
        if day.text.strip() == '16':
            day.click()
            break

    time.sleep(1)

    # --- Fill other fields ---
    pay = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, 'value_4'))
    )
    pay.send_keys('HAITI')

    submit_btn = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Continuar')]"))
    )
    submit_btn.click()
    
    print('third step passed succecfully')



def submit_third_step():
    time.sleep(3)
    submit_btn = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Continuar')]"))
    )
    submit_btn.click()
    





def log(email,password):
    try:
       
        # Zoom the page to 75%
        driver.execute_script("document.body.style.zoom='75%'")

        # Click login label
        label = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(), 'Correo electrónico y contraseña')]")
        ))
        print("✅ Label found:", label.text)
        label.click()

        # Email input
        email_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[name="email"]')
        ))
        email_input.send_keys(email)

        # Password input
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys(password)

        # Checkbox click
        driver.find_element(By.XPATH, "//p[contains(text(), 'He leido y acepto los')]").click()

        # Click icon and Ingresar button
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(3) > div > main > div > div > div > div > div.background > div:nth-child(2) > div:nth-child(2) > div > div > div > div > div > div > div > a > span > svg").click()
        driver.find_element(By.XPATH, "//button[contains(@class, 'btn') and contains(@class, 'primary') and .//font[text()='Ingresar']]").click()

        # captcha
        final_captcha()
       
        # look for error
        at = 0
        atm = 30
        while at < atm:
        
            try:
                err = '.alert.alert-danger.alert-dismissible'
                wait2 = WebDriverWait(driver, 4)
                err_msg = wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, err)))
                print('⚠️ err detected')

                msg = err_msg.text
                message = msg.strip()

                print(f"⚠️ Error message: {message}")

                if "Usuario y/o contraseña no válidos." in message:
                    print("❌ Itilizatè inkorèk")
                    driver.quit()
                elif  "¡Atención! El Captcha no es correcto" in message:
                  time.sleep(1)
                  driver.find_element(By.CSS_SELECTOR, 'button.close').click()
                  driver.find_element(By.XPATH, "//button[contains(@class, 'btn') and contains(@class, 'primary') and .//font[text()='Ingresar']]").click()
                  print('reyese #', at+1)
                  time.sleep(1)
                   # robot
                  final_captcha()
                elif "¡Atención! Se identifico un comportamiento sospechoso por lo que no podrás acceder al sistema durante 24 horas, de insistir es posible que la cuenta se bloquee, Quedan 24 horas de espera para poder acceder" in message:
                  print('❌kont bloke!!!')
                  driver.quit()
                 
            except Exception as e:
             print("captcha passed:")
             break
            

    except Exception as e:
                print("❌ Exception during login:") 


    






def firs_click_with_brazil ():
    try:

        # Click the dropdown toggle to open the options
        selector5a = (By.CSS_SELECTOR, '.v-select[name="country_id"] .vs__dropdown-toggle')
        wait.until(EC.presence_of_element_located(selector5a)).click()

        time.sleep(1)  # wait a bit to ensure options fully load

        # Wait for dropdown options to be present
        selector5b = (By.CSS_SELECTOR, '.vs__dropdown-option')
        wait.until(EC.presence_of_all_elements_located(selector5b))

        time.sleep(1)  # wait a bit to ensure options fully load

        # Find all dropdown options
        option2 = driver.find_elements(*selector5b)

        # Click the 84th option (index 83)
        option2[29].click()
        print('brazil clicked')




        # now click on the city

        print('clicking on the city')

        if PLACE == 'D':
            
            # Click the dropdown toggle to open the options
            selector5a = (By.CSS_SELECTOR, '.v-select[name="state_id"] .vs__dropdown-toggle')
            wait.until(EC.presence_of_element_located(selector5a)).click()

            time.sleep(1)  # wait a bit to ensure options fully load

            # Wait for dropdown options to be present
            selector5b = (By.CSS_SELECTOR, '.vs__dropdown-option')
            wait.until(EC.presence_of_all_elements_located(selector5b))

            time.sleep(1)  # wait a bit to ensure options fully load

            # Find all dropdown options
            option2 = driver.find_elements(*selector5b)

            # Click the 84th option (index 83)
            option2[0].click()
            print('distrio choosed✅')

        elif PLACE == 'R' :
              # Click the dropdown toggle to open the options
            selector5a = (By.CSS_SELECTOR, '.v-select[name="state_id"] .vs__dropdown-toggle')
            wait.until(EC.presence_of_element_located(selector5a)).click()

            time.sleep(1)  # wait a bit to ensure options fully load

            # Wait for dropdown options to be present
            selector5b = (By.CSS_SELECTOR, '.vs__dropdown-option')
            wait.until(EC.presence_of_all_elements_located(selector5b))

            time.sleep(1)  # wait a bit to ensure options fully load

            # Find all dropdown options
            option2 = driver.find_elements(*selector5b)

            # Click the 84th option (index 83)
            option2[1].click()
            print('rio de janeiro choosed✅')

        elif PLACE == "S":
              # Click the dropdown toggle to open the options
            selector5a = (By.CSS_SELECTOR, '.v-select[name="state_id"] .vs__dropdown-toggle')
            wait.until(EC.presence_of_element_located(selector5a)).click()

            time.sleep(1)  # wait a bit to ensure options fully load

            # Wait for dropdown options to be present
            selector5b = (By.CSS_SELECTOR, '.vs__dropdown-option')
            wait.until(EC.presence_of_all_elements_located(selector5b))

            time.sleep(1)  # wait a bit to ensure options fully load

            # Find all dropdown options
            option2 = driver.find_elements(*selector5b)

            # Click the 84th option (index 83)
            option2[2].click()
            print('sao paulo choosed✅')

        else:
             print('code peyi inkorek')
            



    except Exception as e:
        print("❌ Exception during first country selection:", e)















def randevou(url,email,password,firstName,lastName,paspo,NUT,ID_NUMBER,PLACE,day_to_choose,day_to_choose_s):
    driver.get(url)
    wait = WebDriverWait(driver, 60)

    log(email,password)
    print('login finished succesfully')
    
    
    print('procceding croix')
    def croix():
        at = 0
        atm = 3
        while at < atm:

            try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(3) > div.container > div:nth-child(1) > div > div > div > div > div > div > div > div > div > div > span > a')))
                    
                    locator = (By.CSS_SELECTOR, "body > div:nth-child(3) > div.container > div:nth-child(1) > div > div > div > div > div > div > div > div > div > a > span > svg")

                
                    print('konekte')

                    # Click the SVG
                    driver.find_element(*locator).click()
            except Exception as t:
                    at += 1
                    
                    

    
    monitor_thread0 = threading.Thread(target=croix, daemon=True)
    monitor_thread0.start()
            

          
            


    # Example Selenium-like logic
    print("⏸ Waiting for trigger...")
    input('klike sou enter pou kontinye')  # <-- script pauses here until /trigger is hit
    print("▶ Continuing execution after trigger")

    # secong step
    driver.execute_script("document.body.style.zoom='100%'")


    
    # planifier
    B = driver.find_element(By.XPATH, "//a[contains(@class, 'btn') and contains(@class, 'btn-primary') and normalize-space(text())='Iniciar Trámite']")                   
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(B))        
    B.click()
    start = time.time()   # get start timestamp

    if PLACE == 'H':
        print('proccessing with haiti')

    else:
         firs_click_with_brazil()
        
        

    a0 = (By.CSS_SELECTOR,'.card')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located(a0))
    print('card loaded') 

    time.sleep(0.2)
    a1 = "//a[contains(text(), 'Seleccionar')]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, a1))   )     
    a1 = driver.find_element(By.XPATH, a1)                   
    a1.click()

    time.sleep(0.2)
    a2 = "//button[contains(text(), 'Aceptar')]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,a2))  )      
    a2 = driver.find_element(By.XPATH, a2 )                   
    a2.click()

    driver.execute_script("window.scrollTo(0, 346.53125);")
    a3 = "//a[contains(text(), 'Agregar Manualmente')]"
    time.sleep(0.2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,a3)))
    a3 = driver.find_element(By.XPATH, a3)                     
    a3.click()

    
    # information
    wait.until(EC.presence_of_element_located((By.NAME, 'name')))
    time.sleep(0.2)
    driver.find_element(By.NAME, 'name').send_keys(firstName)

    driver.find_element(By.NAME, 'firstName').send_keys(lastName)

    # birthdate
    # Click the birthdate input to open the calendar
    birthdate_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "birthdate"))
    )
    birthdate_input.click()

    # Wait for the year dropdown to be visible
    year_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-datepicker-year"))
    )

    time.sleep(0.2)  # small pause to allow options to load

    # Find the year option '1986'
    year_options = year_dropdown.find_elements(By.CSS_SELECTOR, "option")
    for option in year_options:
        if option.text.strip() == "1986":
            option.click()
            break

    # Select the day '16'
    days = driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-calendar a")
    for day in days:
        if day.text.strip() == "16":
            day.click()
            break


    # Select gender
    selector4a = (By.CSS_SELECTOR, '.v-select[name="cat_gender_id"] .vs__dropdown-toggle')
    wait.until(EC.presence_of_element_located(selector4a)).click()

    selector4b = (By.CSS_SELECTOR, '.vs__dropdown-option')
    wait.until(EC.presence_of_all_elements_located(selector4b))
    time.sleep(0.3)
    option = driver.find_elements(*selector4b)
    option[1].click()

    # Nationality
    selector5a = (By.CSS_SELECTOR, '.v-select[name="cat_nationality_id"] .vs__dropdown-toggle')
    wait.until(EC.presence_of_element_located(selector5a)).click()

    time.sleep(0.3)
    selector5b = (By.CSS_SELECTOR, '.vs__dropdown-option')
    wait.until(EC.presence_of_all_elements_located(selector5b))
    option2 = driver.find_elements(*selector5b)
    option2[82].click()

    # Civil state
    selector6a = (By.CSS_SELECTOR, '.v-select[name="civilState"] .vs__dropdown-toggle')
    wait.until(EC.presence_of_element_located(selector6a)).click()

    selector6b = (By.CSS_SELECTOR, '.vs__dropdown-option')
    wait.until(EC.presence_of_all_elements_located(selector6b))
    time.sleep(0.3)
    option3 = driver.find_elements(*selector6b)
    option3[0].click()

    # Another country
    dropdowns = wait.until(EC.presence_of_all_elements_located((By.NAME, 'country_id')))
    target_dropdown = dropdowns[1]
    target_dropdown.click()

    selector7b = (By.CSS_SELECTOR, '.vs__dropdown-option')
    time.sleep(0.3)
    wait.until(EC.presence_of_all_elements_located(selector7b))
    option4 = driver.find_elements(*selector7b)
    option4[89].click()

    # Wait for department label
    department_label = (
        By.CSS_SELECTOR,
        'body > div:nth-child(3) > div.container > div:nth-child(3) > div > div > div > div:nth-child(2) > div:nth-child(1) > form > div:nth-child(6) > div > div > div > div:nth-child(3) > form > div:nth-child(5) > div:nth-child(2) > div > div > label'
    )
    WebDriverWait(driver, 40).until(EC.presence_of_element_located(department_label))
    print("waited")    



    time.sleep(0.3)

    # Execute the JavaScript for finding the input via XPath and interacting with it
    script = """
    var element = document.evaluate(
        '/html/body/div[2]/div[3]/div[3]/div/div/div/div[2]/div[1]/form/div[3]/div/div/div/div[3]/form/div[5]/div[2]/div/div/div/div/div[1]/input',
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;

    if (element) {
        var blocker = document.querySelector('#navbarMainCollapse');
        if (blocker) blocker.style.pointerEvents = 'none';

        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(function() {
            try {
                element.click();
                element.focus();
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                console.log('Value set!');
            } catch (e) {
                console.error('Error:', e);
            }
        }, 500);
    } else {
        console.log('Element not found');
    }
    """

    driver.execute_script(script)

    a6 = (By.CSS_SELECTOR, '.vs__dropdown-option')
    time.sleep(0.3)
    wait.until(EC.presence_of_all_elements_located(a6))
    a6a = driver.find_elements(*a6)
    a6a[21].click()

    #ville
    ville_element = driver.find_element(By.CSS_SELECTOR, ".form-group > .form-group > .form-group > .form-control")
    ville_element.send_keys('petion ville', Keys.ENTER)


    element_to_wait = 'body > div:nth-child(3) > div.container > div:nth-child(3) > div > div > div > div:nth-child(2) > div:nth-child(1) > form > div:nth-child(6) > div > div > div > div:nth-child(3) > form > div:nth-child(7) > div > span'
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_to_wait)))

    finish = '.btn:nth-child(2)'
    driver.find_element(By.CSS_SELECTOR, finish).click()
    print('first step passed')
    end = time.time()     # get end timestamp
    elapsed = end - start

    print(f"⏱ Script took {elapsed:.2f} seconds")

    
    
    # type of viza
    # Call function based on type
    if type == "C":
        conn_permiso(firstName,lastName,paspo,NUT)
        identidad()

    elif type == "S":
        sin_permiso(firstName,lastName)
        identidad(ID_NUMBER)

    elif type == "L":
        print('proccessing with legalization')
        legalisation(firstName,lastName)
        submit_third_step()

    else:
        print('type pa rekoni')





    # last step
    wait.until(EC.presence_of_element_located((By.NAME, 'country_id')))
    driver.find_element(By.NAME, 'country_id').click()

    pays = '.vs__dropdown-option'
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, pays)))
    time.sleep(0.5)
    paysa = driver.find_elements(By.CSS_SELECTOR, pays)
    paysa[89].click()

    
    # Wait for label element to be present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#up > form > div:nth-child(3) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > div > label')))
    time.sleep(0.5)

    # Execute JS to interact with element located by XPath, scroll, click, focus, dispatch input/change events
    js_script = """
    const element1 = document.evaluate(
        '/html/body/div[2]/div[3]/div[3]/div/div/div/div[2]/div[1]/form/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div[1]/input',
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;

    if (element1) {
        const blocker = document.querySelector('#navbarMainCollapse');
        if (blocker) blocker.style.pointerEvents = 'none';

        element1.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(() => {
            try {
                element1.click();
                element1.focus();

                element1.dispatchEvent(new Event('input', { bubbles: true }));
                element1.dispatchEvent(new Event('change', { bubbles: true }));
                console.log('Value set!');
            } catch (e) {
                console.error('Error:', e);
            }
        }, 500);
    } else {
        console.log('Element not found');
    }
    """
    driver.execute_script(js_script)

    # Wait and click the 26th option in dropdown (index 25)
    selectors = (By.CSS_SELECTOR, '.vs__dropdown-option')
    wait.until(EC.presence_of_element_located(selectors))
    options = driver.find_elements(*selectors)
    if len(options) > 25:
        options[25].click()

    # Fill inputs by name
    direction = wait.until(EC.presence_of_element_located((By.NAME, 'direction')))
    direction.send_keys('petion ville')

    name = wait.until(EC.presence_of_element_located((By.NAME, 'name')))
    name.send_keys('job')

    firstName = wait.until(EC.presence_of_element_located((By.NAME, 'firstName')))
    firstName.send_keys('atilus')

    # Wait for phone input and set value via JS to trigger events properly
    wait.until(EC.presence_of_element_located((By.NAME, 'phone')))
    js_set_phone = """
    const input = document.querySelector('input[name="phone"]');
    if (input) {
        input.scrollIntoView({ behavior: 'smooth', block: 'center' });

        const event = new MouseEvent('mousedown', { bubbles: true });
        input.dispatchEvent(event);

        input.click();
        input.focus();
        input.value = "5551234567";

        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));

        console.log("✅ Phone value set!");
    } else {
        console.log("❌ Phone input not found");
    }
    """
    driver.execute_script(js_set_phone)

    # Function to get timer value from page
    
    def get_timer_value(driver):
        """Returns the timer text from the page."""
        return driver.execute_script("""
            const timer = document.querySelector('#up > form > h4 > p'); 
            return timer ? timer.textContent.trim() : null;
        """)

    # Monitor the timer and wait for specific value
    while True:
        timer_value = get_timer_value(driver)

        if timer_value == "00:58:59":
            print("🎯 Target time reached — clicking button...")
            
            btn_selector = (By.CSS_SELECTOR, 
                "body > div:nth-child(3) > div.container > div:nth-child(3) > div > "
                "div > div > div:nth-child(2) > div:nth-child(2) > div > button.btn.btn-primary"
            )
            
            for i in range(5):  # Try up to 5 times
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(btn_selector))
                    driver.find_element(*btn_selector).click()
                    print(f"✅ Button clicked (Attempt #{i+1})")
                except Exception:
                    print(f"❌ Button not found on attempt #{i+1}")
                    break
            break  # Stop after clicking
        
        time.sleep(0.5)  # Check every 1/2 second

        

   # first robot
    image_changed()
    final_captcha()
    # staring for error
    monitor_thread0 = threading.Thread(target=err1,  daemon=True)
    monitor_thread0.start()

    # wait until the month appear
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#up > div > div.info_colors.el-row.is-justify-center.el-row--flex > div:nth-child(1) > span')))
    choose_date(day_to_choose,day_to_choose_s)
    final_captcha()
    err1()
    choose_time()


    # staring for error
    monitor_thread0 = threading.Thread(target=err, daemon=True)
    monitor_thread0.start()
    
    

 
    input('klike sou enter pou komanse siveye...')

       
    


       
    input("✅ driver open. Press Enter to close...")
    driver.quit()












if __name__ == "__main__":
    patched_executable_path = download_and_patch_driver_once()
    if not patched_executable_path:
        exit(1)

    os.makedirs("screenshots", exist_ok=True)

    urls = {
        "title": "https://www.wikipedia.org",
        "screenshot": "https://www.google.com",
        "randevou1": "https://citas.sre.gob.mx/"
    }

    print("Starting 2 parallel visible Chrome windows...")
    with Pool(processes=2, initializer=init_worker, initargs=(patched_executable_path,)) as pool:
        title_task = pool.apply_async(get_title_task, (urls["title"],))
        screenshot_task = pool.apply_async(take_screenshot_task, (urls["screenshot"], "screenshots/google.png"))
        citas1 = pool.apply_async(randevou, (urls["randevou1"], email1, password1, firstName1, lastName1, paspo1, NUT1, ID_NUMBER1, PLACE1, day_to_choose1, day_to_choose_s1))

        title_result = title_task.get()
        screenshot_result = screenshot_task.get()

        print("\nResults:")
        print(title_result)
        print(screenshot_result)

        input("\nPress ENTER to close all drivers...")

        pool.map(cleanup_worker, range(2))
        print("All cleaned up ✅")
