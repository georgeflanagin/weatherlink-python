import decimal

"""
It is important that all of the math in this module takes place using decimal precision. Floating-point precision is
far too inaccurate.
"""

ONE = decimal.Decimal('1')
ONE_TENTH = decimal.Decimal('0.1')
ONE_HUNDREDTH = ONE_TENTH * ONE_TENTH
FIVE_NINTHS = decimal.Decimal('5.0') / decimal.Decimal('9.0')
NINE_FIFTHS = decimal.Decimal('9.0') / decimal.Decimal('5.0')

CELSIUS_CONSTANT = decimal.Decimal('32')
KELVIN_CONSTANT = decimal.Decimal('459.67')
KILOPASCAL_MERCURY_CONSTANT = decimal.Decimal('0.295299830714')
MILLIBAR_MERCURY_CONSTANT = KILOPASCAL_MERCURY_CONSTANT * ONE_TENTH
METERS_PER_SECOND_CONSTANT = decimal.Decimal('0.44704')

# Wet bulb constants used by NOAA/NWS in its wet bulb temperature charts
WB_0_00066 = decimal.Decimal('0.00066')
WB_0_007 = decimal.Decimal('0.007')
WB_0_114 = decimal.Decimal('0.114')
WB_0_117 = decimal.Decimal('0.117')
WB_2_5 = decimal.Decimal('2.5')
WB_6_11 = decimal.Decimal('6.11')
WB_7_5 = decimal.Decimal('7.5')
WB_14_55 = decimal.Decimal('14.55')
WB_15_9 = decimal.Decimal('15.9')
WB_237_7 = decimal.Decimal('237.7')

# Dew point constants used by NOAA/NWS in the August-Roche-Magnus approximation with the Bogel modification
DP_A = decimal.Decimal('6.112')  # millibars
DP_B = decimal.Decimal('17.67')  # no units
DP_C = decimal.Decimal('243.5')  # degrees Celsius
DP_D = decimal.Decimal('234.5')  # degrees Celsius

# Heat index constants used by NOAA/NWS in its heat index tables
HI_C1 = decimal.Decimal('-42.379')
HI_C2 = decimal.Decimal('2.04901523')
HI_C3 = decimal.Decimal('10.14333127')
HI_C4 = decimal.Decimal('-0.22475541')
HI_C5 = decimal.Decimal('-0.00683783')
HI_C6 = decimal.Decimal('-0.05481717')
HI_C7 = decimal.Decimal('0.00122874')
HI_C8 = decimal.Decimal('0.00085282')
HI_C9 = decimal.Decimal('-0.00000199')

# Wind chill constants used by NOAA/NWS in its wind chill tables
WC_C1 = decimal.Decimal('35.74')
WC_C2 = decimal.Decimal('0.6215')
WC_C3 = decimal.Decimal('35.75')
WC_C4 = decimal.Decimal('0.4275')
WC_V_EXP = decimal.Decimal('0.16')

# Constants used by Davis Instruments for its THW calculations
THW_INDEX_CONSTANT = decimal.Decimal('1.072')

# Constants used by the Australian Bureau of Meteorology for its apparent temperature (THSW) calculations
THSW_0_348 = decimal.Decimal('0.348')
THSW_0_70 = decimal.Decimal('0.70')
THSW_4_25 = decimal.Decimal('4.25')
THSW_6_105 = decimal.Decimal('6.105')
THSW_17_27 = decimal.Decimal('17.27')
THSW_237_7 = decimal.Decimal('237.7')

HEAT_INDEX_THRESHOLD = decimal.Decimal('70.0')  # degrees Fahrenheit
WIND_CHILL_THRESHOLD = decimal.Decimal('40.0')  # degrees Fahrenheit
DEGREE_DAYS_THRESHOLD = decimal.Decimal('65.0')  # degrees Fahrenheit


def convert_fahrenheit_to_kelvin(temperature):
	return (temperature + KELVIN_CONSTANT) * FIVE_NINTHS
assert convert_fahrenheit_to_kelvin(32) == decimal.Decimal('273.15')
assert convert_fahrenheit_to_kelvin(60).quantize(decimal.Decimal('0.01')) == decimal.Decimal('288.71')


def convert_kelvin_to_fahrenheit(temperature):
	return (temperature * NINE_FIFTHS) - KELVIN_CONSTANT
