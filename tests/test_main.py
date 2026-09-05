import unittest
import sys
import os

# Mock bpy module for testing outside Blender
class MockBpy:
    class types:
        class Operator:
            pass
        class Panel:
            pass
    class props:
        class FloatProperty:
            def __init__(self, **kwargs):
                pass
        class IntProperty:
            def __init__(self, **kwargs):
                pass
    class utils:
        @staticmethod
        def register_class(cls):
            pass
        @staticmethod
        def unregister_class(cls):
            pass

sys.modules['bpy'] = MockBpy

# Import the module under test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import blender_material_variant_generator as mvg

class TestMaterialVariantGenerator(unittest.TestCase):
    def test_classes_defined(self):
        self.assertTrue(hasattr(mvg, 'GenerateVariants'))
        self.assertTrue(hasattr(mvg, 'GenerateVariantsPanel'))
        
    def test_register_unregister(self):
        # Ensure register/unregister functions exist and are callable
        self.assertTrue(callable(mvg.register))
        self.assertTrue(callable(mvg.unregister))
        
    def test_operator_properties(self):
        # Check that operator has expected properties
        self.assertTrue(hasattr(mvg.GenerateVariants, 'hue_shift'))
        self.assertTrue(hasattr(mvg.GenerateVariants, 'roughness_offset'))
        self.assertTrue(hasattr(mvg.GenerateVariants, 'variant_count'))

if __name__ == '__main__':
    unittest.main()
