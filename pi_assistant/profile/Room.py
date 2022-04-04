

class Room:
    def __init__(self, **kwargs):
        super().__init__()

        if 'name' not in kwargs:
            raise Exception("Expected key word argument: 'name' to be present when creating a new room. "
                            "i.e Room(name='kitchen')")

        self.name = kwargs['name']
        if 'devices' in kwargs:
            self.devices = kwargs['devices']
        else:
            self.devices = []

    def __str__(self):
        return f"Room(name='{self.name}')"