assert convert_kelvin_to_fahrenheit(convert_fahrenheit_to_kelvin(32)) == decimal.Decimal('32')
assert convert_kelvin_to_fahrenheit(convert_fahrenheit_to_kelvin(60)).quantize(decimal.Decimal('0.00000001')) == decimal.Decimal('60')


def convert_fahrenheit_to_celsius(temperature):
	return (temperature - CELSIUS_CONSTANT) * FIVE_NINTHS
assert convert_fahrenheit_to_celsius(32) == decimal.Decimal('0')
assert convert_fahrenheit_to_celsius(212) == decimal.Decimal('100')


def convert_celsius_to_fahrenheit(temperature):
	return (temperature * NINE_FIFTHS) + CELSIUS_CONSTANT
assert convert_celsius_to_fahrenheit(convert_fahrenheit_to_celsius(32)) == decimal.Decimal('32')
assert convert_celsius_to_fahrenheit(convert_fahrenheit_to_celsius(212)) == decimal.Decimal('212')


def convert_inches_of_mercury_to_kilopascals(barometric_pressure):
	return (barometric_pressure / KILOPASCAL_MERCURY_CONSTANT).quantize(ONE_HUNDREDTH)
assert convert_inches_of_mercury_to_kilopascals(1) == decimal.Decimal('3.39')
assert convert_inches_of_mercury_to_kilopascals(decimal.Decimal('29.45')) == decimal.Decimal('99.73')
assert convert_inches_of_mercury_to_kilopascals(30) == decimal.Decimal('101.59')


def convert_inches_of_mercury_to_millibars(barometric_pressure):
	return (barometric_pressure / MILLIBAR_MERCURY_CONSTANT).quantize(ONE_HUNDREDTH)
assert convert_inches_of_mercury_to_millibars(1) == decimal.Decimal('33.86')
assert convert_inches_of_mercury_to_millibars(decimal.Decimal('29.45')) == decimal.Decimal('997.29')
assert convert_inches_of_mercury_to_millibars(30) == decimal.Decimal('1015.92')


def convert_miles_per_hour_to_meters_per_second(wind_speed):
	return wind_speed * METERS_PER_SECOND_CONSTANT
assert convert_miles_per_hour_to_meters_per_second(1) == decimal.Decimal('0.44704')
assert convert_miles_per_hour_to_meters_per_second(13) == decimal.Decimal('5.81152')


def calculate_wet_bulb_temperature(temperature, relative_humidity, barometric_pressure):
	T = temperature
	RH = relative_humidity
	P = convert_inches_of_mercury_to_millibars(barometric_pressure)
	Tdc = (
		T - (WB_14_55 + WB_0_114 * T) * (1 - (ONE_HUNDREDTH * RH)) -
		((WB_2_5 + WB_0_007 * T) * (1 - (ONE_HUNDREDTH * RH))) ** 3 -
		(WB_15_9 + WB_0_117 * T) * (1 - (ONE_HUNDREDTH * RH)) ** 14
	)
	E = WB_6_11 * 10 ** (WB_7_5 * Tdc / (WB_237_7 + Tdc))
	return (
		(((WB_0_00066 * P) * T) + ((4098 * E) / ((Tdc + WB_237_7) ** 2) * Tdc)) / ((WB_0_00066 * P) + (4098 * E) / ((Tdc + WB_237_7) ** 2))
	).quantize(ONE_TENTH)
assert calculate_wet_bulb_temperature(decimal.Decimal('84.4'), decimal.Decimal('50'), decimal.Decimal('29.80')) == decimal.Decimal('69.4')
assert calculate_wet_bulb_temperature(decimal.Decimal('91.5'), decimal.Decimal('45'), decimal.Decimal('30.01')) == decimal.Decimal('73.4')
assert calculate_wet_bulb_temperature(decimal.Decimal('55.7'), decimal.Decimal('85'), decimal.Decimal('29.41')) == decimal.Decimal('52.8')


def _dew_point_gamma_m(T, RH):
	return (
		RH / 100 * (
			(DP_B - (T / DP_D)) * (T / (DP_C + T))
		).exp()
	).ln()

def calculate_dew_point(temperature, relative_humidity):
	T = convert_fahrenheit_to_celsius(temperature)
	RH = relative_humidity
	return convert_celsius_to_fahrenheit(
		(DP_C * _dew_point_gamma_m(T, RH)) / (DP_B - _dew_point_gamma_m(T, RH))
	).quantize(ONE_TENTH)
