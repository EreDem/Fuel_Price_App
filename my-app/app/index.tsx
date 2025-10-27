import { fuel_pump_icon, location_icon } from "@/assets/svgs";
import { useState } from "react";
import { Text, TouchableOpacity, View } from "react-native";
import { SheetManager } from "react-native-actions-sheet";

export default function Index() {
  // Functions
  // Open Dropdown Sheet
  const openDropdown = (id: string) => {
    SheetManager.show(id);
  };

  // Variables
  const fuel_stations = ["Aral", "Shell", "Jet", "PM", "BFT", "Total"];
  const fuel_types = ["Diesel", "E5", "E10"];
  const time_frames = ["24 Stunden", "48 Stunden", "72 Stunden"];

  const [selected_station, setSelectedStation] = useState("Jet");
  const [selected_fuel, setSelectedFuel] = useState("E5");
  const [time_frame, setTimeFrame] = useState("48 Stunden");

  // Styles
  const button_style = {
    height: 33,
    backgroundColor: "#9ACBD0",
    borderRadius: 10,
    paddingHorizontal: 5,
    justifyContent: "space-between" as const,
    alignItems: "center" as const,
    flexDirection: "row" as const,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  };

  return (
    // main view
    <View
      style={{
        justifyContent: "center",
        width: "100%",
        height: "100%",
        backgroundColor: "#FFFFFF",
      }}
    >
      {/* Welcome text view */}
      <View
        style={{
          top: -25,
          margin: "auto",
          width: "90%",
          padding: 16,
          height: 128,
          backgroundColor: "#FFF5F0FF",
          borderTopLeftRadius: 0,
          borderTopRightRadius: 0,
          borderBottomRightRadius: 16,
          borderBottomLeftRadius: 16,
          shadowColor: "#171a1f",
          shadowOffset: { width: 0, height: 0 },
          shadowOpacity: 0.12,
          shadowRadius: 2,
        }}
      >
        <View
          style={{
            justifyContent: "center",
            alignContent: "center",
            margin: "auto",
          }}
        >
          <Text
            style={{
              top: 10,
              left: 2,
              fontFamily: "Outfit",
              fontSize: 24,
              lineHeight: 32,
              fontWeight: "700",
              color: "#19191FFF",
            }}
          >
            Willkommen zu Gassavy
          </Text>
          <Text
            style={{
              marginTop: 15,
              fontFamily: "Inter" /* Body */,
              fontSize: 14,
              left: 2,
              lineHeight: 20,
              fontWeight: "400",
              color: "#19191FFF",
            }}
          >
            Your trusted partner for predicting future gas prices. Select your
            station and fuel type below.
          </Text>
        </View>
      </View>
      {/* View for fuel station selection */}
      <View
        style={{
          top: -32,
          width: "90%",
          margin: "auto",
          height: 338,
          backgroundColor: "#FFFFFF",
          borderRadius: 10,
          shadowColor: "#171a1f",
          shadowOffset: { width: 0, height: 0 },
          shadowOpacity: 0.12,
          shadowRadius: 2,
          elevation: 2,
        }}
      >
        <View
          style={{
            position: "absolute",
            top: 31,
            left: 24,
            flex: 1,
            flexDirection: "row",
            gap: 10,
          }}
        >
          {location_icon}
          <Text style={{ fontFamily: "Outfit", fontSize: 18, fontWeight: 600 }}>
            Wählen sie eine Tankstelle aus
          </Text>
        </View>
        <View style={{ margin: 24, marginTop: 70 }}>
         
        </View>
      </View>

      {/* view for fuel type selection */}
      <View
        style={{
          top: -45,
          width: "90%",
          margin: "auto",
          height: 142,
          backgroundColor: "#FFFFFF",
          borderRadius: 10,
          shadowColor: "#171a1f",
          shadowOffset: { width: 0, height: 0 },
          shadowOpacity: 0.12,
          shadowRadius: 2,
          elevation: 2,
        }}
      >
        <View
          style={{
            position: "absolute",
            top: 31,
            left: 24,
            flex: 1,
            flexDirection: "row",
            gap: 10,
          }}
        >
          {fuel_pump_icon}
          <Text style={{ fontFamily: "Outfit", fontSize: 18, fontWeight: 600 }}>
            Wählen sie eine Tankstelle aus
          </Text>
        </View>
      </View>

      {/* button for prediction */}
      <TouchableOpacity
        style={{
          top: -33,
          margin: "auto",
          width: "90%",
          height: 48,
          padding: 12,
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#C24100",
          borderRadius: 6,
          shadowColor: "#171a1f",
          shadowOffset: {
            width: 0,
            height: 0,
          },
          shadowOpacity: 0.12,
          shadowRadius: 2,
          elevation: 2,
        }}
        disabled={false} // Handle disabled state
      >
        <Text
          style={{
            fontFamily: "Inter",
            fontSize: 16,
            lineHeight: 26,
            fontWeight: "600",
            color: "#FFFFFF",
          }}
        >
          Predict Price
        </Text>
      </TouchableOpacity>
    </View>
  );
}
