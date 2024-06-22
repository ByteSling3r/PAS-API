from datetime import datetime
import pytz

colombia_tz = pytz.timezone('America/Bogota')

colombia_time = datetime.now(colombia_tz)

print("Fecha y hora en Colombia:", colombia_time.strftime('%H:%M:%S'))
