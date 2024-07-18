import os
import re
import logging
import codecs
from collections import defaultdict

# Path to the landed_titles folder
landed_titles_path = "C:/Users/twsb1/Documents/Paradox Interactive/Crusader Kings III/mod/A-Greater-Earth-CK3-Mod-/Greater Earth/common/landed_titles" ##put your landed_titles directory here 
# Supported languages
languages = ["english", "french", "german", "spanish"]

# Configure logging
logging.basicConfig(filename='localization_script.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def parse_landed_titles(file_path):
    titles = defaultdict(dict)
    current_title = None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                title_match = re.match(r"([ekcbd]_[\w\d_]+)\s*=\s*\{", line)
                name_match = re.match(r'name\s*=\s*"(.*?)"', line)
                
                if title_match:
                    current_title = title_match.group(1)
                    titles[current_title]['name'] = current_title  # Default name to ID
                    logging.debug(f"Found title: {current_title}")
                elif name_match and current_title:
                    titles[current_title]['name'] = name_match.group(1)
                    logging.debug(f"Found name for {current_title}: {name_match.group(1)}")
                elif line == "}":
                    current_title = None
    except Exception as e:
        logging.error(f"Error parsing landed titles file: {e}")
    
    return titles

def format_title_name(title_id):
    name_parts = title_id.split('_')[1:]
    formatted_name = ' '.join([part.capitalize() for part in name_parts])
    return formatted_name

def generate_localization(titles, languages):
    localizations = {lang: [] for lang in languages}
    try:
        for title_id, data in titles.items():
            formatted_name = format_title_name(data.get('name', title_id))
            
            # Regular title localization
            regular_entry = f"{title_id}:0 \"{formatted_name}\""
            for lang in languages:
                localizations[lang].append(regular_entry)
                logging.debug(f"Localized {title_id} for {lang}: {formatted_name}")
            
            # Adjective localization
            adjective_entry = f"{title_id}_adj:0 \"{formatted_name}\""
            for lang in languages:
                localizations[lang].append(adjective_entry)
                logging.debug(f"Localized {title_id}_adj:0 \"{formatted_name}\" for {lang}")
    except Exception as e:
        logging.error(f"Error generating localization: {e}")
    
    return localizations

def write_localization_files(localizations, output_dir):
    try:
        for lang, lines in localizations.items():
            lang_dir = os.path.join(output_dir, lang)
            if not os.path.exists(lang_dir):
                os.makedirs(lang_dir)
            file_name = f"0000001xxxx_landed_titles_l_{lang}.yml"
            with codecs.open(os.path.join(lang_dir, file_name), 'w', encoding='utf-8-sig') as file:
                file.write(f"l_{lang}:\n")
                for line in lines:
                    file.write(f" {line}\n")
            logging.info(f"Wrote {len(lines)} lines to {lang_dir}/{file_name}")
    except Exception as e:
        logging.error(f"Error writing localization files: {e}")

def main():
    try:
        titles = parse_landed_titles(os.path.join(landed_titles_path, "00_landed_titles.txt"))
        if not titles:
            logging.error("No titles found. Please check the input file.")
        localizations = generate_localization(titles, languages)
        write_localization_files(localizations, "output/localization")
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
