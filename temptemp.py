import yfinance as yf
import pandas as pd

def download_exchange_rates_simple():
    """ 
    Einfache Version - lädt nur EUR/USD Wechselkurs in CSV
    """ 
    try:
        print("Lade EUR/USD Wechselkurs...")
        
        # Wechselkurs downloaden
        eur_usd = yf.download("EURUSD=X", start="2023-12-01", progress=False)
        
        # Einfachen DataFrame erstellen
        exchange_df = eur_usd.reset_index()[['Date', 'Close']]
        exchange_df.columns = ['date', 'eur_usd_rate']
        
        # CSV speichern
        exchange_df.to_csv('exchange_rates.csv', index=False)
        
        print(f"✅ Wechselkurs-Daten gespeichert: {len(exchange_df)} Tage")
        print(f"📁 Datei: exchange_rates.csv")
        print(f"💰 Letzter Kurs: 1 EUR = {exchange_df['eur_usd_rate'].iloc[-1]:.4f} USD")
        
        return exchange_df

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None

# Ausführen
download_exchange_rates_simple()