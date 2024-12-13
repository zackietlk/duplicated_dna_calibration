import os
import json

# Defining common paths
ROOT_DIR = "D:/work/MetaHuman-DNA-Calibration"
WORK_DIR = "D:/work/UnrealFest"
# Body file
orig_body_file = f"{WORK_DIR}/model/f_srt_unw_body_rig.ma"

# Temp folder
temp_dir = f"{WORK_DIR}/temp"

# Output folder
output_dir = f"{WORK_DIR}/output/scale"

# Create folders
if not os.path.exists(output_dir):
   os.makedirs(output_dir)
if not os.path.exists(temp_dir):
   os.makedirs(temp_dir)

# Scaled body files
scaled_skeleton_file = os.path.join(temp_dir, "scaled_skeleton_body.ma")
scaled_body_file = os.path.join(temp_dir, "scaled_body.ma")

########################### RIGGING PART ###############################################################################

# Scaling body

from maya import cmds

# Step 1: Open body scene
cmds.file(orig_body_file, options="v=0", type="mayaAscii", i=True)

# Step 2: Save skin cluster values in JSON file
for i in range(4):
    cmds.deformerWeights(f"body_lod{i}_sw.json", path=temp_dir, deformer=f"f_srt_unw_body_lod{i}_mesh_skinCluster",
                         weightPrecision=16, weightTolerance=0.0000001, export=True)

# Step 3: Manual work in Maya

# Scale body and unbind driver skeleton

cmds.select('root', replace=True)
cmds.select(hi=True)
cmds.delete(cmds.ls(sl=True, type='constraint'))

# Step 4: Read joints from skin cluster JSON file

################
def get_joints_from_file(file_path):
    deformer_data = {}
    with open(file_path) as def_file:
        deformer_data = json.load(def_file)

    joints_in_cluster = []
    children = deformer_data["deformerWeight"]["weights"]
    for child in children:
        joints_in_cluster.append(child["source"])
    print(joints_in_cluster)
    return joints_in_cluster
    # cmds.select(joints_in_cluster, add=True)

def load_skin_weights(mesh, path, file_name, max_influence):


    # create skinCluster
    joints = get_joints_from_file(path + "/" + file_name)
    if not joints:
        raise RuntimeError(f"Could not find joints in skinweights file {path}")
    joints.append(mesh)
    skinCluster = cmds.skinCluster(joints, tsb=True)[0]
    # zero everything, was seeing weird values perhaps from initial default weights.
    # cmds.skinPercent(skinCluster,mesh,pruneWeights=100,normalize=False)
    # load new weights
    cmds.deformerWeights(file_name, path=path, deformer=skinCluster, im=True, method='index')

    # set skinCluster settings
    cmds.setAttr(skinCluster + '.normalizeWeights', 1)
    cmds.skinCluster(skinCluster, e=True, forceNormalizeWeights=True)
    cmds.setAttr(skinCluster + '.maintainMaxInfluences', 1)
    cmds.setAttr(skinCluster + '.maxInfluences', max_influence)

for i in range(4):
    influence = 8
    if i == 3:
        influence = 4
    load_skin_weights(f"f_srt_unw_body_lod{i}_meshShape", temp_dir, f"body_lod{i}_sw.json", influence)
#############


# Step 5: Save body files
cmds.file(rename=str(scaled_body_file))
cmds.file(save=True, force=True)


# Step 5: Prepare skeleton file and save
cmds.file(rename=str(scaled_skeleton_file))
cmds.file(save=True, force=True)


########################################################################################################################
############# CALIBRATION PART #########################################################################################

from os import environ
from sys import path as syspath
from sys import platform
import contextlib

MAYA_VERSION = "2022"  # or 2023
ROOT_LIB_DIR = f"{ROOT_DIR}/lib/Maya{MAYA_VERSION}"
if platform == "win32":
    LIB_DIR = f"{ROOT_LIB_DIR}/windows"
