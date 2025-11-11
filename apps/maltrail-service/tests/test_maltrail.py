# Maltrail Service Tests

import os
import sys
import unittest

# Add the src directory to the path so we can import maltrail modules
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'src'))


class TestMaltrailCore(unittest.TestCase):
    """Basic tests for Maltrail core functionality"""

    def test_imports(self):
        """Test that core modules can be imported"""
        try:
            import maltrail.core.common
            import maltrail.core.settings

            # Test passes if imports succeed
            pass
        except ImportError as e:
            self.fail(f"Failed to import core modules: {e}")

    def test_configuration_loading(self):
        """Test that configuration can be loaded"""
        try:
            import maltrail.core.settings as settings

            # Basic test - ensure settings module can be loaded
            self.assertIsNotNone(settings)
        except ImportError as e:
            self.fail(f"Failed to import settings module: {e}")


if __name__ == '__main__':
    unittest.main()
