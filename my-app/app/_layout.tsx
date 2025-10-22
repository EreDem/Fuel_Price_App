import { Stack } from "expo-router";
import { SheetProvider } from "react-native-actions-sheet";
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function RootLayout() {
  return (
  <GestureHandlerRootView style={{ flex: 1 }}>
      <SheetProvider>
        <Stack screenOptions={{ headerShown: true }} />
        {/* Sheets global hier mounten */}
      </SheetProvider>
    </GestureHandlerRootView>
  );
}
