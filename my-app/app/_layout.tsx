import { location_icon, menu_icon } from "@/assets/svgs";
import { Stack } from "expo-router";
import { Text, TouchableOpacity } from 'react-native';
import { SheetProvider } from "react-native-actions-sheet";
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function RootLayout() {
  return (
  <GestureHandlerRootView style={{ flex: 1 }}>
      <SheetProvider>
        <Stack
          screenOptions={{
        headerShown: true,
        headerStyle: { backgroundColor: '#9ACBD0' },
        headerTintColor: '#fff',
        headerTitle: 'Fuel Price',
        headerTitleAlign: 'center',
        headerTitleStyle: { fontWeight: '600' },
        headerRight: () => (
          <TouchableOpacity onPress={() => { /* open modal / navigate */ }} style={{ marginRight: 12, flexDirection: 'row', alignItems: 'center' }}>
            {location_icon}
            <Text style={{ color: '#000' }}>Stadt</Text>
          </TouchableOpacity>
        ),
        headerLeft: () => (
          <TouchableOpacity onPress={() => { /* open menu / navigate */ }} style={{ marginLeft: 12 }}>
            {menu_icon}
          </TouchableOpacity>
        ),
          }}
        />
        {/* Sheets global hier mounten */}
      </SheetProvider>
    </GestureHandlerRootView>
  );
}
