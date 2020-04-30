from __future__ import annotations

import requests
import typing

from best_testrail_client.custom_types import ModelID, Method, JsonData
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.section import Section
from best_testrail_client.models.status import Status
from best_testrail_client.models.template import Template
from best_testrail_client.models.user import User


class TestRailClient:
    def __init__(self, testrail_url: str, login: str, token: str):
        self.token = token
        self.login = login
        self.project_id: typing.Optional[ModelID] = None

        if not testrail_url.endswith('/'):
            testrail_url += '/'
        self.base_url = f'{testrail_url}index.php?/api/v2/'

    # Custom methods
    def set_project_id(self, project_id: ModelID) -> TestRailClient:
        self.project_id = project_id
        return self

    # Sections API
    def get_section(self, section_id: ModelID) -> Section:
        section_data = self.__request(f'get_section/{section_id}')
        return Section.from_json(section_data)

    def get_sections(
        self,
        project_id: typing.Optional[ModelID] = None, suite_id: typing.Optional[ModelID] = None,
    ) -> typing.List[Section]:
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        suite = f'?suite_id={suite_id}' if suite_id else ''
        sections_data = self.__request(f'get_sections/{project_id}{suite}')
        return [Section.from_json(section) for section in sections_data]

    def add_section(self, section: Section, project_id: typing.Optional[ModelID] = None) -> Section:
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        new_section_data = section.to_json()
        section_data = self.__request(
            f'add_section/{project_id}', method='POST', data=new_section_data,
        )
        return Section.from_json(section_data)

    def update_section(
        self, section_id: ModelID, name: str, description: typing.Optional[str] = None,
    ) -> Section:
        new_section_data = {'name': name}
        if description is not None:
            new_section_data['description'] = description
        section_data = self.__request(
            f'update_section/{section_id}', method='POST', data=new_section_data,
        )
        return Section.from_json(section_data)

    def delete_section(self, section_id: ModelID) -> bool:
        self.__request(f'delete_section/{section_id}', method='POST', _return_json=False)
        return True

    # Status API
    def get_statuses(self) -> typing.List[Status]:
        statuses_data = self.__request('get_statuses')
        return [Status.from_json(status) for status in statuses_data]

    # Templates API
    def get_templates(self, project_id: typing.Optional[ModelID] = None) -> typing.List[Template]:
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        templates_data = self.__request(f'get_templates/{project_id}')
        return [Template.from_json(template) for template in templates_data]

    # Users API
    def get_user(self, user_id: ModelID) -> User:
        user_data = self.__request(f'get_user/{user_id}')
        return User.from_json(user_data)

    def get_user_by_email(self, email: str) -> User:
        user_data = self.__request(f'get_user_by_email/{email}')
        return User.from_json(user_data)

    def get_users(self) -> typing.List[User]:
        users_data: typing.List[JsonData] = self.__request('get_users')
        return [User.from_json(user_data) for user_data in users_data]

    def __request(
        self, url: str, data: typing.Optional[JsonData] = None, method: Method = 'GET',
        _return_json: bool = True,
    ) -> typing.Any:
        if data is None:
            data = {}

        response = requests.request(
            method, f'{self.base_url}{url}', json=data,
            auth=(self.login, self.token),
        )

        if _return_json:
            return response.json()
        return response
