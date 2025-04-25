from registry import Registry

@Registry.register(category="models", name="ExternalModel")
class ExternalModel:
    def __init__(self):
        pass

    def __repr__(self):
        return "ExternalModel()"