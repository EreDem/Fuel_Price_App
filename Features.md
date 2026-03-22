# List of available raw data:

## date-type-data:

**- day_of_week**

**- is_weekend**

**- time**

**- month and larger time periods would only be useful if we had long term data, which we don't have**

## location-type-data:

**- latitude**

**- longitude**

**- size of the area (if available)**

**- highway or not (if available)**

# external factors:

**- raw oil price**

**- Euro-Dollar exchange rate**

**- price lag features**

**- brand of gas station**

# Feature engineering ideas:

**- date-type features will be cyclic features**

**- we will use the coordinates to determine wether the gas station is in a city or on a highway, and we can also use the coordinates to determine the average price in the area, which can be a useful feature.**

**- we will normalize the oil price and exchange rate using z-score**

**- we can create lag features for the price, oil price and exchange rate**

# The Data

**The data is in a csv file. We will read the data using pandas.**

**The data has the following columns:**

**date, station_uuid, diesel, e5, e10, dieselchange, e5change, e10change**

# v1-Features:

**time_sin/cos, day_sind/cos, isHoliday/preHoliday**
**The model already performs better than expected with this fraction of planned features. The error is around 3 cents. I do not**
**think that implementing the remaining features is viable, as an error under 2 cents seems unrealistic.**
