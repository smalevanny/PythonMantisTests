import string
import random

from model.project import Project

def random_string(prefix, max_length):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(max_length))])

def test_add_project(app):
    project = Project(name=random_string("project_name", 10), description=random_string("project description", 10))
    old_projects = app.project.get_projects_list()
    app.project.create(project)
    new_projects = app.project.get_projects_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)