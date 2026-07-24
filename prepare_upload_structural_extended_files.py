"""
Copy files needed for connectome into a small staging
folder, then zip it for upload to JupyterHub.

The notebook only reads, per participant, from
  <local_dir>/<participant>_StructuralRecommended/<participant>/MNINonLinear/fsaverage_LR32k/:
    {participant}.L.inflated_MSMAll.32k_fs_LR.surf.gii
    {participant}.R.inflated_MSMAll.32k_fs_LR.surf.gii
    {participant}.curvature_MSMAll.32k_fs_LR.dscalar.nii
"""

import shutil
import sys
from pathlib import Path

LOCAL_DIR = Path(r"D:/neurohack_data/data/unzipped")
STAGING_DIR = Path(r"D:/neurohack_data/data/for_upload")

# Edit this list with the participants
_RAW_IDS = (
    "HCA6002236_V3, HCA6005242_V2, HCA6007044_V3, HCA6007044_V4, HCA6016146_V2, "
    "HCA6016146_V3, HCA6018857_V3, HCA6031344_V3, HCA6031344_V4, HCA6037457_V3, "
    "HCA6054457_V3, HCA6062456_V3, HCA6072156_V3, HCA6072156_V4, HCA6130548_V2, "
    "HCA6131449_V2, HCA6166973_V3, HCA6174770_V2, HCA6183064_V2, HCA6228767_V3, "
    "HCA6276475_V3, HCA6281872_V3, HCA6283371_V2, HCA6283371_V3, HCA6290368_V3, "
    "HCA6290368_V4, HCA6291976_V2, HCA6302349_V3, HCA6330152_V3, HCA6374576_V3, "
    "HCA6397992_V2, HCA6397992_V3, HCA6427066_V3, HCA6429272_V3, HCA6429272_V4, "
    "HCA6464678_V3, HCA6474782_V3, HCA6542470_V3, HCA7348277_V3, HCA7350567_V2, "
    "HCA7434674_V2, HCA7452272_V2, HCA7452575_V3, HCA7453981_V2, HCA7453981_V3, "
    "HCA7467588_V3, HCA7469592_V3, HCA7497395_V2, HCA7497901_V3, HCA7519581_V1, "
    "HCA7530670_V3, HCA7530670_V4, HCA7536884_V2"
)
PARTICIPANTS = [f"{pid.strip()}_MR" for pid in _RAW_IDS.split(",")]

REQUIRED_SUFFIXES = [
    "L.inflated_MSMAll.32k_fs_LR.surf.gii",
    "R.inflated_MSMAll.32k_fs_LR.surf.gii",
    "curvature_MSMAll.32k_fs_LR.dscalar.nii",
]


def stage_participant(participant: str) -> None:
    src_dir = (
        LOCAL_DIR
        / f"{participant}_StructuralRecommended"
        / participant
        / "MNINonLinear"
        / "fsaverage_LR32k"
    )
    dst_dir = STAGING_DIR / participant / "MNINonLinear" / "fsaverage_LR32k"
    dst_dir.mkdir(parents=True, exist_ok=True)

    for suffix in REQUIRED_SUFFIXES:
        src_file = src_dir / f"{participant}.{suffix}"
        if not src_file.is_file():
            print(f"  MISSING: {src_file}")
            continue
        shutil.copy2(src_file, dst_dir / src_file.name)
        print(f"  copied: {src_file.name}")


def main(participants: list[str]) -> None:
    if not participants:
        print("No participants given. Usage: python prepare_upload.py PARTICIPANT [PARTICIPANT ...]")
        sys.exit(1)

    for participant in participants:
        print(f"{participant}:")
        stage_participant(participant)

    zip_path = shutil.make_archive(str(STAGING_DIR), "zip", root_dir=STAGING_DIR)
    print(f"\nStaged files in: {STAGING_DIR}")
    print(f"Zip ready to upload: {zip_path}")


if __name__ == "__main__":
    main(sys.argv[1:] or PARTICIPANTS)
