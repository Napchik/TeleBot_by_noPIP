"""
    Description: File parsing.py

    Contains functionality needed to parse schedule site of KPI using only group name
    To get a schedule, an object of class Parser should be created and method "parse" called.

    Input: group (str)
    Output: schedule (dict)

    Authors: Ivan Skorobagatko
    Version: 1.0 (release)
"""

import requests
import time
import re

from loger_config import logger
from bs4 import BeautifulSoup
import Database.db_function_user as db_function


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
        self.types = ['Лек on-line', 'Прак on-line', 'Лаб on-line']

    def _response_handler(self, url: str, method: str):
        """
            Handles responses from "response" library
            Can raise exceptions if response wasn't called back in time or
            function usage was violated.

            :param url: url of site to handle (string)
            :param method: method of request ("get" or "post" only)
        """
        if self.retry_counter > 5:
            raise Exception("Response wasn't handled in time")

        if method == "get":
            try:
                self.response = requests.get(url, timeout=5)
                self.retry_counter = 0
            except requests.exceptions.Timeout:
                self._request_retry(url=url, method=method)
        elif method == "post":
            try:
                if self.payload == {}:
                    raise Exception("[Failure] Payload is empty")
                self.response = requests.post(url, data=self.payload, timeout=5, allow_redirects=False)
                self.retry_counter = 0
            except requests.exceptions.Timeout:
                self._request_retry(url=url, method=method)
        else:
            raise Exception("[Failure] Violation function usage")

    def _request_retry(self, url: str, method: str):
        """
            Retries connecting to the server.
            Calls _response_handler()

            :param url: url of site to handle (string)
            :param method: method of request ("get" or "post" only)
        """
        logger.info("Connection was timed out. Retrying...")
        self.retry_counter += 1
        time.sleep(0.5)
        self._response_handler(url=url, method=method)

    def _payload_creator(self, group: str) -> dict:
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

    def _trans_data(self) -> dict:
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
                    select1 = [item.text for item in items[pos].select("span a")]
                    select2 = [item.text for item in items[pos].select("a")]
                    subject = ", ".join([subj for subj in select2 if subj in select1])
                    type_of_subject = ", ".join(
                        [item for item in self.types if re.search(item, " ".join(select2)) is not None])
                    professor = [prof for prof in select2 if prof not in select1]
                    professor = [prof for prof in professor if
                                 not re.search(" ".join(re.split('\\s', prof)[-2::]), " ".join(self.types))]
                    professor = ", ".join(professor)
                    formatted_data.append((subject, professor, type_of_subject))
            self.data.append(formatted_data)

    def parse(self, group: str) -> dict:
        """
            Main parsing function that should be called to get a schedule.

            :param group: Takes the name of group (str). This should be written in Ukraine language.
            :return: Returns dictionary with schedule if success, otherwise - empty dict.
        """
        logger.info(f"Started parsing group '{group}'")
        self.parsed_data.clear()
        self._response_handler(url=self.start_url, method="get")

        self._payload_creator(group=group)
        self._response_handler(url=self.start_url, method="post")
        if self.response.status_code != 302:
            logger.critical(f"Group '{group}' doesn't exists")
            db_function.delete_group(group)
            return self.parsed_data

        self.last_url = "http://epi.kpi.ua" + self.response.headers["Location"]
        self._response_handler(url=self.last_url, method="get")

        self._parser(param="table#ctl00_MainContent_FirstScheduleTable tr")
        self.parsed_data["week1"] = self._trans_data()
        self._parser(param="table#ctl00_MainContent_SecondScheduleTable tr")
        self.parsed_data["week2"] = self._trans_data()

        logger.info(f"Group '{group}' has been parsed successful")
        return self.parsed_data
