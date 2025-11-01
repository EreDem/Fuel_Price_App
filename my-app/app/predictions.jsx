import { useState } from "react";
import { ScrollView, View } from "react-native";
import { Button, Text } from "react-native-paper";
import { VictoryAxis, VictoryChart, VictoryLine } from "victory-native";
import { usePredictions } from "./predictionsContext";

export default function Predictions() {
  const [selected_time_frame, setSelectedTimeFrame] = useState("48");

  const { predictions } = usePredictions();

  if (!predictions) {
    return <Text>Keine Vorhersagen verfügbar</Text>;
  }

  const predData =
    predictions?.predictions?.map((p) => ({ x: p.time, y: p.price })) ?? [];
  console.log(
    "predictions len:",
    predictions?.length,
    "first:",
    predictions?.[0]
  );

  const chartData = (Array.isArray(predictions) ? predictions : []).map(
    (item, i) => {
      // Fall 1: API gibt nur Preise
      if (typeof item === "number") {
        return {
          x: (i * 0.5) % 24, // alle 30 min, zyklisch 0–24
          y: item,
        };
      }

      // Fall 2: API gibt { time, price }
      return {
        x: typeof item.time === "number" ? item.time : Number(item.time),
        y: typeof item.price === "number" ? item.price : Number(item.price),
      };
    }
  );

  return (
    // main view
    <ScrollView>
      <View
        style={{
          width: "100%",
          height: 1350,
          backgroundColor: "#FFFFFF",
        }}
      >
        {/* time frame selector */}
        <View
          style={{
            width: "60%",
            height: 48,
            marginHorizontal: "auto",
            backgroundColor: "#F3F4F6FF",
            flexDirection: "row",
            borderRadius: 24,
            top: 32,
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <Button
            mode="contained"
            style={{
              height: 40,
              backgroundColor:
                selected_time_frame === "24" ? "#C24100" : "#F3F4F6FF",
              marginLeft: 5,
            }}
            labelStyle={{
              color: selected_time_frame === "24" ? "#FFFFFF" : "#565D6DFF",
            }}
            onPress={() => setSelectedTimeFrame("24")}
          >
            24h
          </Button>
          <Button
            mode="contained"
            style={{
              height: 40,
              backgroundColor:
                selected_time_frame === "48" ? "#C24100" : "#F3F4F6FF",
            }}
            labelStyle={{
              color: selected_time_frame === "48" ? "#FFFFFF" : "#565D6DFF",
            }}
            onPress={() => setSelectedTimeFrame("48")}
          >
            48h
          </Button>
          <Button
            mode="contained"
            style={{
              height: 40,
              backgroundColor:
                selected_time_frame === "72" ? "#C24100" : "#F3F4F6FF",
              marginRight: 5,
            }}
            labelStyle={{
              color: selected_time_frame === "72" ? "#FFFFFF" : "#565D6DFF",
            }}
            onPress={() => setSelectedTimeFrame("72")}
          >
            72h
          </Button>
        </View>

        {/* View with prediction graph */}
        <View
          style={{
            height: 441,
            width: "90%",
            top: 45,
            backgroundColor: "#FFFFFF",
            borderRadius: 16,
            marginHorizontal: "auto",
            shadowColor: "#171a1f",
            shadowOffset: { width: 0, height: 0 },
            shadowOpacity: 0.12,
            shadowRadius: 2,
            elevation: 2,
          }}
        >
          <View style={{ width: "85%", marginHorizontal: "auto", top: 25 }}>
            <Text
              style={{
                color: "#171A1FFF",
                fontSize: 18,
                fontWeight: 600,
              }}
            >
              Kursvorhersage ({selected_time_frame}h)
            </Text>
          </View>

          {/* prediction graph */}
          <View style={{ flex: 1, marginHorizontal: "auto", paddingTop: 40 }}>
            <VictoryChart
              domain={{ x: [0, 24], y: [1.0, 2.5] }}
              domainPadding={{ x: 20, y: 12 }}
            >
              <VictoryAxis
                label="Uhrzeit"
                tickValues={[0, 6, 12, 18, 24]}
                tickFormat={(t) => `${t}h`}
              />
              <VictoryAxis dependentAxis label="Preis (€)" />
              <VictoryLine
                data={chartData}
                style={{ data: { stroke: "#2563EB", strokeWidth: 2 } }}
              />
            </VictoryChart>
          </View>
        </View>
        {/* view for prediction */}
        <View
          style={{
            height: 380,
            backgroundColor: "#FFF5F0FF",
            top: 65,
            width: "90%",
            marginHorizontal: "auto",
            borderRadius: 16,
            shadowColor: "#171a1f",
            shadowOffset: { width: 0, height: 0 },
            shadowOpacity: 0.12,
            shadowRadius: 2,
            elevation: 2,
          }}
        >
          <Text
            style={{
              fontSize: 20,
              color: "#19191FFF",
              fontWeight: 600,
              top: 25,
              paddingLeft: 24,
            }}
          >
            Bestpreis:
          </Text>
          <View
            style={{
              flexDirection: "row",
            }}
          >
            <Text
              style={{
                fontSize: 72,
                color: "#19191FFF",
                fontWeight: 800,
                top: 25,
                paddingLeft: 50,
              }}
            >
              1.73$
            </Text>
            <Text
              style={{
                fontSize: 20,
                color: "#19191FFF",
                fontWeight: 500,
                top: 95,
              }}
            >
              /Liter
            </Text>
          </View>
          <Text style={{ marginHorizontal: "auto", top: 17, color: "#555" }}>
            (Zu 98% genau)
          </Text>
          <Text
            style={{
              fontSize: 20,
              fontWeight: 600,
              color: "#19191FFF",
              top: 40,
              paddingLeft: 24,
            }}
          >
            Zum Zeitpunkt:
          </Text>
          <View>
            <Text
              style={{
                fontSize: 50,
                color: "#C24100FF",
                fontWeight: 800,
                top: 35,
                paddingLeft: 50,
              }}
            >
              15:00 Uhr
            </Text>
            <Text
              style={{
                fontSize: 30,
                color: "#C24100FF",
                fontWeight: 800,
                top: 35,
                marginHorizontal: "auto",
              }}
            >
              Fr, 31.10
            </Text>
          </View>
        </View>
        {/* view for savings screen */}
        <View
          style={{
            height: 358,
            backgroundColor: "#F4EDE1FF",
            top: 85,
            width: "90%",
            marginHorizontal: "auto",
            borderRadius: 16,
            shadowColor: "#171a1f",
            shadowOffset: { width: 0, height: 0 },
            shadowOpacity: 0.12,
            shadowRadius: 2,
            elevation: 2,
          }}
        ></View>
      </View>
    </ScrollView>
  );
}