elif platform == "linux":
    LIB_DIR = f"{ROOT_LIB_DIR}/linux"
else:
    raise OSError(
        "OS not supported, please compile dependencies and add value to LIB_DIR"
    )
DATA_DIR = f"{ROOT_DIR}/data"

# Add bin directory to maya plugin path
if "MAYA_PLUG_IN_PATH" in environ:
    separator = ":" if platform == "linux" else ";"
    environ["MAYA_PLUG_IN_PATH"] = separator.join([environ["MAYA_PLUG_IN_PATH"], LIB_DIR])
else:
    environ["MAYA_PLUG_IN_PATH"] = LIB_DIR

# Adds directories to path
syspath.insert(0, ROOT_DIR)
syspath.insert(0, DATA_DIR)
syspath.insert(0, LIB_DIR)

# Imports
from maya import cmds, mel

from dna_viewer import (
    DNA,
    Config,
    RigConfig,
    build_meshes,
    build_rig,
    get_skin_weights_from_scene,
    set_skin_weights_to_scene
)
from dnacalib import (
    CommandSequence,
    DNACalibDNAReader,
    RenameJointCommand,
    ScaleCommand,
    SetBlendShapeTargetDeltasCommand,
    SetVertexPositionsCommand,
    VectorOperation_Add,
    VectorOperation_Interpolate,
    SetNeutralJointTranslationsCommand,
    SetNeutralJointRotationsCommand,
    SetLODsCommand,
    TranslateCommand,
    SetSkinWeightsCommand,
    RemoveJointCommand,
    RotateCommand
)

from dna import (
    BinaryStreamReader,
    BinaryStreamWriter,
    DataLayer_All,
    FileStream,
    Status,
)
from vtx_color import MESH_SHADER_MAPPING, VTX_COLOR_MESHES, VTX_COLOR_VALUES


