import csv
import time
import serial

# === CONFIG ===
CSV_FILE = "logs.csv"
SERIAL_PORT = "COM6"  # Change this to your Arduino port
BAUD_RATE = 9600

# === FUNCTION: Get last log ===
def get_latest_plate_and_status():
    with open(CSV_FILE, 'r') as f:
        reader = list(csv.DictReader(f))
        if not reader:
            return None, None

        last_row = reader[-1]
        plate_number = last_row['Plate_number']
        access = "GRANTED" if last_row['Name'].strip().lower() != "unauthorised person" else "DENIED"
        return plate_number, access

# === MAIN ===
if __name__ == "__main__":
    print("[INFO] Checking latest entry...")
    plate_number, access_status = get_latest_plate_and_status()

    if not plate_number:
        print("[ERROR] No log found in CSV.")
        exit()

    print(f"[INFO] Last Plate: {plate_number}, Access: {access_status}")

    try:
        print("[INFO] Connecting to Arduino...")
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Wait for Arduino to reset

        message = f"{plate_number},{access_status}\n"
        arduino.write(message.encode())
        print("[INFO] Sent to Arduino:", message.strip())

        arduino.close()

    except serial.SerialException as e:
        print(f"[ERROR] Could not connect to Arduino: {e}")
