from auto_registry import AutoReg

@AutoReg.register(category="models", name="cnn")
class CNN:
    def __init__(self, filters=32):
        self.filters = filters

    def __repr__(self):
        return f"CNN(filters={self.filters})"