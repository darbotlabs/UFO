"""
Minimal test to validate that UFO imports work correctly.
This helps ensure the basic installation is functional.
"""
import unittest
import sys
import importlib.util
import importlib
import os

# Temporarily suppress argparse errors from UFO
os.environ["UFO_TEST_MODE"] = "1"

class TestUfoImports(unittest.TestCase):
    """Test case for validating UFO imports."""

    def test_ufo_package_import(self):
        """Test that the UFO package can be imported."""
        try:
            import ufo
            self.assertTrue(True, "UFO package imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import UFO package: {e}")
            
    def test_ufo_module_existence(self):
        """Test that key UFO modules exist."""
        try:
            # Check for file existence rather than importing
            import ufo
            ufo_dir = os.path.dirname(ufo.__file__)
            
            core_files = ["__init__.py", "__main__.py", "ufo.py"]
            for file in core_files:
                path = os.path.join(ufo_dir, file)
                self.assertTrue(os.path.exists(path), f"Core file {file} does not exist")
                  self.assertTrue(True, "All UFO core files exist")
        except Exception as e:
            self.fail(f"Failed to check UFO module files: {e}")
            
    def test_critical_dependencies(self):
        """Test that critical dependencies are available."""
        critical_deps = [
            'azure.identity',
            'numpy',
            'torch',
            'langchain',
            'langchain_community',
            'openai',
            'html2text',
            'art',
            'uiautomation',
            'gradio_client'
        ]

        for dep in critical_deps:
            with self.subTest(dependency=dep):
                spec = importlib.util.find_spec(dep)
                self.assertIsNotNone(spec, f"Dependency {dep} not found")

if __name__ == "__main__":
    unittest.main()
