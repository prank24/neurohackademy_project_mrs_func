import zipfile
from pathlib import Path

# Define source directories and output directory
source_dirs = [
    Path(r"D:\neurohack_data\data"),
    Path.cwd(),  # Current working directory (.)
]
target_base_dir = Path(r"D:\neurohack_data\data\unzipped")

# Create output directory if it doesn't exist
target_base_dir.mkdir(parents=True, exist_ok=True)

for source_dir in source_dirs:
    # Find all .zip files matching the pattern
    zip_files = list(source_dir.glob("HCA*_*_MR_StructuralRecommended.zip"))
    
    for zip_path in zip_files:
        # Get folder name by stripping '.zip' extension
        folder_name = zip_path.stem
        extract_to_path = target_base_dir / folder_name

        print(f"Extracting: {zip_path.name} -> {extract_to_path}")

        # Extract contents into dedicated folder
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to_path)

print("\nDone! All files extracted successfully.")