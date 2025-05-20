from key_registry import KeyRegistry

@KeyRegistry.register(category="models", name="ConvolutionalModel")
class ConvolutionalModel:
    def __init__(self, layers):
        self.layers = layers

    def __repr__(self):
        return f"ConvolutionalModel(layers={self.layers})"