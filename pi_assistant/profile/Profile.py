import json
import os.path
from pi_assistant.log import logger
from pi_assistant.profile.Room import Room
from pi_assistant.profile.Group import Group


class Profile:
    """
    Profile - An object which encapsulates information about the user's home, rooms within the home, and groups
    of devices in the home. An existing profile can be loaded from a JSON file or JSON string when the application starts
    with the --profile argument.
    """
    def __init__(self):
        super().__init__()
        self.name = None
        self.rooms = []
        self.groups = []

    def save(self):
        path = os.path.join(".", "resources", "profiles", self.name + ".json")
        try:
            with open(path, 'w') as file:
                file.write(json.dumps(self, indent=4, default=lambda o: o.__dict__))
                file.close()
        except Exception as e:
            logger.error(f"Failed to save profile to disk. Path = {path}. Error = {str(e)}")

    @staticmethod
    def load_json_file(path: str):
        try:
            p = Profile()
            with open(path, 'r') as json_file:
                data = json.loads(json_file.read())
                for k, v in data.items():
                    if k == 'room':
                        r = Room(name=v['name'], devices=v['devices'])
                        p.rooms.append(r)
                    if k == 'group':
                        g = Group(name=v['name'], devices=v['devices'])
                        p.groups.append(g)
                    else:
                        setattr(p, k, v)
            return p
        except Exception as e:
            logger.error(f"Failed to load json profile from the path: {path}. Ensure the path is valid and points to a "
                         f"json profile file. You can use profile:create to create a new profile. Error = {str(e)}")

    def __str__(self):
        return f"Profile(name='{self.name}', groups='{len(self.groups)}', rooms='{len(self.rooms)}')"
