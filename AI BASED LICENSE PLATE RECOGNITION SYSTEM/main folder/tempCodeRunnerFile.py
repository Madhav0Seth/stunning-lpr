import csv

def find_owner_by_plate(plate_number, filename='database.csv'):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['PlateNumber'].strip().upper() == plate_number.strip().upper():
                return row['Name']            
    return None

# Example use
plate = "DL8CAF7654"
owner = find_owner_by_plate(plate)
if owner:
    print(f"[INFO] Plate {plate} belongs to {owner}")
else:
    print(f"[WARNING] Plate {plate} not found in the database.")