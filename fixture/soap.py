from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app, endpoint, username, password):
        self.app = app
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.client = Client(endpoint)

    def get_projects_list(self):
        projects = []
        try:
            soap_projects = self.client.service.mc_projects_get_user_accessible(self.username, self.password)
            for project in soap_projects:
                projects.append(Project(name=project.name, description=project.description, id=str(project.id)))
        except WebFault:
            print("Couldn't get projects list through SOAP API a Webfault has happened")
        return projects


