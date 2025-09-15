"""
Sample plugin system scaffold
"""


class Plugin:
    def activate(self):
        print("Plugin activated!")


def load_plugins():
    # In real use, dynamically discover plugins
    return [Plugin()]
