from key_registry import KeyRegistry

def main():
    # Access the model builder for the 'models' category
    model_builder = KeyRegistry.access(category="models")

    # Build a CNN model
    cnn_model = model_builder.build(name="cnn", filters=64)
    print(f"Created model: {cnn_model}")

    # Build a LinearModel instance
    linear_model = model_builder.build(name="LinearModel", input_dim=784, output_dim=10)
    print(f"Created model: {linear_model}")

    # Build a ConvolutionalModel instance
    conv_model = model_builder.build(name="ConvolutionalModel", layers=3)
    print(f"Created model: {conv_model}")

    # Build an ExternalModel instance
    external_model = model_builder.build(name="ExternalModel")
    print(f"Created model: {external_model}")

    # Demonstrate error handling for unregistered model
    try:
        model_builder.build(name="UnknownModel")
    except KeyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()