import { useEffect, useMemo, useState } from "react";
import { Dimensions, FlatList, Pressable, Text, View } from "react-native";
import { ScrollView } from "react-native-actions-sheet";
import { LineChart } from "react-native-chart-kit";
import { Button, Searchbar } from "react-native-paper";
import cities from "../resources/cities.json";

const screenWidth = Dimensions.get("window").width;
const screenHeight = Dimensions.get("window").height;

type Station = {
    id: string;
    brand?: string | null;
    street?: string | null;
    house_number?: string | null;
    status?: string | null;
    e5?: number | null;
    e10?: number | null;
    diesel?: number | null;
  };

export default function Index() {
  const [city, setCity] = useState("");
  const [stationsInCity, setStationsInCity] = useState<Station[]>([]);
  const [query, setQuery] = useState("");
  const [fuelType, setFuelType] = useState("Super E5");
  const [showCityResults, setShowCityResults] = useState(false);
  const [bestPrice, setBestPrice] = useState<number | null>(null);
  const [worstPrice, setWorstPrice] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = "https://fuel-flash.onrender.com";


  const chartData = {
    labels: ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00", "00:00"],
    datasets: [
      {
        data: [1.58, 1.62, 1.6, 1.54, 1.53, 1.59, 1.61],
        strokeWidth: 3,
      },
    ],
  };

  async function getStationInfo(city: string) {
  setLoading(true);
  try {
    const response = await fetch(`${API_BASE_URL}/stations/${city}`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    console.log("raw data:", data);

    if (!Array.isArray(data)) {
      throw new Error("API response is not an array");
    }

    const stationData: Station[] = data.map((station: any) => ({
      id: station.id,
      brand: station.brand,
      e5: station.e5,
      e10: station.e10,
      diesel: station.diesel,
      status: station.status,
      street: station.street,
      house_number: station.house_number,
    }));

    console.log("mapped stationData:", stationData);
    setStationsInCity(stationData);
  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
}

function getBestWorstPrice(stations: Station[], fuelType: string) {
  const fuelKey: "e5" | "e10" | "diesel" =
    fuelType === "Super E5"
      ? "e5"
      : fuelType === "Super E10"
      ? "e10"
      : "diesel";
  const prices = stations
    .map((station) => station[fuelKey])
    .filter((price): price is number => price != null);
  if (prices.length === 0) return null;
  setBestPrice(Math.min(...prices));
  setWorstPrice(Math.max(...prices));
}


// get the best/ worst price from stationsInCity when stationsInCity or fuelType changes
useEffect(() => {
  getBestWorstPrice(stationsInCity, fuelType);
}, [stationsInCity, fuelType]);


  // get stations in city when city changes
  useEffect(() => {
    async function fetchStations() {
      getStationInfo(city);
    }
    if (city) {
      fetchStations();
    }
  }, [city]);

  const cityResults = useMemo(() => {
    const trimmed = query.trim().toLowerCase();

    if (!trimmed) return [];

    return cities
      .filter((item) => {
        const cityMatch = item.city.toLowerCase().startsWith(trimmed);
        const plzMatch = item.plz.some((code) => code.startsWith(trimmed));

        return cityMatch || plzMatch;
      })
      .slice(0, 8);
  }, [query]);


  const renderItem = ({ item, index }: { item: Station; index: number }) => {
    const fuelKey: "e5" | "e10" | "diesel" =
      fuelType === "Super E5"
        ? "e5"
        : fuelType === "Super E10"
        ? "e10"
        : "diesel";
    const fuelPrice = item[fuelKey];
    const fuelPriceText =
      fuelPrice != null ? fuelPrice.toFixed(2).replace(".", ",") : "--,--";

    return (
      <View
        style={{
          backgroundColor: "#18181B",
          borderRadius: 16,
          borderWidth: 2,
          borderLeftWidth: 5,
          borderColor: fuelPrice === bestPrice ? "#2ECC71" : fuelPrice === worstPrice ? "#E74C3C" : "#27272A",
          paddingHorizontal: 16,
          paddingVertical: 14,
          marginBottom: 10,
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {/* Linke Seite */}
        <View style={{ flex: 1, paddingRight: 12 }}>
          <Text
            style={{
              color: "#FFFFFF",
              fontSize: 17,
              fontWeight: "700",
              marginBottom: 6,
            }}
          >
            {item.brand ?? "Unbekannt"}
          </Text>

          <View
            style={{
              flexDirection: "row",
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <Text
              style={{
                color: "#71717A",
                fontSize: 13,
              }}
            >
              {item.street} {item.house_number}
            </Text>

            <Text
              style={{
                color: "#71717A",
                fontSize: 13,
                marginHorizontal: 6,
              }}
            >
              •
            </Text>

            <Text
              style={{
                color: item.status === "open"  ? "#2ECC71" : "#E74C3C",
                fontSize: 13,
                fontWeight: "600",
              }}
            >
              {item.status === "open"  ? "Geöffnet" : "Geschlossen"}
            </Text>
          </View>
        </View>

        {/* Rechte Seite */}
        <View style={{ alignItems: "flex-end" }}>
          <Text
            style={{
              color: "#FFFFFF",
              fontSize: 30,
              fontWeight: "800",
              lineHeight: 30,
            }}
          >
            {fuelPriceText}
            <Text
              style={{
                fontSize: 14,
                fontWeight: "700",
                color: "#FFFFFF",
                lineHeight: 14,
              }}
            >€/L
            </Text>
          </Text>

        </View>
      </View>
    );
  };

  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "#121212",
        paddingHorizontal: 16,
        paddingTop: 8,
        paddingBottom: 8,
      }}
    >
      {city === "" || loading ? (
        <View
          style={{
            position: "relative",
            zIndex: 50,
          }}
        >
          <Searchbar
            placeholder="Ort oder Postleitzahl eingeben"
            placeholderTextColor={"#6B7280"}
            value={query}
            style={{
              backgroundColor: "#1E1E1E",
              borderColor: "#2D2D2D",
              borderRadius: 12,
              width: "100%",
              height: 48,
              justifyContent: "center",
            }}
            inputStyle={{
              fontSize: 16,
              color: "#FFFFFF",
              height: 48,
              textAlignVertical: "center",
              paddingBottom: 6,
            }}
            iconColor="#9CA3AF"
            onFocus={() => setShowCityResults(true)}
            onBlur={() => {
              setTimeout(() => setShowCityResults(false), 150);
            }}
            onChangeText={(text) => {
              setQuery(text);
              setShowCityResults(true);
            }}
          />

          {showCityResults && cityResults.length > 0 && (
            <View
              style={{
                position: "absolute",
                top: 54,
                left: 0,
                right: 0,
                zIndex: 100,
                backgroundColor: "#1E1E1E",
                borderRadius: 12,
                borderWidth: 1,
                borderColor: "#2D2D2D",
                overflow: "hidden",
                elevation: 8,
                shadowColor: "#000",
                shadowOpacity: 0.25,
                shadowRadius: 8,
                shadowOffset: { width: 0, height: 4 },
              }}
            >
              {cityResults.map((item, index) => (
                <Pressable
                  key={`${item.city}-${index}`}
                  onPress={() => {
                    setQuery(item.city);
                    setCity(item.city);
                    setShowCityResults(false);
                  }}
                  style={{
                    paddingHorizontal: 14,
                    paddingVertical: 14,
                    borderBottomWidth: index === cityResults.length - 1 ? 0 : 1,
                    borderBottomColor: "#2D2D2D",
                  }}
                >
                  <Text style={{ color: "#FFFFFF", fontSize: 15 }}>
                    {item.city}
                  </Text>
                </Pressable>
              ))}
            </View>
          )}

          <Text
            style={{
              color: "#FFFFFF",
              fontSize: 20,
              textAlign: "center",
              marginTop: screenHeight * 0.3,
            }}
          >
            {loading ? (
              <Text>Loading...</Text>
            ) : (
              "Bitte wählen Sie einen Ort aus"
            )}
          </Text>
        </View>
      ) : (
        <ScrollView showsVerticalScrollIndicator={false}>
          <View
            style={{
              position: "relative",
              zIndex: 50,
            }}
          >
            <Searchbar
              placeholder="Ort oder Postleitzahl eingeben"
              placeholderTextColor={"#6B7280"}
              value={query}
              style={{
                backgroundColor: "#1E1E1E",
                borderColor: "#2D2D2D",
                borderRadius: 12,
                width: "100%",
                height: 48,
                justifyContent: "center",
              }}
              inputStyle={{
                fontSize: 16,
                color: "#FFFFFF",
                height: 48,
                textAlignVertical: "center",
                paddingBottom: 6,
              }}
              iconColor="#9CA3AF"
              onFocus={() => setShowCityResults(true)}
              onBlur={() => {
                setTimeout(() => setShowCityResults(false), 150);
              }}
              onChangeText={(text) => {
                setQuery(text);
                setShowCityResults(true);
              }}
            />

            {showCityResults && cityResults.length > 0 && (
              <View
                style={{
                  position: "absolute",
                  top: 54,
                  left: 0,
                  right: 0,
                  backgroundColor: "#1E1E1E",
                  borderRadius: 12,
                  borderWidth: 1,
                  borderColor: "#2D2D2D",
                  overflow: "hidden",
                  elevation: 8,
                  shadowColor: "#000",
                  shadowOpacity: 0.25,
                  shadowRadius: 8,
                  shadowOffset: { width: 0, height: 4 },
                }}
              >
                {cityResults.map((item, index) => (
                  <Pressable
                    key={item.city + "-" + index}
                    onPress={() => {
                      setQuery(item.city);
                      setCity(item.city);
                      setShowCityResults(false);
                    }}
                    style={{
                      paddingHorizontal: 14,
                      paddingVertical: 14,
                      borderBottomWidth:
                        index === cityResults.length - 1 ? 0 : 1,
                      borderBottomColor: "#2D2D2D",
                    }}
                  >
                    <Text style={{ color: "#FFFFFF", fontSize: 15 }}>
                      {item.city}
                    </Text>
                  </Pressable>
                ))}
              </View>
            )}
          </View>
          <View
            style={{
              flexDirection: "row",
              paddingVertical: 16,
              gap: 8,
              marginBottom: 8,
            }}
          >
            <Button
              style={{
                backgroundColor:
                  fuelType === "Super E5" ? "#FF6B35" : "#1E1E1E",
                borderRadius: 16,
              }}
              contentStyle={{
                paddingHorizontal: 4,
                paddingVertical: 6,
              }}
              labelStyle={{
                fontSize: 14,
                marginVertical: 0,
              }}
              textColor={fuelType === "Super E5" ? "#FFFFFF" : "#6B7280"}
              onPress={() => setFuelType("Super E5")}
            >
              Super E5
            </Button>

            <Button
              style={{
                backgroundColor:
                  fuelType === "Super E10" ? "#FF6B35" : "#1E1E1E",
                borderRadius: 16,
              }}
              contentStyle={{
                paddingHorizontal: 4,
                paddingVertical: 6,
              }}
              labelStyle={{
                fontSize: 14,
                marginVertical: 0,
              }}
              textColor={fuelType === "Super E10" ? "#FFFFFF" : "#6B7280"}
              onPress={() => setFuelType("Super E10")}
            >
              Super E10
            </Button>

            <Button
              style={{
                backgroundColor: fuelType === "Diesel" ? "#FF6B35" : "#1E1E1E",
                borderRadius: 16,
              }}
              contentStyle={{
                paddingHorizontal: 4,
                paddingVertical: 6,
              }}
              labelStyle={{
                fontSize: 14,
                marginVertical: 0,
              }}
              textColor={fuelType === "Diesel" ? "#FFFFFF" : "#6B7280"}
              onPress={() => setFuelType("Diesel")}
            >
              Diesel
            </Button>
          </View>

          <View
            style={{
              flexDirection: "row",
              gap: 12,
              marginBottom: 20,
            }}
          >
            <View
              style={{
                flex: 1,
                backgroundColor: "#1E1E1E",
                borderRadius: 18,
                paddingHorizontal: 16,
                paddingVertical: 14,
                borderWidth: 1,
                borderColor: "#2D2D2D",
              }}
            >
              <Text
                style={{
                  color: "#9CA3AF",
                  fontSize: 14,
                  marginBottom: 6,
                }}
              >
                Günstigster in
              </Text>
              <Text
                style={{
                  color: "#9CA3AF",
                  fontSize: 14,
                  marginBottom: 6,
                }}
              >
                {city}
              </Text>

              <Text
                style={{
                  color: "#2ECC71",
                  fontSize: 24,
                  fontWeight: "700",
                }}
              >
                {bestPrice != null ? bestPrice.toFixed(2).replace(".", ",") : "--,--"}
                <Text style={{ fontSize: 16, fontWeight: "600" }}>€/L</Text>
              </Text>
            </View>

            <View
              style={{
                flex: 1,
                backgroundColor: "#1E1E1E",
                borderRadius: 18,
                paddingHorizontal: 16,
                paddingVertical: 14,
                borderWidth: 1,
                borderColor: "#2D2D2D",
                alignItems: "center",
              }}
            >
              <Text
                style={{
                  color: "#9CA3AF",
                  fontSize: 14,
                  marginBottom: 6,
                }}
              >
                Günstigste Uhrzeit
              </Text>

              <Text
                style={{
                  color: "#FFFFFF",
                  fontSize: 30,
                  fontWeight: "700",
                }}
              >
                18
              </Text>
              <Text
                style={{
                  color: "#FFFFFF",
                  fontSize: 18,
                  fontWeight: "700",
                }}
              >
                Uhr
              </Text>
            </View>
          </View>

          <View
            style={{
              marginBottom: 20,
              backgroundColor: "#1E1E1E",
              borderRadius: 16,
              paddingVertical: 16,
              paddingLeft: 8,
              overflow: "hidden",
            }}
          >
            <Text
              style={{
                color: "#FFFFFF",
                fontSize: 18,
                fontWeight: "600",
                marginBottom: 12,
                paddingHorizontal: 12,
              }}
            >
              Preisprognose ({fuelType})
            </Text>

            <LineChart
              data={chartData}
              width={screenWidth - 40}
              height={220}
              withDots={true}
              withInnerLines={true}
              withOuterLines={false}
              withShadow={true}
              withVerticalLines={false}
              yAxisSuffix="€"
              fromZero={false}
              bezier
              chartConfig={{
                backgroundColor: "#1E1E1E",
                backgroundGradientFrom: "#1E1E1E",
                backgroundGradientTo: "#1E1E1E",
                decimalPlaces: 2,
                color: (opacity = 1) => `rgba(255, 107, 53, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(156, 163, 175, ${opacity})`,
                propsForDots: {
                  r: "4",
                  strokeWidth: "2",
                  stroke: "#FF6B35",
                  fill: "#121212",
                },
                propsForBackgroundLines: {
                  stroke: "#2D2D2D",
                  strokeDasharray: "",
                },
                fillShadowGradient: "#FF6B35",
                fillShadowGradientOpacity: 0.18,
              }}
              style={{
                borderRadius: 16,
              }}
            />
          </View>

          <Text
            style={{
              color: "#FFFFFF",
              fontSize: 18,
              fontWeight: "600",
              marginBottom: 8,
            }}
          >
            Tankstellen in der Nähe
          </Text>

          <View style={{}}>
            <FlatList
              data={stationsInCity}
              renderItem={renderItem}
              keyExtractor={(item) => item.id}
              showsVerticalScrollIndicator={false}
              keyboardShouldPersistTaps="handled"
              contentContainerStyle={{ paddingBottom: 24 }}
              initialNumToRender={15}
              maxToRenderPerBatch={20}
              windowSize={7}
            />
          </View>
        </ScrollView>
      )}
    </View>
  );
}
