from selenium.webdriver.common.by import By

from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        # init project creation
        wd.find_element(By.CSS_SELECTOR, "input[value='Create New Project']").click()
        self.fill_project_form(project)
        # submit project creation
        wd.find_element(By.CSS_SELECTOR, "input[value='Add Project']").click()
        self.return_to_projects_page()
        self.projects_cache = None

    def delete(self, project):
        wd = self.app.wd
        self.open_projects_page()
        self.select_project(project)
        #deletion
        wd.find_element(By.CSS_SELECTOR, "input[value='Delete Project']").click()
        #second click on confirmation page
        if len(wd.find_elements(By.CSS_SELECTOR, "input[value='Update Project']")) == 0:
            wd.find_element(By.CSS_SELECTOR, "input[value='Delete Project']").click()
        self.projects_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field("name", project.name)
        self.change_field("description", project.description)

    def change_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element(By.NAME, field_name).click()
            wd.find_element(By.NAME, field_name).clear()
            wd.find_element(By.NAME, field_name).send_keys(text)

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements(By.CSS_SELECTOR, "input[value='Create New Project']")) > 0):
            wd.find_element(By.LINK_TEXT, "Manage").click()
            wd.find_element(By.LINK_TEXT, "Manage Projects").click()

    def select_project(self, project):
        wd = self.app.wd
        wd.find_element(By.CSS_SELECTOR, f"a[href='manage_proj_edit_page.php?project_id={project.id}']").click()

    def return_to_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements(By.CSS_SELECTOR, "input[value='Create New Project']")) > 0):
            wd.find_element(By.LINK_TEXT, "Proceed").click()

    def count(self):
        wd = self.app.wd
        self.open_projects_page()
        return len(wd.find_elements(By.XPATH, "//table[@class='width100']//tr[@class='row-1'] | //table[@class='width100']//tr[@class='row-2']"))

    projects_cache = None

    def get_projects_list(self):
        if self.projects_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.projects_cache = []
            for element in wd.find_elements(By.XPATH, "//table[@class='width100']//tr[@class='row-1'] | //table[@class='width100']//tr[@class='row-2']"):
                href_with_id = element.find_element(By.XPATH, "td[1]/a").get_attribute("href")
                id_start_index = str(href_with_id).index("=") + 1
                id = str(href_with_id)[id_start_index:]
                name = element.find_element(By.XPATH, "td[1]").text
                description = element.find_element(By.XPATH, "td[5]").text
                self.projects_cache.append(Project(name=name, description=description, id=id))
        return list(self.projects_cache)