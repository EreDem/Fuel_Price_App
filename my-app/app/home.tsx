import React, { useEffect, useState } from "react";
import { ScrollView, Text, TouchableOpacity, View } from "react-native";
import { FlatList } from "react-native-actions-sheet";
import { List, Menu, Searchbar } from "react-native-paper";
import { DropdownIcon, FuelPumpIcon, LocationIcon } from "../assets/svgs";
import { usePredictions } from "./predictionsContext";

export default function Home() {
  // Types
  type Station = {
    id: string;
    brand?: string | null;
    street?: string | null;
    house_number?: string | null;
    zip?: string | null;
    city?: string | null;
  };

  // Variables
  const fuel_stations = ["Aral", "Shell", "Jet", "PM", "BFT", "Total"];
  const fuel_types = ["Diesel", "E5", "E10"];
  const time_frames = ["24 Stunden", "48 Stunden", "72 Stunden"];

  const [selected_station, setSelectedStation] = useState("");
  const [selected_fuel, setSelectedFuel] = useState("E5");
  const [time_frame, setTimeFrame] = useState("48 Stunden");

  const [visible, setVisible] = useState(false);
  const [city, setCity] = useState("");

  const [visibleStations, setVisibleStations] = useState<Station[]>([]);
  const [allStations, setAllStations] = useState<Station[]>([]);

  const { setPredictions } = usePredictions();

  // debounce for city input
  const [query, setQuery] = useState(city);

  useEffect(() => {
    const t = setTimeout(() => setCity(query), 250);
    return () => clearTimeout(t);
  }, [query]);

  // load stations on mount
  useEffect(() => {
    import("../stations.json").then((mod) => {
      setVisibleStations(mod.default);
      setAllStations(mod.default);
    });
  }, []);

  // enable searching
  useEffect(() => {
    if (!city) {
      setVisibleStations(allStations);
      return;
    }
    const q = city.toLowerCase();

    const filtered = allStations.filter(
      (s) =>
        s.city?.toLowerCase().includes(q) || s.zip?.toLowerCase().includes(q)
    );

    setVisibleStations(filtered);
  }, [allStations, city]);

  const renderItem = ({ item }: { item: Station }) => (
    <List.Item
      title={`${item.brand ?? "Unbekannt"} – ${item.city ?? ""}`}
      description={`${item.street ?? ""} ${item.house_number ?? ""}, ${
        item.zip ?? ""
      }`}
      titleStyle={{
        fontWeight: "600",
        color: selected_station === item.id ? "#C24100FF" : "#171A1FFF",
      }}
      descriptionStyle={{ color: "#555" }}
      style={
        {
          // backgroundColor: selected_station === item.id ? "red" : "black"
        }
      }
      onPress={() => {
        // eslint-disable-next-line no-unused-expressions
        selected_station === item.id ? console.log("ja") : console.log("nein");
        setSelectedStation(item.id);
        console.log(item.id);
      }}
    />
  );

  return (
    // main view
    <ScrollView
      style={{
        height: "100%",
        backgroundColor: "#FFFFFF",
      }}
    >
      <View
        style={{
          width: "100%",
          height: 736,
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
              Willkommen zu GasSavy
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
              Ihr Partner zum Geld sparen.
            </Text>
          </View>
        </View>
        {/* View for fuel station selection */}
        <View
          style={{
            top: -22,
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
            <LocationIcon></LocationIcon>
            <Text
              style={{ fontFamily: "Outfit", fontSize: 18, fontWeight: 600 }}
            >
              Wählen sie eine Tankstelle aus
            </Text>
          </View>
          <View
            style={{
              paddingHorizontal: 24,
              marginTop: 70,
            }}
          >
            <View
              style={{
                backgroundColor: "#DEE1E6FF",
                borderRadius: 6,
                width: "100%",
                height: 48,
                justifyContent: "center",
              }}
            >
              <Searchbar
                placeholder=""
                value={query}
                style={{
                  backgroundColor: "#DEE1E6FF",
                  borderRadius: 6,
                  width: "100%",
                  height: 48,
                  justifyContent: "center",
                }}
                inputStyle={{
                  fontSize: 16,
                  color: "#565D6DFF",
                  height: 48,
                  textAlignVertical: "center",
                  paddingVertical: 0,
                }}
                iconColor="#565D6DFF"
                onChangeText={(text) => {
                  setQuery(text);
                }}
              />
            </View>
            <View
              style={{
                width: "100%",
                height: 180,
                marginTop: 15,
                backgroundColor: "#F3F4F6FF",
                borderRadius: 6,
              }}
            >
              <FlatList
                data={visibleStations}
                renderItem={renderItem}
                keyExtractor={(item) => item.id}
                scrollEnabled={true}
                contentContainerStyle={{ paddingVertical: 4 }}
                showsVerticalScrollIndicator={false}
                initialNumToRender={15}
                maxToRenderPerBatch={20}
                windowSize={7}
              />
            </View>
          </View>
        </View>

        {/* view for fuel type selection */}
        <View
          style={{
            top: -25,
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
            zIndex: 10,
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
            <FuelPumpIcon />
            <Text
              style={{ fontFamily: "Outfit", fontSize: 18, fontWeight: 600 }}
            >
              Wählen sie eine Kraftstoffart aus
            </Text>
          </View>
          <View
            style={{
              margin: "auto",
              top: 20,
              width: "90%",
              height: 48,
              backgroundColor: "#DEE1E6FF",
              borderRadius: 6,
            }}
          >
            <Menu
              visible={visible}
              onDismiss={() => setVisible(false)}
              anchor={
                <View
                  style={{
                    height: 48,
                    zIndex: 10,
                    width: "100%",
                    flexDirection: "row",
                    alignItems: "center",
                  }}
                >
                  <TouchableOpacity
                    onPress={() => {
                      setVisible((prev) => !prev);
                    }}
                    activeOpacity={0.7}
                    style={{
                      flex: 1,
                      height: 48,
                      zIndex: 100,
                      flexDirection: "row",
                      justifyContent: "space-between",
                      alignItems: "center",
                      backgroundColor: "#DEE1E6FF",
                      borderRadius: 6,
                      width: "80%",
                      paddingHorizontal: 12,
                    }}
                  >
                    <Text
                      style={{
                        color: "#171A1FFF",
                        textAlign: "left",
                        fontSize: 16,
                        flexShrink: 1,
                      }}
                      numberOfLines={1}
                    >
                      {selected_fuel}
                    </Text>

                    <DropdownIcon />
                  </TouchableOpacity>
                </View>
              }
              contentStyle={{
                backgroundColor: "#F3F4F6FF",
                borderRadius: 6,
                width: "100%",
              }}
              style={{
                zIndex: 100,
                width: "80%",
                marginHorizontal: "auto",
                marginTop: 55,
              }}
            >
              <Menu.Item
                title="Diesel"
                onPress={() => {
                  setSelectedFuel("Diesel");
                  setVisible(false);
                }}
                titleStyle={{ color: "#111" }}
                style={{ paddingVertical: 8 }}
              />
              <Menu.Item
                title="E5"
                onPress={() => {
                  setSelectedFuel("E5");
                  setVisible(false);
                }}
                titleStyle={{ color: "#111" }}
                style={{ paddingVertical: 8 }}
              />
              <Menu.Item
                title="E10"
                onPress={() => {
                  setSelectedFuel("E10");
                  setVisible(false);
                }}
                titleStyle={{ color: "#111" }}
                style={{ paddingVertical: 8 }}
              />
            </Menu>
          </View>
        </View>

        {/* button for prediction */}
        <TouchableOpacity
          style={{
            bottom: 5,
            zIndex: 0,
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
          onPress={() => {
            const getPrediction = async () => {
              try {
                const resp = await fetch(
                  `http://127.0.0.1:8000/predict?fuel_type=${selected_fuel}&station_uuid=${selected_station}`
                );
                
                if (!resp.ok) throw new Error(`Request failed: ${resp.status}`);

                const result = await resp.json();
                console.log("Prediction result:", result);
                setPredictions(result.predictions);
              } catch (error) {
                console.error("Prediction error:", error);
              }
            };
            getPrediction()
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
    </ScrollView>
  );
}
