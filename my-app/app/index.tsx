import { useState } from "react";
import { Pressable, Text, View } from "react-native";
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

  return (
    <View
      style={{
        flex: 1,
        marginTop: 75,
        alignItems: "center",
        alignSelf: "center",
        width: "90%",
      }}
    >
      <Text style={{ marginBottom: 20, fontSize: 18, fontWeight: "bold" }}>
        Wählen Sie eine Tankstelle, einen Kraftstofftyp und einen Zeitrahmen für die Vorhersage aus:
      </Text>
      {/* container for dropdowns */}
      <View
        style={{
          width: "80%",
          flexDirection: "row",
          justifyContent: "center",
          alignItems: "center",
          gap: 50,
        }}
      >
        <Pressable
          style={{
            width: 70,
            height: 30,
            backgroundColor: "#ddd",
            borderRadius: 5,
            alignItems: "center",
            justifyContent: "center",
          }}
          onPress={() => openDropdown("station_picker")}
        >
          <Text>{selected_station}</Text>
        </Pressable>
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

        <Pressable
          style={{
            width: 70,
            height: 30,
            backgroundColor: "#ddd",
            borderRadius: 5,
            alignItems: "center",
            justifyContent: "center",
          }}
          onPress={() => openDropdown("fuel_picker")}
        >
          <Text>{selected_fuel}</Text>
        </Pressable>
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
        <Pressable
          style={{
            width: 90,
            height: 30,
            backgroundColor: "#ddd",
            borderRadius: 5,
            alignItems: "center",
            justifyContent: "center",
          }}
          onPress={() => openDropdown("timeframe_picker")}
        >
          <Text>{time_frame}</Text>
        </Pressable>
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
        <Pressable
          style={{
            padding: 10,
            backgroundColor: "#ddd",
            borderRadius: 5,
          }}
          onPress={() => {
            fetch("http://localhost:8000/predict")
              .then((res) => res.json())
              .then((data) => console.log(data.prediction))
              .catch(console.error);
          }}
        >
          <Text>Predict</Text>
        </Pressable>
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
