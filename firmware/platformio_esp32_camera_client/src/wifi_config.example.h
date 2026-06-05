#pragma once

// Copy this file to wifi_config.h before flashing.
// Do not commit wifi_config.h because it contains local Wi-Fi credentials.
static const char* WIFI_SSID = "YOUR_WIFI_NAME";
static const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Laptop/backend IP must be reachable from the ESP32 network.
static const char* BACKEND_URL = "http://YOUR_LAPTOP_IP:8000/analyze";

// Hardware pins. Change these to match your glasses wiring.
// Do not use camera pins from camera_pins.h. For Freenove, GPIO 6/7 are camera
// VSYNC/HREF, so they are not safe for buzzers when the camera is enabled.
#define ULTRASONIC_TRIG_GPIO 1
#define ULTRASONIC_ECHO_GPIO 2
#define BUZZER_LEFT_GPIO 41
#define BUZZER_RIGHT_GPIO 42

// Most simple active buzzers are active HIGH. Set to 0 if your module is active LOW.
#define BUZZER_ACTIVE_HIGH 1

// HC-SR04 echo is often 5V. Use a voltage divider/level shifter into ESP32 GPIO.
#define ULTRASONIC_MAX_DISTANCE_M 4.5f
