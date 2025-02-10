# Author: Tomas Hodan (hodantom@cmp.felk.cvut.cz)
# Center for Machine Perception, Czech Technical University in Prague

"""
Visualizes object models in the ground-truth poses.
The script visualize datasets in the classical BOP19 format as well as the HOT3D dataset in H3 BOP24 format.
"""

import os
import argparse
import numpy as np

from bop_toolkit_lib import config
from bop_toolkit_lib import dataset_params
from bop_toolkit_lib import inout
from bop_toolkit_lib import misc
from bop_toolkit_lib import renderer
from bop_toolkit_lib import visualization

# Get the base name of the file without the .py extension
file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = misc.get_logger(file_name)

htt_available = False
try:
    from bop_toolkit_lib import pose_error_htt
except ImportError as e:
    logger.warning("""Missing hand_tracking_toolkit dependency
                mandatory if you are running evaluation on HOT3d.
                Refer to the README.md for installation instructions.
                """)
try:
    from bop_toolkit_lib import renderer_htt
    htt_available = True
except ImportError as e:
    logger.warning("""Missing hand_tracking_toolkit dependency,
                mandatory if you are running evaluation on HOT3d.
                Refer to the README.md for installation instructions.
                """)

# PARAMETERS.
################################################################################
p = {
    # See dataset_params.py for options.
    "dataset": "lm",
    # Dataset split. Options: 'train', 'val', 'test'.
    "dataset_split": "test",
    # Dataset split type. None = default. See dataset_params.py for options.
    "dataset_split_type": None,
    # File with a list of estimation targets used to determine the set of images
    # for which the GT poses will be visualized. The file is assumed to be stored
    # in the dataset folder. None = all images.
    # 'targets_filename': 'test_targets_bop19.json',
    "targets_filename": None,
    # Select ID's of scenes, images and GT poses to be processed.
    # Empty list [] means that all ID's will be used.
    "scene_ids": [],
    "im_ids": [],
    "gt_ids": [],

    # ---------------------------------------------------------------------------------
    # Next parameters apply only to classical BOP19 datasets (not the H3 BOP24 format)
    # ---------------------
    # Indicates whether to render RGB images.
    "vis_rgb": True,
    "vis_rgb_background": False,
    "vis_rect": True,
    "vis_3d_bounding_box": True,
    # Indicates whether to resolve visibility in the rendered RGB images (using
    # depth renderings). If True, only the part of object surface, which is not
    # occluded by any other modeled object, is visible. If False, RGB renderings
    # of individual objects are blended together.
    "vis_rgb_resolve_visib": True,
    # Indicates whether to save images of depth differences.
    "vis_depth_diff": True,
    # ---------------------------------------------------------------------------------

    # Whether to use the original model color.
    "vis_orig_color": True,
    # Type of the renderer (used for the VSD pose error function).
    "renderer_type": "vispy",  # Options: 'vispy', 'cpp', 'python'.
    # Folder containing the BOP datasets.
    "datasets_path": config.datasets_path,
    # Folder for output visualisations.
    "vis_path": os.path.join(config.output_path, "vis_gt_poses"),
    # Path templates for output images.
    "vis_rgb_tpath": os.path.join(
        "{vis_path}", "{dataset}", "{split}", "{scene_id:06d}", "{im_id:06d}.jpg"
    ),
    "vis_depth_diff_tpath": os.path.join(
        "{vis_path}",
        "{dataset}",
        "{split}",
        "{scene_id:06d}",
        "{im_id:06d}_depth_diff.jpg",
    ),
}
################################################################################
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
# Command line arguments.
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--dataset", default=p["dataset"], help="Dataset name.")
parser.add_argument("--model_type", default='default', help="choose from 'default' or 'eval', choose 'eval' to have no color")
parser.add_argument('--vis_rgb_background', type=str2bool, nargs='?', const=True, default=False, help="Visualize RGB background")
parser.add_argument('--vis_3d_bounding_box', type=str2bool, nargs='?', const=True, default=True, help="Visualize 3D bounding box")
parser.add_argument('--vis_rect', type=str2bool, nargs='?', const=True, default=False, help="Visualize rectangle")
parser.add_argument("--scene_ids", nargs="+", type=int, help="Scene ID's to be processed, separated by space.")
parser.add_argument("--im_ids", nargs="+", type=int, help="Image ID's to be processed, separated by space.")
parser.add_argument("--gt_ids", nargs="+", type=int, help="GT pose ID's to be processed, separated by space.")
args = parser.parse_args()
p["dataset"] = args.dataset
if args.scene_ids is not None:
    p["scene_ids"] = args.scene_ids
if args.im_ids is not None:
    p["im_ids"] = args.im_ids
if args.gt_ids is not None:
    p["gt_ids"] = args.gt_ids
p["vis_rgb_background"] = args.vis_rgb_background
p["vis_rect"] = args.vis_rect
p["vis_3d_bounding_box"] = args.vis_3d_bounding_box

if p["dataset"] == "hot3d" and not htt_available:
    raise ImportError("Missing hand_tracking_toolkit dependency, mandatory for HOT3D dataset.")

