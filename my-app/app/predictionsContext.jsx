import { createContext, useContext, useState } from "react";

const PredictionsContext = createContext();

export function PredictionsProvider({ children }) {
  const [predictions, setPredictions] = useState(null);

  return (
    <PredictionsContext.Provider value={{ predictions, setPredictions }}>
      {children}
    </PredictionsContext.Provider>
  );
}

export function usePredictions() {
  return useContext(PredictionsContext);
}
