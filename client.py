"""
In-Memory Virtual Module Loader via sys.meta_path.
Zero external dependencies, standard library only.
"""

import sys
import types
from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec
from typing import Dict, Any, Optional

class VirtualModuleLoader(Loader):
    def __init__(self, code_str: str):
        self.code_str = code_str

    def create_module(self, spec: ModuleSpec) -> Optional[types.ModuleType]:
        return None # Use default module creation

    def exec_module(self, module: types.ModuleType):
        exec(self.code_str, module.__dict__)

class VirtualModuleFinder(MetaPathFinder):
    def __init__(self, virtual_registry: Dict[str, str]):
        self.registry = virtual_registry

    def find_spec(self, fullname: str, path: Any, target: Any = None) -> Optional[ModuleSpec]:
        if fullname in self.registry:
            loader = VirtualModuleLoader(self.registry[fullname])
            return ModuleSpec(fullname, loader)
        return None

class VirtualModuleImporterClient:
    """
    Dynamically exposes string code as importable modules without file I/O:
    - Registers custom finder into sys.meta_path
    - Supports standard 'import module_name' syntax in agent code
    - Unregisters cleanly upon cleanup
    """

    def __init__(self):
        self.virtual_modules: Dict[str, str] = {}
        self.finder = VirtualModuleFinder(self.virtual_modules)
        if self.finder not in sys.meta_path:
            sys.meta_path.insert(0, self.finder)

    def register_module(self, module_name: str, code_str: str):
        """Registers Python code string under specified module import path."""
        self.virtual_modules[module_name] = code_str

    def unregister_module(self, module_name: str):
        """Removes module from virtual registry and sys.modules."""
        if module_name in self.virtual_modules:
            del self.virtual_modules[module_name]
        if module_name in sys.modules:
            del sys.modules[module_name]

    def cleanup(self):
        """Removes finder from sys.meta_path."""
        if self.finder in sys.meta_path:
            sys.meta_path.remove(self.finder)
