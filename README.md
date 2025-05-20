# KeyRegistry

KeyRegistry is a lightweight Python package designed to simplify dynamic class registration and instantiation in Python projects. It enables developers to register classes across a project using a decorator and instantiate them by name, without hardcoding import paths. This is particularly useful for projects with modular components, such as machine learning models, plugins, or extensible systems.

## What is KeyRegistry?

KeyRegistry provides a registry system that **automatically scans a project directory** for Python classes decorated with `@KeyRegistry.register`. It maps class names to their module locations, allowing dynamic instantiation of classes based on their registered names and categories. KeyRegistry eliminates the need to manually import modules or maintain a centralised list of classes, making it ideal for projects with many components or frequent additions.

Key features:
- **Automatic Discovery**: Scans project directories for registered classes using AST parsing.
- **Flexible Imports**: Supports dynamic imports without requiring package structures (e.g., `__init__.py` files).
- **Category-Based Organisation**: Groups classes by user-defined categories (e.g., "models", "plugins").
- **Convenient Registration**: Optionally uses class names as default registration names, requiring only a category.
- **Performance Optimisation**: Caches scan results to minimise overhead.

## What Can It Do?

KeyRegistry enables the following:
- **Register Classes Dynamically**: Use the `@KeyRegistry.register(category="category_name")` decorator to register classes, with an optional `name` parameter (defaults to the class name).
- **Instantiate Classes by Name**: Create instances of registered classes using a simple API, passing arbitrary arguments.
- **Support Non-Package Directories**: Works with directories lacking `__init__.py`, making it flexible for various project structures.
- **Handle Large Projects**: Efficiently scans and caches results for projects with many Python files.
- **Error Handling**: Provides clear error messages for missing classes, unimportable modules, or syntax errors in scanned files.

## Installation

To install KeyRegistry, install it as a Python package:

```bash
pip install KeyRegistry
```

### Requirements
- Python 3.6+
- No external dependencies

## How to Use It

### 1. Registering Classes
Decorate your classes with `@KeyRegistry.register`, specifying a `category` and an optional `name`. If `name` is omitted, the class name is used.

Example (`models/my_model.py`):
```python
from key_registry import KeyRegistry

@KeyRegistry.register(category="models")  # Name defaults to "MyModel"
class MyModel:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
```

Or, with a custom name:
```python
@KeyRegistry.register(category="models", name="CustomModel")
class MyModel:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
```

### 2. Instantiating Classes
Use the `KeyRegistry.access` and `ModelBuilder.build` methods to create instances.

Example:
```python
from key_registry import KeyRegistry

# Access the registry for a category
model_builder = KeyRegistry.access(category="models", project_root="/path/to/your/project")

# Instantiate a model
model = model_builder.build("MyModel", param1=1, param2="value")
print(model.param1)  # Output: 1
```

**The** `project_root` **parameter defaults to the current working directory if not specified.**

### 3. Project Structure
KeyRegistry scans all `.py` files in the specified `project_root` (recursively) for decorated classes. It works with or without `__init__.py` files in directories, making it flexible for various project layouts.

Example structure:
```
my_project/
├── models/
│   ├── my_model.py
│   ├── another_model.py
├── other_components/
│   ├── plugin.py
├── key_registry/
│   ├── __init__.py
│   ├── registry.py
├── main.py
```

### 4. Error Handling
KeyRegistry provides informative errors:
- `KeyError`: If the requested class name or category isn’t registered.
- `ImportError`: If a module cannot be imported (e.g., due to missing files or syntax errors).
- Warnings: Logged for files with syntax errors (e.g., mixed tabs and spaces).

## Examples of Situations Where KeyRegistry is Needed

1. **Machine Learning Projects**:
   - In a computer vision project with multiple models (e.g., `AlexNet`, `ResNet`, `UNet`), KeyRegistry allows you to register models in different files and instantiate them by name without manual imports. This is useful for experimenting with different architectures or adding new models without changing the main codebase.
   - Example: Register models in `backbones/alexnet.py` and `segmentation/unet.py`, then instantiate them dynamically in a training script.

2. **Plugin Systems**:
   - For applications with pluggable components (e.g., data processors, APIs), KeyRegistry enables developers to add new plugins by dropping Python files with decorated classes into a directory, without modifying import statements.

3. **Extensible Frameworks**:
   - In frameworks where users contribute components (e.g., custom optimisers, loss functions), KeyRegistry simplifies integration by automatically discovering and registering user-defined classes.

4. **Testing and Prototyping**:
   - When prototyping, KeyRegistry allows quick iteration by registering new classes in separate files, enabling dynamic instantiation for testing without hardcoding imports.

## Example Usage

### Example 1: Machine Learning Models
Project structure:
```
Computer-Vision-Models/
├── backbones/
│   ├── alexnet.py
├── segmentation/
│   ├── unet.py
├── main.py
```

`backbones/alexnet.py`:
```python
import torch
from torch import nn
from key_registry import KeyRegistry

@KeyRegistry.register(category="models")
class AlexNet(nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        # ... model definition ...
```

`main.py`:
```python
from key_registry import KeyRegistry

model_builder = KeyRegistry.access(category="models")
alex_net = model_builder.build("AlexNet", in_channels=3, num_classes=1000)
print(alex_net)  # Output: AlexNet(...)
```

### Example 2: Plugin System
Register plugins in a directory and instantiate them dynamically:
```python
from key_registry import KeyRegistry

plugin_builder = KeyRegistry.access(category="plugins", project_root="./plugins")
plugin = plugin_builder.build("MyPlugin", config="settings.yaml")
plugin.run()
```

## Author
- **Name**: Le Hoang Viet
- **Contact**: lehoangviet2k@gmail.com

## Contributing
Contributions are welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/Mikyx-1/KeyRegistry). To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## Licence
KeyRegistry is licensed under the [Apache License 2.0](LICENSE). See the LICENSE file for details.