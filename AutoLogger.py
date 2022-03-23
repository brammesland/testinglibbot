import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoLogger:

    def __init__(self, student):
        s = Service('/Users/konstantinasam/PycharmProjects/chromedriver_98')
        self.web = webdriver.Chrome(service=s)
        self.wait = WebDriverWait(self.web, 10)
        self.website = "https://eur-nl.libcal.com/r"
        self.student = student
        self.code = None

    def get_code(self):
        # To retrieve the code we have to check the outlook e-mail account
        outlookLogin = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1643724024&rver=7.0.6737.0&wp" \
                       "=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3db6ec5ca0" \
                       "-ed2e-16f2-8709-1c6e3fa784b3&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld" \
                       "&cobrandid=90015 "
        self.web.get(outlookLogin)

        # Log in procedure
        self.web.find_element(By.NAME, "loginfmt").send_keys(self.student.get_user_name())
        self.web.find_element(By.ID, "idSIButton9").click()

        # Redirected to the EUR site we fill in the password
        self.wait.until(EC.element_to_be_clickable((By.NAME, "Password")))
        self.web. find_element(By.NAME, "Password").send_keys(self.student.get_password())
        self.web.find_element(By.XPATH, "//*[@id=\"submitButton\"]").click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()

        
        time.sleep(0.5)
        self.web.find_element(By.CSS_SELECTOR, 'div[title="Library reservations"]').click()
        time.sleep(0.5)
        title = self.web.find_element(By.CSS_SELECTOR, 'div[role="option"]').get_attribute("aria-label")
        print(title.split("Enter this code: ")[1].split(" ")[0])

        while True:
            time.sleep(3)

    def log_in(self):
        self.web.get(self.website)

        # Fill in the code
        self.wait.until(EC.element_to_be_clickable((By.ID, "s-lc-new-reservation-checkin"))).click()
        fill_in_code_here = self.wait.until(EC.element_to_be_clickable((By.NAME, "code")))
        fill_in_code_here.click()
        fill_in_code_here.send_keys(self.code)

        # Submit and we are done
        self.wait.until(EC.element_to_be_clickable((By.ID, "s-lc-checkin-button"))).click()
        time.sleep(2)
        self.web.close()
