#include "app_httpd.h"

#define LED 21

void capture(const String& localIP) {
  digitalWrite(LED, HIGH);
  uint32_t number = random(40000000);

  String capture_url = "http://" + localIP + "/capture?_cb=" + String(number);
  Serial.println("Photo captured!");
  Serial.println("Image URL: " + capture_url);

  delay(1000);
  digitalWrite(LED, LOW);
}

void startCameraServer() {
  // Implement your camera server here or call built-in server start
  Serial.println("Starting camera server...");

  // Placeholder - replace with actual server setup
}
