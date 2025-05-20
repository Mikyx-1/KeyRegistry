import ast
import importlib
import os
import sys
from functools import lru_cache
from pathlib import Path


class ModelBuilder:
    def __init__(self, category, registry_map):
        self.category = category
        self.registry_map = registry_map  # Maps name to (module_path, parent_dir)

    def build(self, name, *args, **kwargs):
        if name not in self.registry_map:
            raise KeyError(
                f"No class named '{name}' registered in category '{self.category}'"
            )

        # Get module path and parent directory
        module_path, parent_dir = self.registry_map[name]
        original_sys_path = sys.path.copy()
        try:
            if parent_dir and parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)  # Add backbones/ to sys.path
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(f"Failed to import module for {name}: {e}")
        finally:
            sys.path[:] = original_sys_path  # Restore sys.path

        if (
            self.category not in KeyRegistry._registry
            or name not in KeyRegistry._registry[self.category]
        ):
            raise KeyError(
                f"No class named '{name}' registered in category '{self.category}' after import"
            )

        return KeyRegistry._registry[self.category][name](*args, **kwargs)


class KeyRegistry:
    _registry = {}

    @classmethod
    def register(cls, category, name=None):
        def decorator(class_):
            if category not in cls._registry:
                cls._registry[category] = {}
            # Use class name if name is not provided
            registry_name = name if name is not None else class_.__name__
            cls._registry[category][registry_name] = class_
            return class_

        return decorator

    @classmethod
    @lru_cache(maxsize=128)
    def _scan_project(cls, project_root, category):
        """Scan the project and return a registry_map."""
        registry_map = {}
        project_root = Path(project_root).resolve()
        for py_file in project_root.rglob("*.py"):
            if py_file.name.startswith("__"):  # Skip __init__.py
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for decorator in node.decorator_list:
                            if (
                                isinstance(decorator, ast.Call)
                                and isinstance(decorator.func, ast.Attribute)
                                and decorator.func.attr == "register"
                                and isinstance(decorator.func.value, ast.Name)
                                and decorator.func.value.id == "KeyRegistry"
                            ):
                                # Extract category and name from decorator arguments
                                kw_args = {
                                    kw.arg: kw.value for kw in decorator.keywords
                                }
                                if (
                                    kw_args.get("category")
                                    and isinstance(kw_args["category"], ast.Constant)
                                    and kw_args["category"].value == category
                                ):
                                    # Use class name if name is not provided
                                    name = (
                                        kw_args["name"].value
                                        if kw_args.get("name")
                                        and isinstance(kw_args["name"], ast.Constant)
                                        else node.name
                                    )
                                    parent_dir = str(py_file.parent.resolve())
                                    module_path = (
                                        py_file.stem
                                    )  # Use file name (e.g., "alexnet")
                                    registry_map[name] = (module_path, parent_dir)
            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"Warning: Could not parse {py_file}: {e}")

        return registry_map

    @classmethod
    def access(cls, category, project_root=None):
        if project_root is None:
            project_root = os.getcwd()
        project_root = str(Path(project_root).resolve())
        print(f"project_root: {project_root}")

        registry_map = cls._scan_project(project_root, category)
        return ModelBuilder(category, registry_map)