assert calculate_dew_point(decimal.Decimal('83.1'), decimal.Decimal('54')) == decimal.Decimal('64.4')
assert calculate_dew_point(decimal.Decimal('82.1'), decimal.Decimal('55')) == decimal.Decimal('64.0')
assert calculate_dew_point(decimal.Decimal('77.9'), decimal.Decimal('58')) == decimal.Decimal('61.7')
assert calculate_dew_point(decimal.Decimal('54.5'), decimal.Decimal('97')) == decimal.Decimal('53.6')
assert calculate_dew_point(decimal.Decimal('32.0'), decimal.Decimal('99')) == decimal.Decimal('31.8')
assert calculate_dew_point(decimal.Decimal('95.0'), decimal.Decimal('31')) == decimal.Decimal('59.2')


def calculate_heat_index(temperature, relative_humidity):
	if temperature < HEAT_INDEX_THRESHOLD:
		return None

	T = temperature
	RH = relative_humidity
	return (
		HI_C1 + (HI_C2 * T) + (HI_C3 * RH) + (HI_C4 * T * RH) + (HI_C5 * T * T) +
		(HI_C6 * RH * RH) + (HI_C7 * T * T * RH) + (HI_C8 * T * RH * RH) + (HI_C9 * T * T * RH * RH)
	).quantize(ONE_TENTH, rounding=decimal.ROUND_UP)
assert calculate_heat_index(decimal.Decimal('69.9'), decimal.Decimal('90')) == None
assert calculate_heat_index(decimal.Decimal('80'), decimal.Decimal('40')) == decimal.Decimal('80.0')
assert calculate_heat_index(decimal.Decimal('81.5'), decimal.Decimal('58')) == decimal.Decimal('83.5')
assert calculate_heat_index(decimal.Decimal('80'), decimal.Decimal('100')) == decimal.Decimal('87.2')
assert calculate_heat_index(decimal.Decimal('100'), decimal.Decimal('65')) == decimal.Decimal('135.9')


def calculate_wind_chill(temperature, wind_speed):
	if temperature > WIND_CHILL_THRESHOLD:
		return None

	T = temperature
	V = wind_speed ** WC_V_EXP
	return (
		WC_C1 + (WC_C2 * T) - (WC_C3 * V) + (WC_C4 * T * V)
	).quantize(ONE)
assert calculate_wind_chill(decimal.Decimal('40.1'), decimal.Decimal('5')) == None
assert calculate_wind_chill(decimal.Decimal('40.0'), decimal.Decimal('5')) == decimal.Decimal('36')
assert calculate_wind_chill(decimal.Decimal('40.0'), decimal.Decimal('45')) == decimal.Decimal('26')
assert calculate_wind_chill(decimal.Decimal('0'), decimal.Decimal('5')) == decimal.Decimal('-11')
assert calculate_wind_chill(decimal.Decimal('0'), decimal.Decimal('45')) == decimal.Decimal('-30')


def calculate_thw_index(temperature, relative_humidity, wind_speed):
	return (
		calculate_heat_index(temperature, relative_humidity) -
		(THW_INDEX_CONSTANT * wind_speed).quantize(ONE_TENTH, rounding=decimal.ROUND_DOWN)
	)


def calculate_thsw_index(temperature, relative_humidity, solar_radiation, wind_speed):
	T = convert_fahrenheit_to_celsius(temperature)
	WS = convert_miles_per_hour_to_meters_per_second(wind_speed)
	E = relative_humidity / 100 * THSW_6_105 * (THSW_17_27 * T / ( THSW_237_7 + T )).exp()
	Thsw = T + (THSW_0_348 * E) - (THSW_0_70 * WS) + THSW_0_70 * (solar_radiation / (WS + 10)) - THSW_4_25
	return convert_celsius_to_fahrenheit(Thsw).quantize(ONE_TENTH)

def calculate_cooling_degree_days(average_temperature):
	if average_temperature <= DEGREE_DAYS_THRESHOLD:
		return None
	return average_temperature - DEGREE_DAYS_THRESHOLD

def calculate_heating_degree_days(average_temperature):
	if average_temperature >= DEGREE_DAYS_THRESHOLD:
		return None
	return DEGREE_DAYS_THRESHOLD - average_temperature
