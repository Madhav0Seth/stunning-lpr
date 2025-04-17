#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // 0x27 is a common I2C address. Yours might be 0x3F — check if needed.
Servo myServo;

String input = "";
bool messageComplete = false;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  myServo.attach(9);
  myServo.write(0);

  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("plate number...");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      messageComplete = true;
      break;
    }
    input += c;
  }

  if (messageComplete) {
    Serial.println("Received: " + input);

    lcd.clear();
    int commaIndex = input.indexOf(',');
    if (commaIndex > 0) {
      String plate = input.substring(0, commaIndex);
      String status = input.substring(commaIndex + 1);

      lcd.setCursor(0, 0);
      lcd.print("Plate: " + plate);

      lcd.setCursor(0, 1);
      lcd.print("Access: " + status);

      if (status == "GRANTED") {
        myServo.write(90);  // Open gate
        delay(3000);        // Wait 3 seconds
        myServo.write(0);   // Close gate
      }
    } else {
      lcd.setCursor(0, 0);
      lcd.print("Invalid message");
    }

    input = "";
    messageComplete = false;
  }
}
