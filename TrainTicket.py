#!/usr/bin/env python
# encoding: utf-8
'''
@contact: shiwudaozhuan@163.com
@project: train_ticket
@author: zhibuyu
@file: TrainTicket.py
@time: 2018-12-26 09:19
@desc: 12306抢票
'''
from splinter.browser import Browser
from splinter.driver.webdriver.chrome import Options, Chrome
from configparser import ConfigParser
from time import sleep
import sys
import codecs
import argparse
import os
import time

class TrainTicket(object):

    # 读取配置文件
    def readConfig(self, config_file = 'config.ini'):
        print("加载配置文件...")
        path = os.path.join(os.getcwd(), config_file)
        cp = ConfigParser()
        try:
            cp.read_file(codecs.open(config_file, "r", "utf-8-sig"))
        except IOError as e:
            print(u'打开配置文件"%s"失败，请先创建一份config.ini' % (config_file))
            input('Press any key to continue')
            sys.exit()

        self.username = cp.get("login", "username")
        self.passwd = cp.get("login", "password")
        self.city = cp.get("cookieInfo", "starts")
        #始发站，终点站
        starts_city = cp.get("cookieInfo", "starts")
        self.starts = self.convertCityToCode(starts_city).encode('unicode_escape').decode("utf-8").replace("\\u", "%u").replace(",", "%2c")
        ends_city = cp.get("cookieInfo", "ends");
        self.ends = self.convertCityToCode(ends_city).encode('unicode_escape').decode("utf-8").replace("\\u", "%u").replace(",", "%2c")

        self.dtime = cp.get("cookieInfo", "dtime")
        #车次
        order_str = cp.get("orderItem", "order")
        self.order = int(order_str)
        self.users = cp.get("userInfo", "users").split(",")
        self.train_types = cp.get("trainInfo", "train_types").split(",")
        self.start_time = cp.get("trainInfo", "start_time")

        self.ticket_url = cp.get("urlInfo", "ticket_url")
        self.login_url = cp.get("urlInfo", "login_url")
        self.initmy_url = cp.get("urlInfo", "initmy_url")
        self.buy = cp.get("urlInfo", "buy")

        # 票种
        ticker_type = cp.get("tickerInfo", "ticker_type")
        self.tickerType = self.tickerMap[ticker_type] if ticker_type in self.tickerMap else ""

        seat_type = cp.get("confirmInfo", "seat_type")
        self.seatType = self.seatMap[seat_type] if seat_type in self.seatMap else ""

        noseat_allow = cp.get("confirmInfo", "noseat_allow")
        self.noseat_allow = 1 if int(noseat_allow) != 0 else 0

        self.driver_name = cp.get("pathInfo", "driver_name")
        self.executable_path = cp.get("pathInfo", "executable_path")

    def loadConfig(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', help='Specify config file, use absolute path')
        args = parser.parse_args()
        if args.config:
            self.readConfig(args.config)
        else:
            self.readConfig()

    def loadCityCode(self):
        print("映射出发地，目的地")
        city_codes = {}
        path = os.path.join(os.getcwd(), 'city_code.txt')
        with codecs.open(path, "r", "utf-8-sig") as f:
            for l in f.readlines():
                city = l.split(':')[0]
                code = l.split(':')[1].strip()
                city_codes[city] = city+","+code
            return city_codes

    def convertCityToCode(self,c):
        try:
            return self.city_codes[c]
        except KeyError:
            print("转换错误，修改config.ini中starts和ends城市名")
            return False

    def loadTickerType(self):
        self.tickerMap = {
            "儿童票": "2",
            "学生票": "3",
            "残军票": "4"
        }

    def loadSeatType(self):
        self.seatMap = {
            "硬座": "1",
            "硬卧": "3",
            "软卧": "4",
            "一等软座": "7",
            "二等软座": "8",
            "商务座": "9",
            "一等座": "M",
            "二等座": "O",
            "混编硬座": "B",
            "特等座": "P"
        }

    def __init__(self):
        self.city_codes = self.loadCityCode()
        self.loadTickerType()
        self.loadSeatType()
        self.loadConfig()

    def login(self):
        print("开始登陆")
        self.driver.visit(self.login_url)
        self.driver.fill("loginUserDTO.user_name", self.username)
        self.driver.fill("userDTO.password", self.passwd)

        print(u"等待输入验证码...")

        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break

    def searchMore(self):
        # 选择车次类型
        for type in self.train_types:
            train_type_dict = {'T':u'T-特快',
                               'G':u'GC-高铁/城际',
                               'D':u'D-动车',
                               'Z':u'Z-直达',
                               'K':u'K-快速'}
            if type == 'T' or type == 'G' or type == 'D' or type == 'Z' or type == 'K':
                print(u'--------->选择的车次类型', train_type_dict[type])
                self.driver.find_by_text(train_type_dict[type]).click()
            else:
                print(u"车次类型异常或未选择！(train_type=%s)"% type)

        print(u'--------->选择的发车时间', self.start_time)
        if self.start_time:
            # self.driver.find_option_by_text(self.start_time).first.cilck()
            self.driver.find_option_by_text(self.start_time).first.click()
        else:
            print(u"未指定发车时间，默认00:00-24:00")



    def preStart(self):
        # 加载查询信息
        # 出发地
        self.driver.cookies.add({"_jc_save_fromStation": self.starts})
        # 目的地
        self.driver.cookies.add({"_jc_save_toStation": self.ends})
        # 出发日
        self.driver.cookies.add({"_jc_save_fromDate": self.dtime})

    def specifyTrainNo(self):
        count = 0
        while self.driver.url == self.ticket_url:
            self.searchMore()
            sleep(0.3)
            self.driver.find_by_text(u"查询").click()
            count += 1
            # print(u"循环点击查询... 第%s次" % count)
            print(u"持续抢票... 第%s次" % count)

            try:
                self.driver.find_by_text(u"预订")[self.order-1].click()
                sleep(0.3)
            except Exception as e:
                print(e)
                print(u"还没开始预定")
                continue

    def buyOrderZero(self):
        count = 0
        while self.driver.url == self.ticket_url:
            self.searchMore()
            sleep(0.05)
            self.driver.find_by_text(u"查询").click()
            count += 1
            # print(u"循环点击查询... 第%s次" % count)
            print(u"持续抢票... 第%s次" % count)
            # if self.driver.find_by_id(u"ZE_550000D95610")
            try:
                for i in self.driver.find_by_text(u"预订"):
                    i.click()
                    sleep(0.3)

            except Exception as e:
                print(e)
                print(u"还没开始预定")
                continue

    def selUser(self):
        print(u"开始选择用户...")
        for user in self.users:
            print("选择用户",user)
            self.driver.find_by_text(user).last.click()

    def confirmTickerType(self):
        print(u"选择票种")
        if self.tickerType:
            print("票种",self.tickerType)
            self.driver.find_by_value(self.tickerType).click()
        else:
            print(u"未指定席别，按照12306默认成人票")


    def confirmOrder(self):
        print(u"选择席别")
        if self.seatType:
            self.driver.find_by_value(self.seatType).click()
        else:
            print(u"未指定席别，按照12306默认席别")

    def submitOrder(self):
        print(u"提交订单")
        sleep(2)
        self.driver.find_by_id('submitOrder_id').click()

    def confirmSeat(self):
        sleep(0.3)
        print("开始选座")
        if self.driver.find_by_text(u"硬座余票<strong>0</strong>张") == None:
            # self.driver.find_by_id('1F').click()
             self.driver.find_by_id('qr_submit_id').click()
        else:
            if self.noseat_allow == 0:
                self.driver.find_by_id('back_edit_id').click()
            elif self.noseat_allow == 1:
                self.driver.find_by_id('qr_submit_id').click()

    def buyTickets(self):
        t = time.process_time()
        try:
            print(u"购票开始")
            self.preStart()

            self.driver.reload()

            if self.order != 0:
                self.specifyTrainNo()
            else:
                print("test")
                self.buyOrderZero()

            print(u"开始预定...")
            sleep(0.8)
            self.selUser()
            self.confirmTickerType()
            self.confirmOrder()
            self.submitOrder()
            self.confirmSeat()

            print(time.process_time() - t)
        except Exception as e:
            print(e)

    def start(self):
        # 代理设置
        # PROXY = "119.101.113.139:9999"  #代理ip地址
        # chrome_options = Options()
        # chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
        # 使用代理ip访问，免费的最好不要用，12306很容易超时，可以自行购买代理ip
        # self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path,chrome_options=chrome_options)

        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        self.driver.driver.set_window_size(1400, 1000)
        self.login()
        self.driver.visit(self.ticket_url)
        self.buyTickets()

if __name__ == '__main__':
    print("begin:")
    Tickets = TrainTicket()
    Tickets.start()