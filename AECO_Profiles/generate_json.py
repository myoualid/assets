import os
import csv
import json
from pathlib import Path


def read_csv_profiles(csv_path):
    profiles = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            profile = {}
            psets = {}
            for col, val in row.items():
                col = col.strip()
                if col.startswith('Pset_'):
                    parts = col.split('.', 1)
                    if len(parts) == 2:
                        pset_name = parts[0]
                        prop_name = parts[1]
                        if val.strip():
                            psets.setdefault(pset_name, {})[prop_name] = val
                else:
                    if val.strip():
                        profile[col] = val
            if psets:
                profile['psets'] = [{name: props} for name, props in psets.items()]
            if profile.get('ProfileName', '').strip():
                profiles.append(profile)
    return profiles


def process_folders(base_path):
    main_dict = {}
    for folder in os.listdir(base_path):
        folder_path = Path(base_path) / folder
        if folder_path.is_dir():
            csv_path = folder_path / 'template.csv'
            if csv_path.exists():
                ifc_class = "Ifc" + folder + "ProfileDef"
                main_dict[ifc_class] = read_csv_profiles(csv_path)
    return main_dict


def main():
    base_path = Path(__file__).parent
    main_dict = process_folders(base_path)
    output_path = base_path / 'template.json'
    with open(output_path, 'w') as f:
        json.dump(main_dict, f, indent=4)
    print("template.json has been created successfully.")


if __name__ == "__main__":
    main()
