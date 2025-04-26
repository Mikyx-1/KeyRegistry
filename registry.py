import os
import ast
import importlib
from pathlib import Path
from functools import lru_cache

class ModelBuilder:
    def __init__(self, category, registry_map):
        self.category = category
        self.registry_map = registry_map  # Maps name to module path

    def build(self, name, *args, **kwargs):
        if name not in self.registry_map:
            raise KeyError(f"No class named '{name}' registered in category '{self.category}'")
        
        # Import the module containing the class
        module_path = self.registry_map[name]
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(f"Failed to import module for {name}: {e}")
        
        # Access the registered class from Registry._registry
        if (self.category not in Registry._registry or 
                name not in Registry._registry[self.category]):
            raise KeyError(f"No class named '{name}' registered in category '{self.category}' after import")
        
        return Registry._registry[self.category][name](*args, **kwargs)

class Registry:
    _registry = {}
    _registry_map_cache = {}  # Cache for registry_map per category and project_root

    @classmethod
    def register(cls, category, name):
        def decorator(class_):
            if category not in cls._registry:
                cls._registry[category] = {}
            cls._registry[category][name] = class_
            return class_
        return decorator

    @classmethod
    @lru_cache(maxsize=128)
    def _scan_project(cls, project_root, category):
        """Scan the project and return a registry_map. Cached for performance."""
        registry_map = {}
        project_root = Path(project_root).resolve()
        for py_file in project_root.rglob("*.py"):
            if py_file.name.startswith("__"):  # Skip __init__.py
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source, filename=str(py_file))
                
                # Analyze the AST for class definitions with @Registry.register
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for decorator in node.decorator_list:
                            if (isinstance(decorator, ast.Call) and
                                    isinstance(decorator.func, ast.Attribute) and
                                    decorator.func.attr == "register" and
                                    isinstance(decorator.func.value, ast.Name) and
                                    decorator.func.value.id == "Registry"):
                                # Extract category and name from decorator arguments
                                kw_args = {kw.arg: kw.value for kw in decorator.keywords}
                                if (kw_args.get("category") and
                                        isinstance(kw_args["category"], ast.Constant) and
                                        kw_args["category"].value == category and
                                        kw_args.get("name") and
                                        isinstance(kw_args["name"], ast.Constant)):
                                    name = kw_args["name"].value
                                    # Convert file path to module path
                                    relative_path = py_file.relative_to(project_root)
                                    module_parts = relative_path.with_suffix("").parts
                                    module_path = ".".join(module_parts)
                                    registry_map[name] = module_path
            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"Warning: Could not parse {py_file}: {e}")
        
        return registry_map

    @classmethod
    def access(cls, category, project_root=None):
        if project_root is None:
            project_root = os.path.dirname(__file__)
        project_root = str(Path(project_root).resolve())  # Ensure string for cache key
        
        # Get or compute the registry_map (cached)
        registry_map = cls._scan_project(project_root, category)
        return ModelBuilder(category, registry_map)