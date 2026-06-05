#pragma once

// Copy this file to wifi_config.h before flashing.
// Do not commit wifi_config.h because it contains local Wi-Fi credentials.
static const char* WIFI_SSID = "YOUR_WIFI_NAME";
static const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Laptop/backend IP must be reachable from the ESP32 network.
static const char* BACKEND_URL = "http://YOUR_LAPTOP_IP:8000/analyze";

