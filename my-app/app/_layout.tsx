import { Tabs } from "expo-router";
import { Image } from "react-native";
import { SheetProvider } from "react-native-actions-sheet";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { Provider as PaperProvider, Portal } from "react-native-paper";

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <PaperProvider>
        <Portal.Host>
          <SheetProvider>
              <Tabs
                screenOptions={{
                  headerShown: true,
                  headerTitle: "FUEL SMART",
                  headerLeft: () => (
                    <Image
                      source={require("../assets/icon.png")}
                      style={{ width: 40, height: 30, marginLeft: 10 }}
                    />
                  ),
                  headerStyle: {
                    backgroundColor: "#121212",
                    height: 57,
                  },
                  headerTitleStyle: {
                    fontFamily: "Arial",
                    fontSize: 24,
                    fontWeight: "600",
                    color: "#FF6B35",
                  },
                  tabBarStyle: {
                  height: 0,
                  }
                }}
              >
              </Tabs>
          </SheetProvider>
        </Portal.Host>
      </PaperProvider>
    </GestureHandlerRootView>
  );
}
