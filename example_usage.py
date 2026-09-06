"""
Demonstration of genpark-virtual-inmemory-module-importer-skill
"""

from client import VirtualModuleImporterClient

def main():
    importer = VirtualModuleImporterClient()

    # Dynamic synthetic module code
    calc_module_code = (
        "def compute_compound_growth(val, rate, periods):\n"
        "    return round(val * ((1 + rate) ** periods), 2)\n"
    )

    importer.register_module("virtual_finance_lib", calc_module_code)

    # Standard python import succeeds without any files written to disk!
    import virtual_finance_lib

    result = virtual_finance_lib.compute_compound_growth(1000, 0.07, 10)
    print("=== VIRTUAL IN-MEMORY MODULE IMPORT SUCCESS ===")
    print(f"Function imported: {virtual_finance_lib.compute_compound_growth.__name__}")
    print(f"Growth Result: {result}")

    # Cleanup
    importer.cleanup()

if __name__ == "__main__":
    main()
