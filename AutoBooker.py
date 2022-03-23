import time
import datetime as dt
import Booking

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoBooker:

    def __init__(self, student):
        s = Service('/Users/konstantinasam/PycharmProjects/chromedriver_98')
        self.web = webdriver.Chrome(service=s)
        self.wait = WebDriverWait(self.web, 10)
        self.student = student



    def book(self):
        # The date to be booked lies one week ahead
        booking_date = str((dt.date.today() + dt.timedelta(days=7)).day)

        self.web.get(self.student.get_seat())

        # Navigate to calendar
        self.wait.until(EC.element_to_be_clickable((By.NAME, "loginfmt")))
        self.web.find_element(By.NAME, "loginfmt").send_keys(self.student.get_user_name())
        self.web.find_element(By.ID, "idSIButton9").click()

        self.wait.until(EC.element_to_be_clickable((By.NAME, "UserName")))
        self.web.find_element(By.NAME, "Password").send_keys(self.student.get_password())
        self.web.find_element(By.XPATH, "//*[@id=\"submitButton\"]").click()

        self.web.find_element(By.ID, "idSIButton9").click()

        # Click on the determined date
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"eq-time-grid\"]/div[1]/div[1]/button[1]"))).click()

        """            
        To find the day we are looking for we get all table dates from the datepicker object and compare their text to 
        the determined booking date
        """
        days = self.web.find_elements(By.CLASS_NAME, "day")

        to_be_booked = None
        for element in days:
            if element.text == booking_date:
                to_be_booked = element
                break

        if to_be_booked is None:
            raise OSError

        to_be_booked.click()

        """
        As time and button are stored in different containers we need two lists of containers. 
        Then select the time slots according to their index
        """
        self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "fc-event-title-container")))
        time_slots = self.web.find_elements(By.CLASS_NAME, "fc-event-title-container")
        i = 0
        if len(time_slots) == 32:
            slot_range = range(6, 20, 1)
        elif len(time_slots) == 22:
            slot_range = range(2, 16, 1)

        while i < len(time_slots):
            if i in slot_range:
                time_slots[i].click()
                time.sleep(1)

            i = i + 1

        # Now that the times are selected we can continue to submit
        self.wait.until(EC.element_to_be_clickable((By.ID, "submit_times"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "terms_accept"))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"s-lc-eq-bform-submit\"]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "s-lc-eq-auth-lobtn")))

        self.student.add_booking(Booking(booking_date))

        time.sleep(2)
        self.web.close()
