import google.generativeai as genai
import requests
from PIL import Image
import io
import csv

from datetime import datetime

def log_entry(name, plate_number, file_path='logs.csv'):
    entry = {
        "Name": name,
        "Plate_number": plate_number,
        "Entry_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Exit_time": ""  # empty for now
    }

    file_exists = False
    try:
        with open(file_path, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Plate_number", "Entry_time", "Exit_time"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

def find_owner_by_plate(plate_number, filename='database.csv'):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['PlateNumber'].strip().upper() == plate_number.strip().upper():
                return row['Name']            
    return None

def has_active_entry(plate_number, file_path='logs.csv'):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Plate_number'] == plate_number and row['Exit_time'] == "":
                log_exit(plate_number)
                return True
    return False

def log_exit(plate_number, file_path='logs.csv'):
    updated_rows = []
    exit_logged = False

    # Read all rows and update the one that matches the plate and has no Exit_time
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Plate_number"] == plate_number and row["Exit_time"] == "":
                row["Exit_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                exit_logged = True
            updated_rows.append(row)

    # Write back all rows
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Plate_number", "Entry_time", "Exit_time"])
        writer.writeheader()
        writer.writerows(updated_rows)

    return exit_logged

# Step 1: Fetch image from ESP-EYE
esp_ip = "IP FROM ESP SERVER"  # Change if your ESP IP changes
url = f"http://{esp_ip}/capture"

print("[INFO] Downloading image from ESP-EYE...")
response = requests.get(url)
if response.status_code != 200:
    raise Exception("Failed to get image from ESP-EYE")

# Step 2: Convert raw JPEG bytes to PIL image
image = Image.open(io.BytesIO(response.content))
image = image.transpose(Image.FLIP_LEFT_RIGHT)

# Step 3: Authenticate and Send to Gemini
genai.configure(api_key="api key here")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
result = model.generate_content([
    "What is the plate number? Answer only the plate contents .",
    image
])
plate = result.text.strip()

# Step 4: Print the output
print("[PLATE NUMBER]",plate )

owner = find_owner_by_plate(plate)
if owner:
    if has_active_entry(plate)==False:
        log_entry(owner, plate)
    print(f"[INFO] Plate {plate} belongs to {owner}")
    
else:
    if has_active_entry(plate)==False:
        log_entry("Unauthorised person",plate)
    print(f"[WARNING] Plate {plate} not found in the database.")
    

