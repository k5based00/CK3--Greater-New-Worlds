import os
import re
import shutil

# Function to convert old calendar dates to new calendar counterparts
def convert_calendar_dates(line):
    # Example conversion: replace years with NewEra
    pattern = r'(\d+)\.(\d{1,2})\.(\d{1,2})'
    
    def replace_date(match):
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))

        # Convert based on the provided rules
        if year >= 2:
            new_year = year + 2002
        else:
            new_year = year + 2000

        return f"{new_year}.{month}.{day}"

    converted_line = re.sub(pattern, replace_date, line)
    return converted_line

# Define the root directory to start searching
root_dir = "C:/Users/twsb1/Documents/Paradox Interactive/Crusader Kings III/mod/A-Greater-Earth-CK3-Mod-/Greater Earth/history"

# Define output directory for fixed files
output_dir = os.path.join(root_dir, 'history_fixed')

# Ensure the output directory exists or create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to process and copy the history folder
def process_and_copy_history(root_dir, output_dir):
    # Traverse through all files in the history directory and its subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file matches the .txt pattern
            if filename.endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                print(f"Processing file: {file_path}")

                try:
                    # Read the file contents
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_contents = f.readlines()

                    # Process each line and convert calendar dates
                    converted_lines = [convert_calendar_dates(line) for line in file_contents]

                    # Write the converted lines to the output file in history_fixed folder
                    output_file_path = os.path.join(output_dir, os.path.relpath(file_path, root_dir))
                    output_dirname = os.path.dirname(output_file_path)
                    if not os.path.exists(output_dirname):
                        os.makedirs(output_dirname)

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.writelines(converted_lines)

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    # Copy the entire history folder to history_fixed
    try:
        shutil.copytree(root_dir, output_dir)
        print(f"History folder copied to {output_dir}")
    except Exception as e:
        print(f"Error copying history folder: {e}")

# Call the function to process and copy the history folder
process_and_copy_history(root_dir, output_dir)

print("Conversion of calendar dates completed. Fixed files exported to history_fixed folder.")