# Methods
def read_dna(path):
    stream = FileStream(path, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error loading DNA: {status.message}")
    return reader


def save_dna(reader, path):
    stream = FileStream(path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    writer.write()

    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error saving DNA: {status.message}")

    print(f"DNA {path} successfully saved.")


def assemble_scene(dna_path, analog_gui_path, gui_path,
                   additional_assemble_script):
    dna = DNA(dna_path)
    config = RigConfig(
        gui_path=gui_path,
        analog_gui_path=analog_gui_path,
        aas_path=additional_assemble_script,
        add_animated_map_attributes_on_root_joint=True,
        add_key_frames=True,
        add_mesh_name_to_blend_shape_channel_name=True
    )

    # Creates the rig
    build_rig(dna=dna, config=config)

    translation = cmds.xform("neck_01", ws=True, query=True, translation=True)
    cmds.xform("CTRL_faceGUI", ws=True, t=[translation[0] + 20, translation[1] + 5, translation[2]])


def prepare_rotated_dna(dna_path, rotated_dna_path):
    reader = read_dna(dna_path)

    # Copies DNA contents and will serve as input/output parameter to commands
    calibrated = DNACalibDNAReader(reader)

    # Modifies calibrated DNA in-place
    rotate = RotateCommand([90.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    rotate.run(calibrated)

    save_dna(calibrated, rotated_dna_path)
    return DNA(rotated_dna_path)


def get_dna(dna_path, rotated_dna_path):
    if up_axis == "z":
        return prepare_rotated_dna(dna_path, rotated_dna_path)
    return DNA(dna_path)


def build_meshes_for_lod(dna, lod):
    # Create config
    config = Config(
        group_by_lod=False,
        create_display_layers=False,
        lod_filter=[lod],
        add_mesh_name_to_blend_shape_channel_name=True,
    )

    # Builds and returns the created mesh paths in the scene
    return build_meshes(dna, config)


def create_skin_cluster(influences, mesh, skin_cluster_name, maximum_influences):
    cmds.select(influences[0], replace=True)
    cmds.select(mesh, add=True)
    skinCluster = cmds.skinCluster(
        toSelectedBones=True,
        name=skin_cluster_name,
        maximumInfluences=maximum_influences,
        skinMethod=0,
        obeyMaxInfluences=True,
    )
    if len(influences) > 1:
        cmds.skinCluster(
            skinCluster, edit=True, addInfluence=influences[1:], weight=0.0
        )
    return skinCluster


def create_head_and_body_scene(mesh_names, body_file, neck_joints, root_joint, facial_root_joints):
    scene_mesh_names = []
    skinweights = []

    for mesh_name in mesh_names:
        if cmds.objExists(mesh_name):
            scene_mesh_names.append(mesh_name)
            skinweights.append(get_skin_weights_from_scene(mesh_name))
            cmds.delete(f"{mesh_name}_skinCluster")

    for facial_joint in facial_root_joints:
        cmds.parent(facial_joint, world=True)
    cmds.delete(root_joint)

    cmds.file(body_file, options="v=0", type="mayaAscii", i=True)
    if up_axis == "y":
        cmds.joint("root", edit=True, orientation=[-90.0, 0.0, 0.0])
    for facial_joint, neck_joint in zip(facial_root_joints, neck_joints):
        cmds.parent(facial_joint, neck_joint)

    for mesh_name, skinweight in zip(scene_mesh_names, skinweights):
        create_skin_cluster(
            skinweight.joints,
            mesh_name,
            f"{mesh_name}_skinCluster",
            skinweight.no_of_influences,
        )
        set_skin_weights_to_scene(mesh_name, skinweight)


def set_fbx_options(orientation):
    # Executes FBX relate commands from the imported plugin
    min_time = cmds.playbackOptions(minTime=True, query=True)
    max_time = cmds.playbackOptions(maxTime=True, query=True)

    cmds.FBXResetExport()
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval(f"FBXExportBakeComplexStart -v {min_time}")
    mel.eval(f"FBXExportBakeComplexEnd -v {max_time}")
    mel.eval("FBXExportConstraints -v true")
    mel.eval("FBXExportSkeletonDefinitions -v true")
    mel.eval("FBXExportInputConnections -v true")
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportCameras -v false")
    mel.eval("FBXExportLights -v false")
    cmds.FBXExportUpAxis(orientation)
    # Deselects objects in Maya
    cmds.select(clear=True)


def create_shader(name):
    cmds.shadingNode("blinn", asShader=True, name=name)

    shading_group = str(
        cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{name}SG",
        )
    )
    cmds.connectAttr(f"{name}.outColor", f"{shading_group}.surfaceShader")
    return shading_group


def add_shader(lod):
    for shader_name, meshes in MESH_SHADER_MAPPING.items():
        shading_group = create_shader(shader_name)
        for mesh in meshes:
            if f"lod{lod}" in mesh:
                try:
                    cmds.select(mesh, replace=True)
                    cmds.sets(edit=True, forceElement=shading_group)
                except Exception as e:
                    print(f"Skipped adding shader for mesh {mesh}. Reason {e}")


def set_vertex_color(lod):
    for m, mesh_name in enumerate(VTX_COLOR_MESHES):
        try:
            if f"lod{lod}" in mesh_name:
                cmds.select(mesh_name)
                for v, rgb in enumerate(VTX_COLOR_VALUES[m]):
                    cmds.polyColorPerVertex(f"{mesh_name}.vtx[{v}]", g=rgb[1], b=rgb[2])
        except Exception as e:
            print(f"Skipped adding vtx color for mesh {mesh_name}. Reason {e}")
            continue


def export_fbx(lod_num, meshes, root_jnt, chr_name, fbx_dir):
    # Selects every mesh in the given lod
    for item in meshes:
        cmds.select(item, add=True)
    # Adds facial root joint to selection
    cmds.select(root_jnt, add=True)
    # Sets the file path
    export_file_name = f"{fbx_dir}/{chr_name}_lod{lod_num}.fbx"
    # Exports the fbx
    mel.eval(f'FBXExport -f "{export_file_name}" -s true')


def export_body_fbx(lod, mesh, body_root, fbx_dir):
    # Selects mesh
    cmds.select(mesh, add=True)
    # Adds facial root joint to selection
    cmds.select(body_root, add=True)
    # Sets the file path
    export_file_name = f"{fbx_dir}/{character_name}_body_lod{lod}.fbx"
    # Exports the fbx
    mel.eval(f'FBXExport -f "{export_file_name}" -s true')
    # Deselects all
    cmds.select(clear=True)



def export_fbx_for_lod(dna, lod, add_vtx_color, chr_name, body_file, fbx_dir, neck_joints, root_joint,
                       fbx_root_jnt, facial_root_joints, orientation):
    # Creates the meshes for the given lod
    result = build_meshes_for_lod(dna, lod)
    meshes = result.get_all_meshes()
    # Executes FBX relate commands from the imported plugin
    create_head_and_body_scene(meshes, body_file, neck_joints, root_joint, facial_root_joints)
    set_fbx_options(orientation)
    # Saves the result
    if add_vtx_color:
        add_shader(lod)
        set_vertex_color(lod)
    export_fbx(lod, meshes, fbx_root_jnt, chr_name, fbx_dir)


# Setting paths that will be used

# Original MH DNA
character_dna = f"{WORK_DIR}/dna/Lena.dna"

# Final DNA
final_dna = f"{WORK_DIR}/dna/Lena_resized.dna"

# Rotated DNA
rotated_dna = f"{WORK_DIR}/dna/Lena_rotated.dna"

# Result scene
review_scene = f"{temp_dir}/scaled_scene.mb"

# Scene misc files
gui_path = f"{DATA_DIR}/mh4/gui.ma"
analog_gui_path = f"{DATA_DIR}/analog_gui.ma"
aas_path = f"{DATA_DIR}/mh4/additional_assemble_script.py"

# Consts
up_axis = "z"
head_mesh = "head_lod0_mesh"
facial_root_joints = ["FACIAL_C_FacialRoot", "FACIAL_C_Neck1Root", "FACIAL_C_Neck2Root"]
neck_joints = ["head", "neck_01", "neck_02"]
root_joint = "spine_04"
facial_root = "FACIAL_C_FacialRoot"
fbx_root = "root"
character_name = "Lena"
add_vtx_color = True
#############################################


# DNA calibration steps

# Step 1: Scale whole rig
reader = read_dna(character_dna)
calibrated = DNACalibDNAReader(reader)
command = ScaleCommand(0.85, [0.0, 0.0, 0.0])
command.run(calibrated)

# Save DNA
save_dna(calibrated, final_dna)

# Step 2: Check result
assemble_scene(final_dna, analog_gui_path, gui_path, aas_path)
cmds.file(rename=review_scene)
cmds.file(save=True)
#
# ###################################################################################
# Export FBX
# Loads the builtin plugin needed for FBX
cmds.loadPlugin("fbxmaya.mll")

# Generate workspace.mel
mel.eval(f'setProject "{output_dir}";')

# Export FBX for each lod
cmds.upAxis(ax=up_axis)

dna_for_export = get_dna(final_dna, rotated_dna)
for lod_index in range(dna_for_export.get_lod_count()):
    export_fbx_for_lod(dna_for_export, lod_index, add_vtx_color,
                       character_name, scaled_skeleton_file, output_dir, neck_joints, root_joint, fbx_root,
                       facial_root_joints, up_axis)

with contextlib.suppress(FileNotFoundError):
    os.remove(rotated_dna)

cmds.file(force=True, new=True)
cmds.file(scaled_body_file, options="v=0", type="mayaAscii", i=True)
for lod in range(4):
    export_body_fbx(lod, f"f_srt_unw_body_lod{lod}_mesh", "root", output_dir)