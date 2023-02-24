"""
    Description: File Parsing.py

    Contains functionality needed to parse schedule site of KPI using only group name
    To get a schedule, an object of class Parser should be created and
    method "parse" called.

    Input: group (str)
    Output: data (dict)

    Authors: Ivan Skorobagatko
    Version: 0.1 (beta-debug)
"""

import requests
import time
from bs4 import BeautifulSoup


class Parser:
    """
        Class Parser
        Available methods to execute: parse(group)
        Takes "group" - a str variable / name of group from which schedule should be parsed
        Use Ukrainian language !
        Outputs dict object with whole schedule for both weeks
    """

    def __init__(self):
        """ Contains starting and processed values """
        # Request library data
        self.start_url = "http://epi.kpi.ua/Schedules/ScheduleGroupSelection.aspx"
        self.last_url = ""
        self.response = None
        self.retry_counter = 0

        # Parse data
        self.soup = None
        self.payload = {}
        self.data = []
        self.parsed_data = {}

    def _response_handler(self, url: str, method: str):
        """
            Handles responses from "response" library
            Can raise exceptions, but not meant to be used anywhere else.
            Also will raise exception if response has no callback. (For future restart)

            :param url: url of site to handle (string)
            :param method: method of request (get() or post() only)
        """
        if self.retry_counter > 5:
            raise Exception("Response wasn't handled in time")

        if method == "get":
            try:
                self.response = requests.get(url, timeout=5)
                self.retry_counter = 0
            except requests.exceptions.Timeout:
                print("Timed out. Retrying...")
                self.retry_counter += 1
                time.sleep(0.5)
                self._response_handler(url, method="get")
        elif method == "post":
            try:
                if self.payload == {}:
                    raise Exception("[Failure] Payload is empty")
                # allow_redirects param might be reconsidered in a future versions
                self.response = requests.post(url, data=self.payload, timeout=5, allow_redirects=False)
                self.retry_counter = 0
            except requests.exceptions.Timeout:
                print("Timed out. Retrying...")
                self.retry_counter += 1
                time.sleep(0.5)
                self._response_handler(url, method="post")
        else:
            raise Exception("[Failure] Violation function usage")

    def _payload_creator(self, group: str):
        """
            Created data for post request
            Needs for at least one response from KPI schedule site

            :param group: selected group (string)
        """
        if self.response is None:
            raise Exception("[Failure] Response wasn't handled at least once")

        self.soup = BeautifulSoup(self.response.text, "html.parser")
        inputs = self.soup.find_all("input")
        temp_array = []

        for field in inputs:
            try:
                temp_array.append((field["name"], field["value"]))
            except KeyError:
                temp_array.append((field["name"], f"{group}"))

        for elem in temp_array:
            self.payload[f"{elem[0]}"] = elem[1]

    def _trans_data(self):
        """
            Since main parser function goes row by row, the output data will have first classes, then second and so on.
            For DB, it's better to reverse parsed data to be first Monday, then Tuesday and so on.

            :return: formatted data
        """
        output_data = [[] for _ in range(len(self.data[0]))]
        for data in self.data:
            for index, elem in enumerate(data):
                output_data[index].append(elem)

        return output_data

    def _parser(self, param: str):
        """
            Function that parses response with schedule in it

            :param param: needed to select each table separately
        """
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.data.clear()
        temp_data = []

        for items in self.soup.select(f"{param}"):
            temp_data.append(items.select("td"))
        temp_data.pop(0)

        for items in temp_data:
            items.pop(0)
            formatted_data = []
            for pos in range(len(items)):
                if items[pos].text == "":
                    formatted_data.append(None)
                else:
                    par = [item.text for item in items[pos].select("span a")]
                    part = [item.text for item in items[pos].select("a")]
                    subject = ", ".join([subj for subj in part if subj in par])
                    professor = ", ".join(
                        [prof for prof in part if prof not in par and prof not in part[len(part) - 1]])
                    type_of_subject = part[len(part) - 1][4::]
                    formatted_data.append((subject, professor, type_of_subject))
            self.data.append(formatted_data)

    def _url_generator(self):
        """
            Simple function that makes link to a needed schedule.
            Might get deleted in future.
        """
        self.last_url = "http://epi.kpi.ua" + self.response.headers["Location"]

    def parse(self, group: str) -> dict:
        """
            Main parsing function that should be called to get a schedule.


            :param group: Takes the name of group (str). This should be written in Ukraine language.
            :return: Returns dictionary with schedule in it.
        """
        self.parsed_data.clear()
        self._response_handler(url=self.start_url, method="get")

        self._payload_creator(group=group)
        self._response_handler(url=self.start_url, method="post")
        if self.response.status_code != 302:
            raise Exception("Group doesn't exist. Please, check if the name is written properly")

        self._url_generator()
        self._response_handler(url=self.last_url, method="get")

        self._parser(param="table#ctl00_MainContent_FirstScheduleTable tr")
        self.parsed_data["week1"] = self._trans_data()
        self._parser(param="table#ctl00_MainContent_SecondScheduleTable tr")
        self.parsed_data["week2"] = self._trans_data()

        return self.parsed_data

# Test section
# WARNING. This file isn't meant to ever be executable. Section below contains some test-purpose code
# It will be removed in release version

# parser = Parser()

# print(parser.parse(group="ІО-11"))
# print(parser.parse(group="ІО-12"))
# print(parser.parse(group="ІО-13"))
# print(parser.parse(group="ІО-14"))
# print(parser.parse(group="ІО-15"))
# print(parser.parse(group="ІО-16"))
# This code will prompt Exception
# print(parser.parse(group="IO-13"))