# if HOT3D dataset is used, next parameters are set
if p["dataset"] == "hot3d":
    p["vis_rgb"] = True
    p["vis_rgb_resolve_visib"] = False
    p["vis_depth_diff"] = False

# Load dataset parameters.
dp_split = dataset_params.get_split_params(
    p["datasets_path"], p["dataset"], p["dataset_split"], p["dataset_split_type"]
)
if args.model_type == 'default':
    model_type = None  # Default.
elif args.model_type == 'eval':
    model_type = "eval"  # None = default.
dp_model = dataset_params.get_model_params(p["datasets_path"], p["dataset"], model_type)

# Load colors.
colors_path = os.path.join(os.path.dirname(visualization.__file__), "colors.json")
colors = inout.load_json(colors_path)

# Subset of images for which the ground-truth poses will be rendered.
if p["targets_filename"] is not None:
    targets = inout.load_json(
        os.path.join(dp_split["base_path"], p["targets_filename"])
    )
    scene_im_ids = {}
    for target in targets:
        scene_im_ids.setdefault(target["scene_id"], set()).add(target["im_id"])
else:
    scene_im_ids = None

# List of considered scenes.
scene_ids_curr = dp_split["scene_ids"]
if p["scene_ids"]:
    scene_ids_curr = set(scene_ids_curr).intersection(p["scene_ids"])

# Rendering mode.
# if classical BOP19 format define render modalities
# The H3 BOP24 format for HOT3D does not include depth images, so this is irrelevant
if not p['dataset'] == "hot3d":
    renderer_modalities = []
    if p["vis_rgb"]:
        renderer_modalities.append("rgb")
    if p["vis_depth_diff"] or (p["vis_rgb"] and p["vis_rgb_resolve_visib"]):
        renderer_modalities.append("depth")
    renderer_mode = "+".join(renderer_modalities)

# Create a renderer.
# if HOT3D dataset, create separate renderers for Quest3 and Aria with different image sizes
if p["dataset"] == "hot3d":
    quest3_im_size = dp_split["quest3_im_size"][dp_split["quest3_eval_modality"]]
    aria_im_size = dp_split["aria_im_size"][dp_split["aria_eval_modality"]]
    quest3_ren = renderer_htt.RendererHtt(quest3_im_size, p["renderer_type"], shading="flat")
    aria_ren = renderer_htt.RendererHtt(aria_im_size, p["renderer_type"], shading="flat")
else:  # classical BOP format
    width, height = dp_split["im_size"]
    ren = renderer.create_renderer(
        width, height, p["renderer_type"], mode=renderer_mode, shading="phong"
    )
# Load object models.
models = {}
for obj_id in dp_model["obj_ids"]:
    misc.log("Loading 3D model of object {}...".format(obj_id))
    model_path = dp_model["model_tpath"].format(obj_id=obj_id)
    model_color = None
    if not p["vis_orig_color"]:
        model_color = tuple(colors[(obj_id - 1) % len(colors)])
    if p["dataset"] == "hot3d":
        quest3_ren.add_object(obj_id, model_path, surf_color=model_color)
        aria_ren.add_object(obj_id, model_path, surf_color=model_color)
    else:
        ren.add_object(obj_id, model_path, surf_color=model_color)
# Load model info
def get_3d_bbox(min_x, min_y, min_z, size_x, size_y, size_z):
    """
    Input: 
        scale: [3] or scalar
        shift: [3] or scalar
    Return 
        bbox_3d: [3, N]

    """
    bbox_3d = np.array([[+size_x, +size_y, +size_z],
                        [+size_x, +size_y, -size_z],
                        [-size_x, +size_y, +size_z],
                        [-size_x, +size_y, -size_z],
                        [+size_x, -size_y, +size_z],
                        [+size_x, -size_y, -size_z],
                        [-size_x, -size_y, +size_z],
                        [-size_x, -size_y, -size_z]]) + np.array([min_x, min_y, min_z])
    bbox_3d = bbox_3d.transpose()
    return bbox_3d

models_bbox_3d = {}
if p["vis_3d_bounding_box"]:
    models_info_path = dp_model["models_info_path"]  # path_to/models_info.json
    models_info = inout.load_json(models_info_path)
    models_bbox_3d = {int(obj_id): get_3d_bbox(info['min_x'], info['min_y'], info['min_z'], info['size_x'], info['size_y'], info['size_z']) for obj_id, info in models_info.items()}

