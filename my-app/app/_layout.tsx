import { Tabs } from "expo-router";
import { SheetProvider } from "react-native-actions-sheet";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { Provider as PaperProvider, Portal } from "react-native-paper";
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
                  headerTitle: "Fuel Flash",
                  headerStyle: {
                    backgroundColor: "#1E1E1E",
                    height: 57,
                  },
                  headerTitleStyle: {
                    fontFamily: "Outfit",
                    fontSize: 18,
                    fontWeight: "600",
                    color: "#FFFFFF",
                  },
                  tabBarStyle: {
                    backgroundColor: "#FFFFFF",
                    height: 0,
                  },
                  tabBarActiveTintColor: "#C24100FF",
                  tabBarInactiveTintColor: "#888888",
                }}
              >
                {/* <Tabs.Screen
                  name="index_outdated"
                  options={{
                    title: "Home",
                  }}
                />
                <Tabs.Screen
                  name="predictions"
                  options={{
                    title: "predictions",
                  }}
                /> */}
              </Tabs>
            </PredictionsProvider>
          </SheetProvider>
        </Portal.Host>
      </PaperProvider>
    </GestureHandlerRootView>
  );
}
