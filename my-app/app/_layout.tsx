import { Tabs } from "expo-router";
import { SheetProvider } from "react-native-actions-sheet";
import { GestureHandlerRootView } from "react-native-gesture-handler";

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SheetProvider>
        <Tabs
          screenOptions={{
            headerShown: true,
            headerTitle: "GasSavy",
            headerStyle: {
              backgroundColor: "#FFFFFF",
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
            }}
          />
          <Tabs.Screen
            name="settings"
            options={{
              title: "Settings",
            }}
          />
        </Tabs>
      </SheetProvider>
    </GestureHandlerRootView>
  );
}