scene_ids = dataset_params.get_present_scene_ids(dp_split)
for scene_id in scene_ids:
    tpath_keys = dataset_params.scene_tpaths_keys(dp_split["eval_modality"], scene_id)
    if p["dataset"] == "hot3d":  # for other dataset the renderer does not change
        # find which renderer to use (quest3 or aria)
        if scene_id in dp_split["test_quest3_scene_ids"] or scene_id in dp_split["train_quest3_scene_ids"]:
            ren = quest3_ren
        elif scene_id in dp_split["test_aria_scene_ids"] or scene_id in dp_split["train_aria_scene_ids"]:
            ren = aria_ren
    # Load scene info and ground-truth poses.
    scene_camera = inout.load_scene_camera(dp_split[tpath_keys["scene_camera_tpath"]].format(scene_id=scene_id))
    scene_gt = inout.load_scene_gt(dp_split[tpath_keys["scene_gt_tpath"]].format(scene_id=scene_id))
    # List of considered images.
    if scene_im_ids is not None:
        im_ids = scene_im_ids[scene_id]
    else:
        im_ids = sorted(scene_gt.keys())
    if p["im_ids"]:
        im_ids = set(im_ids).intersection(p["im_ids"])

    # Render the object models in the ground-truth poses in the selected images.
    for im_counter, im_id in enumerate(im_ids):
        if im_counter % 10 == 0:
            misc.log(
                "Visualizing GT poses - dataset: {}, scene: {}, im: {}/{}".format(
                    p["dataset"], scene_id, im_counter, len(im_ids)
                )
            )

        if p['dataset'] == 'hot3d':
            cam = pose_error_htt.create_camera_model(scene_camera[im_id])
        # TODO might delete if-else here
        else:
            cam = scene_camera[im_id]["cam_K"]

        # List of considered ground-truth poses.
        gt_ids_curr = range(len(scene_gt[im_id]))
        if p["gt_ids"]:
            gt_ids_curr = set(gt_ids_curr).intersection(p["gt_ids"])

        # Collect the ground-truth poses.
        gt_poses = []
        for gt_id in gt_ids_curr:
            gt = scene_gt[im_id][gt_id]
            # skip fully occluded masks - all values are -1
            if all(val == -1 for val in gt["cam_t_m2c"]):
                continue
            gt_poses.append(
                {
                    "obj_id": gt["obj_id"],
                    "R": gt["cam_R_m2c"],
                    "t": gt["cam_t_m2c"],
                    "text_info": [
                        {
                            "name": "",
                            "val": "{}:{}".format(gt["obj_id"], gt_id),
                            "fmt": "",
                        }
                    ],
                }
            )

        if p["dataset"] == "hot3d":
            # load the image of the eval modality
            rgb = inout.load_im(
                dp_split[dp_split["eval_modality"](scene_id) + "_tpath"].format(scene_id=scene_id, im_id=im_id)
            )
            # if image is grayscale (quest3), convert it to 3 channels
            if rgb.ndim == 2:
                rgb = np.dstack([rgb, rgb, rgb])
        else:
            # Load the color and depth images and prepare images for rendering.
            rgb = None
            if p["vis_rgb"]:
                if "rgb" in dp_split["im_modalities"] or p["dataset_split_type"] == "pbr":
                    rgb = inout.load_im(
                        dp_split["rgb_tpath"].format(scene_id=scene_id, im_id=im_id)
                    )[:, :, :3]
                    if p["vis_rgb_background"] is False:
                        rgb = np.zeros_like(rgb)
                elif "gray" in dp_split["im_modalities"]:
                    gray = inout.load_im(
                        dp_split["gray_tpath"].format(scene_id=scene_id, im_id=im_id)
                    )
                    rgb = np.dstack([gray, gray, gray])
                    if p["vis_rgb_background"] is False:
                        rgb = np.zeros_like(rgb)
                else:
                    raise ValueError("RGB nor gray images are available.")

        depth = None
        if p["dataset"] != "hot3d":
            if p["vis_depth_diff"] or (p["vis_rgb"] and p["vis_rgb_resolve_visib"]):
                depth = inout.load_depth(
                    dp_split["depth_tpath"].format(scene_id=scene_id, im_id=im_id)
                )
                depth *= scene_camera[im_id]["depth_scale"]  # Convert to [mm].

        # Path to the output RGB visualization.
        vis_rgb_path = None
        if p["vis_rgb"]:
            vis_rgb_path = p["vis_rgb_tpath"].format(
                vis_path=p["vis_path"],
                dataset=p["dataset"],
                split=p["dataset_split"],
                scene_id=scene_id,
                im_id=im_id,
            )

        # Path to the output depth difference visualization.
        vis_depth_diff_path = None
        if p["dataset"] != "hot3d":
            if p["vis_depth_diff"]:
                vis_depth_diff_path = p["vis_depth_diff_tpath"].format(
                    vis_path=p["vis_path"],
                    dataset=p["dataset"],
                    split=p["dataset_split"],
                    scene_id=scene_id,
                    im_id=im_id,
                )
        
        # Visualization.
        visualization.vis_object_poses(
            poses=gt_poses,
            K=cam,
            renderer=ren,
            rgb=rgb,
            depth=depth,
            vis_rgb_path=vis_rgb_path,
            vis_depth_diff_path=vis_depth_diff_path,
            vis_rgb_resolve_visib=p["vis_rgb_resolve_visib"],
            vis_rgb_background=p["vis_rgb_background"],
            vis_rect=p["vis_rect"],
            vis_3d_bounding_box=p["vis_3d_bounding_box"],
            models_bbox_3d=models_bbox_3d,
        )

misc.log("Done.")
