class Temperature:
    def __init__(self, *args, **kwargs):
        if args:
            self._celsius = args[0]
        elif 'celsius' in kwargs:
            self.celsius = kwargs['celsius']
        elif 'fahrenheit' in kwargs:
            self.fahrenheit = kwargs['fahrenheit']
        elif 'kelvin' in kwargs:
            self.kelvin = kwargs['kelvin']
        else:
            raise TypeError('Temperature in celsius, fahrenheit or kelvin must be specified')


    @property
    def celsius(self):
        return self.celsius

    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError('Celsius value must be greater than absolute zero (-273.15 \u00B0C)')
        self._celsius = value

    @property
    def fahrenheit(self)  -> float:
        fahrenheit = (self._celsius * 9 / 5) + 32
        return fahrenheit

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        if value < -459.67:
            raise ValueError('Kelvin value must be greater than absolute zero (0 \u00B0K)')
        self._celsius = (value - 32) * 5/9

    @property
    def kelvin(self) -> float:
        kelvin = self._celsius + 273.15
        return kelvin

    @kelvin.setter
    def kelvin(self, value: float):
        if value < 0:
            raise ValueError('Kelvin value must be greater than absolute zero (0 \u00B0K)')
        self._celsius = value - 273.15

    def __repr__(self):
        return f"Temperature(celsius={self._celsius:.1f})"

if __name__ == '__main__':
    temp = Temperature(25)
    # Note PyCharm is warning me not to do this!
    print(temp._celsius)
