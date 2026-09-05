import bpy
from bpy.props import FloatProperty, IntProperty
from math import pi

class GenerateVariants(bpy.types.Operator):
    bl_idname = "material.generate_variants"
    bl_label = "Generate Material Variants"
    bl_description = "Create color and roughness variants of selected materials"
    
    hue_shift: FloatProperty(default=0.0, min=-pi, max=pi)
    roughness_offset: FloatProperty(default=0.0, min=-1.0, max=1.0)
    variant_count: IntProperty(default=3, min=1, max=10)

    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for obj in selected:
            if not obj.data.materials:
                continue
                
            for i, mat in enumerate(obj.data.materials):
                if not mat.use_nodes:
                    continue
                    
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                
                # Find Principled BSDF
                bsdf = None
                for node in nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        bsdf = node
                        break
                        
                if not bsdf:
                    continue
                
                # Create variants
                for v in range(self.variant_count):
                    new_mat = mat.copy()
                    new_mat.name = f"{mat.name}_v{v+1}"
                    
                    if new_mat.use_nodes:
                        new_nodes = new_mat.node_tree.nodes
                        new_bsdf = None
                        for node in new_nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                new_bsdf = node
                                break
                        
                        if new_bsdf:
                            # Adjust base color
                            if 'Base Color' in new_bsdf.inputs:
                                color = new_bsdf.inputs['Base Color'].default_value
                                # Simple hue shift
                                h, s, v = color[:3]
                                h = (h + self.hue_shift / self.variant_count * v) % 1.0
                                new_bsdf.inputs['Base Color'].default_value = (h, s, v, 1.0)
                            
                            # Adjust roughness
                            if 'Roughness' in new_bsdf.inputs:
                                rough = new_bsdf.inputs['Roughness'].default_value
                                rough = max(0.0, min(1.0, rough + self.roughness_offset / self.variant_count * v))
                                new_bsdf.inputs['Roughness'].default_value = rough
                    
                    obj.data.materials.append(new_mat)
        
        return {'FINISHED'}

class GenerateVariantsPanel(bpy.types.Panel):
    bl_label = "Material Variants"
    bl_idname = "MATERIAL_OT_generate_variants_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Material Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator(GenerateVariants.bl_idname)
        layout.prop(GenerateVariants, "hue_shift")
        layout.prop(GenerateVariants, "roughness_offset")
        layout.prop(GenerateVariants, "variant_count")

classes = (GenerateVariants, GenerateVariantsPanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
