import threading
from tkinter import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class App(threading.Thread):
    def __init__(self):
        super().__init__()
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('window-size=800,600')
        self.driver = webdriver.Chrome(executable_path="./chromedriver", options=self.opt)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://ticket.interpark.com/Gate/TPLogin.asp"
        self.driver.get(self.url)
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("인터파크 티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()

        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, show="*", width=40)
        self.id_entry.grid(row=1, column=1)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, show="*", width=40)
        self.pw_entry.grid(row=2, column=1)
        self.login_button = Button(self.object_frame, text="Login", width=3, height=2, command=self.login_go)
        self.login_button.grid(row=3, column=1)
        self.showcode_label = Label(self.object_frame, text="공연번호")
        self.showcode_label.grid(row=4, column=0)
        self.showcode_entry = Entry(self.object_frame, width=40)
        self.showcode_entry.grid(row=4, column=1)
        self.showcode_button = Button(self.object_frame, text="직링", width=3, height=2, command=self.link_go)
        self.showcode_button.grid(row=5, column=1)
        self.calender_ladel = Label(self.object_frame, text="달력")
        self.calender_ladel.grid(row=6, column=0)
        self.calender_entry = Entry(self.object_frame, width=40)
        self.calender_entry.grid(row=6, column=1)
        self.date_label = Label(self.object_frame, text="날짜")
        self.date_label.grid(row=7, column=0)
        self.date_entry = Entry(self.object_frame, width=40)
        self.date_entry.grid(row=7, column=1)
        self.round_label = Label(self.object_frame, text="회차")
        self.round_label.grid(row=8, column=0)
        self.round_entry = Entry(self.object_frame, width=40)
        self.round_entry.grid(row=8, column=1)
        self.test_button = Button(self.object_frame, text="테스트", width=3, height=2, command=self.seat_select)
        self.test_button.grid(row=9, column=1)
        self.dp.mainloop()

    def login_go(self):
        def task():
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
            self.driver.find_element_by_name('userId').send_keys(self.id_entry.get())
            self.driver.find_element_by_id('userPwd').send_keys(self.pw_entry.get())
            self.driver.find_element_by_id('btn_login').click()

        newthread = threading.Thread(target=task)
        newthread.start()

    def link_go(self):
        def task():
            self.driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + self.showcode_entry.get())

        newthread = threading.Thread(target=task)
        newthread.start()

    def date_select(self):
        def task():
            while (True):
                try:
                    self.driver.switch_to.frame(self.driver.find_element_by_id('ifrmBookStep'))
                    if int(self.calender_entry.get()) == 0:
                        pass
                    elif int(self.calender_entry.get()) >= 1:
                        for i in range(1, int(self.calender_entry.get()) + 1):
                            self.driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/span[3]").click()
                    try:
                        self.driver.find_element_by_xpath(
                            '(//*[@id="CellPlayDate"])' + "[" + self.date_entry.get() + "]").click()
                        break
                    except NoSuchElementException:
                        self.link_go()
                        break
                except NoSuchElementException:
                    self.link_go()
                    break
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + self.round_entry.get() + ']/a'))).click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_id('LargeNextBtnImage').click()

        newthread = threading.Thread(target=task)
        newthread.start()

    def seat_select(self):
        def task():
            self.driver.switch_to.frame(self.driver.find_element_by_name("ifrmSeat"))
            self.driver.switch_to.frame(self.driver.find_element_by_name("ifrmSeatDetail"))
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')))
            seats = self.driver.find_elements_by_css_selector(
                'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
            print(len(seats))

        newthread = threading.Thread(target=task)
        newthread.start()


app = App()
app.start()
