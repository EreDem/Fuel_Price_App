import { clock_icon, dropdown_icon, fuel_icon, fuel_pump_icon, predict_graph_icon } from "@/assets/svgs";
import { useState } from "react";
import { Pressable, Text, TouchableOpacity, View } from "react-native";
import ActionSheet, {
  FlatList,
  SheetManager,
} from "react-native-actions-sheet";

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
    <View
      style={{
        flex: 1,
        marginTop: 75,
        alignItems: "center",
        alignSelf: "center",
        width: "100%",
        backgroundColor: "#EFEFEF"
      }}
    >
      <Text style={{ marginBottom: 20, fontSize: 18, fontWeight: "bold", textAlign: "center" }}>
        Wählen sie Tankstelle, Kraftstoff und Zeitrahmen aus
      </Text>
      {/* container for dropdowns */}
      <View
        style={{
          width: "80%",
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <TouchableOpacity
          style={{
            ...button_style,
            width: 90,
          }}
          onPress={() => openDropdown("station_picker")}
        >
          {fuel_pump_icon}
          <Text style={{ fontSize: 16}}>{selected_station}</Text>
          {dropdown_icon}
        </TouchableOpacity>
        <ActionSheet
          id="station_picker"
          containerStyle={{
            maxHeight: 360,
            width: 320, // make the sheet narrower
            alignSelf: "center",
            borderTopLeftRadius: 12,
            borderTopRightRadius: 12,
            overflow: "hidden",
          }}
        >
          <FlatList
            data={fuel_stations.map((station, index) => ({
              id: index.toString(),
              title: station,
            }))}
            keyExtractor={(item) => item.id}
            style={{ maxHeight: 320, backgroundColor: "white", width: "100%" }}
            renderItem={({ item }) => (
              <Pressable
                onPress={() => {
                  SheetManager.hide("station_picker");
                  setSelectedStation(item.title);
                }}
                style={{
                  padding: 16,
                  borderBottomWidth: 1,
                  borderBottomColor: "#eee",
                  backgroundColor: "white",
                }}
              >
                <Text>{item.title}</Text>
              </Pressable>
            )}
          />
        </ActionSheet>

        <TouchableOpacity
          style={{
            ...button_style,
            width: 90,
          }}
          onPress={() => openDropdown("fuel_picker")}
        >
          {fuel_icon}
          <Text style={{ fontSize: 16 }}>{selected_fuel}</Text>
          {dropdown_icon}
        </TouchableOpacity>
        <ActionSheet
          id="fuel_picker"
          containerStyle={{
            maxHeight: 360,
            width: 320, // make the sheet narrower
            alignSelf: "center",
            borderTopLeftRadius: 12,
            borderTopRightRadius: 12,
            overflow: "hidden",
          }}
        >
          <FlatList
            data={fuel_types.map((fuel, index) => ({
              id: index.toString(),
              title: fuel,
            }))}
            keyExtractor={(item) => item.id}
            style={{ maxHeight: 320, backgroundColor: "white", width: "100%" }}
            renderItem={({ item }) => (
              <Pressable
                onPress={() => {
                  SheetManager.hide("fuel_picker");
                  setSelectedFuel(item.title);
                }}
                style={{
                  padding: 16,
                  borderBottomWidth: 1,
                  borderBottomColor: "#eee",
                  backgroundColor: "white",
                }}
              >
                <Text>{item.title}</Text>
              </Pressable>
            )}
          />
        </ActionSheet>
        <TouchableOpacity
          style={{
            width: 140,
            ...button_style,
          }}
          onPress={() => openDropdown("timeframe_picker")}
        >
          {clock_icon}
          <Text style={{ fontSize: 16 }}>{time_frame}</Text>
          {dropdown_icon}
        </TouchableOpacity>
        <ActionSheet
          id="timeframe_picker"
          containerStyle={{
            maxHeight: 360,
            width: 320, // make the sheet narrower
            alignSelf: "center",
            borderTopLeftRadius: 12,
            borderTopRightRadius: 12,
            overflow: "hidden",
          }}
        >
          <FlatList
            data={time_frames.map((frame, index) => ({
              id: index.toString(),
              title: frame,
            }))}
            keyExtractor={(item) => item.id}
            style={{ maxHeight: 320, backgroundColor: "white", width: "100%" }}
            renderItem={({ item }) => (
              <Pressable
                onPress={() => {
                  SheetManager.hide("timeframe_picker");
                  setTimeFrame(item.title);
                }}
                style={{
                  padding: 16,
                  borderBottomWidth: 1,
                  borderBottomColor: "#eee",
                  backgroundColor: "white",
                }}
              >
                <Text>{item.title}</Text>
              </Pressable>
            )}
          />
        </ActionSheet>
      </View>
      <View style={{ marginTop: 20 }}>
        <TouchableOpacity
          style={{
            ...button_style,
            width: 100,
            paddingHorizontal: 10,
          }}
          onPress={() => {
            fetch("http://localhost:8000/predict?fuel_station=" + selected_station + "&fuel_type=" + selected_fuel + "&time_frame=" + time_frame)
              .then((res) => res.json())
              .then((data) => console.log(data))
              .catch(console.error);
          }}
        >
          <Text style={{ fontSize: 16 }}>Predict</Text>
          {predict_graph_icon}
        </TouchableOpacity>
      </View>
      <View
        style={{
          marginTop: 20,
          backgroundColor: "#ddd",
          width: 300,
          height: 300,
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Text>Prediction Graph</Text>
      </View>
      <Text style={{ marginTop: 20 }}>
        Beste Zeit zum Tanken in den nächsten {time_frame} ist:
      </Text>
      <Text style={{ fontSize: 24, fontWeight: "bold", marginTop: 10 }}>
        14:30 Uhr - 15:00 Uhr
      </Text>
    </View>
  );
}
