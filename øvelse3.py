import sqlite3
import Adafruit_DHT
import time

# Angiv DHT11-sensoren pin-nummer (her bruger vi pin 4)
sensor = Adafruit_DHT.DHT11
pin = 4

# Opret forbindelse til SQLite-databasen
try:
    conn = sqlite3.connect('dht11_data.db')
    c = conn.cursor()

    # Opret en tabel for sensordata
    c.execute('''CREATE TABLE IF NOT EXISTS dht11_data
                 (timestamp INTEGER, temperature REAL, humidity REAL)''')
except sqlite3.Error as e:
    print("Fejl ved oprettelse af forbindelse til databasen: ", e)

while True:
    try:
        # Læs sensordata
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Indsæt data i databasen
        timestamp = int(time.time())
        c.execute("INSERT INTO dht11_data VALUES (?, ?, ?)",
                  (timestamp, temperature, humidity))
        conn.commit()

        # Vent i 10 sekunder
        time.sleep(10)
    except Exception as e:
        conn.rollback()
        print("Fejl ved læsning og indsættelse af sensordata: ", e)

# Luk forbindelsen til databasen
conn.close()
