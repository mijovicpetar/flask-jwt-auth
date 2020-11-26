

class DataValidator:
    def __init__(self):
        self.validators = {}

    def register_validator(self, project_name, key, method):
        if self.validators.get('project_name') is None:
            self.validators[project_name] = {}

        self.validators[project_name] = {key: method}

    def get_validator(self, project_name, key):
        project = self.validators.get(project_name)
        if project is None:
            return None

        return project.get(key)
