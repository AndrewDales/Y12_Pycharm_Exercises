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
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value

    @property
    def fahrenheit(self):
        return (self._celsius * 9 / 5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9

    @property
    def kelvin(self):
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value):
        self._celsius = value - 273.15

    def __repr__(self):
        return f"Temperature(celsius={self._celsius:.1f})"
