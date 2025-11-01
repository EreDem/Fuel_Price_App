import { Tabs } from "expo-router";
import { SheetProvider } from "react-native-actions-sheet";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { Provider as PaperProvider, Portal } from "react-native-paper";
import { HomeIcon, PredictGraphIcon } from "../assets/svgs";
import { PredictionsProvider } from "./predictionsContext";

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <PaperProvider>
        <Portal.Host>
          <SheetProvider>
            <PredictionsProvider>
              <Tabs
                screenOptions={{
                  headerShown: true,
                  headerTitle: "GasSavy",
                  headerStyle: {
                    backgroundColor: "#FFFFFF",
                    height: 57,
                  },
                  headerTitleStyle: {
                    fontFamily: "Outfit",
                    fontSize: 18,
                    fontWeight: "600",
                    color: "#171A1FFF",
                  },
                  tabBarStyle: {
                    backgroundColor: "#FFFFFF",
                    height: 64,
                  },
                  tabBarActiveTintColor: "#C24100FF",
                  tabBarInactiveTintColor: "#888888",
                }}
              >
                <Tabs.Screen
                  name="home"
                  options={{
                    title: "Home",
                    tabBarIcon: ({ color }) => <>{HomeIcon(color)}</>,
                  }}
                />
                <Tabs.Screen
                  name="predictions"
                  options={{
                    title: "predictions",
                    tabBarIcon: ({ color }) => <>{PredictGraphIcon(color)}</>,
                  }}
                />
              </Tabs>
            </PredictionsProvider>
          </SheetProvider>
        </Portal.Host>
      </PaperProvider>
    </GestureHandlerRootView>
  );
}
