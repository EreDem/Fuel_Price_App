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

  const [selected_station, setSelectedStation] = useState("Select Station");
  const [selected_fuel, setSelectedFuel] = useState("Select Fuel Type");

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        // backgroundColor: "black"
      }}
    >
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
        <Pressable onPress={() => openDropdown("station_picker")}>
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

        <Pressable onPress={() => openDropdown("fuel_picker")}>
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
          onPress={() => {
            fetch("http://localhost:8000/predict")
              .then((res) => res.json())
              .then((data) => console.log(data.prediction))
              .catch(console.error);
          }}
        >
          <Text>FETCH</Text>
        </Pressable>
      </View>
    </View>
  );
}
