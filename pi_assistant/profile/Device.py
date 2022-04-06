

class Device:
    """
    Device - Defines an IoT device which can be controlled via a plugin.
    """
    def __init__(self, name: str, bind_to: str, metadata: dict = {}):
        self.name = name
        self.metadata = metadata
        self.bind_to = bind_to
