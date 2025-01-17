import numpy as np
import pandas as pd

def generate_iot_data_low_occupancy_high_appliance():
    np.random.seed(0)  # For reproducibility
    hours = 24 * 7  # 1 week
    time_index = pd.date_range(start='2023-01-01', periods=hours, freq='H')

    # Generate synthetic environmental data
    temperature = np.random.normal(loc=22, scale=2, size=hours)  # Temperature in °C
    luminosity = np.random.uniform(low=100, high=1000, size=hours)  # Luminosity level
    co_level = np.random.uniform(low=0, high=5, size=hours)  # Carbon monoxide level
    humidity = np.random.uniform(low=30, high=60, size=hours)  # Humidity level

    # Generate appliance settings with high performance
    fan_speed = np.random.randint(8, 11, size=hours)  # Fan speed setpoints (8 to 10)
    smart_light = np.random.randint(8, 11, size=hours)  # Smart light bulb setpoints (8 to 10)
    smart_humidifier = np.random.randint(8, 11, size=hours)  # Smart humidifier setpoints (8 to 10)
    smart_air_purifier = np.random.randint(8, 11, size=hours)  # Smart air purifier setpoints (8 to 10)

    # Generate low occupancy (mostly unoccupied in the morning)
    occupancy = np.where(np.arange(hours) < 12, 0, 1)  # 0 (unoccupied) in the first 12 hours, 1 (occupied) thereafter

    # Calculate energy usage based on appliance settings and occupancy
    energy_usage = (
        0.5 * fan_speed +
        0.3 * smart_light +
        0.4 * smart_humidifier +
        0.2 * smart_air_purifier +
        0.5 * occupancy  # Extra usage when occupied
    )

    # Create DataFrame
    df = pd.DataFrame({
        'Timestamp': time_index,
        'Temperature (°C)': temperature,
        'Luminosity (lux)': luminosity,
        'CO Level (ppm)': co_level,
        'Humidity (%)': humidity,
        'Fan Speed': fan_speed,
        'Smart Light': smart_light,
        'Smart Humidifier': smart_humidifier,
        'Smart Air Purifier': smart_air_purifier,
        'Occupancy': occupancy,
        'Energy Usage (kWh)': energy_usage
    })

    # Save to CSV
    df.to_csv('iot_data_low_occupancy_high_appliance.csv', index=False)
    print("CSV file 'iot_data_low_occupancy_high_appliance.csv' has been created.")
    
    return df

# Generate the data
iot_data = generate_iot_data_low_occupancy_high_appliance()
