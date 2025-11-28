import tkinter as tk
from temperature import Temperature

def only_decimal(char, word):
    """Validate that the new char entered and the resulting word is a valid start to a float"""
    check = False
    # Allow any digit
    if char.isdigit():
        check = True
    # Allow a single negative sign
    elif word == '-':
        check = True
    # Allow a . if no . already exists
    elif char == '.' and not '.' in word[:-1]:
        check = True
    else:
        check = False
    return check

class TemperatureGUIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Temperature Converter')
        self.geometry('300x70')
        self.resizable(False, False)

        self.main_frame = TemperatureConverterFrame(self)
        self.main_frame.pack()


class TemperatureConverterFrame(tk.Frame):
    def __init__(self, master: TemperatureGUIApp):
        super().__init__()
        
        # Create an instance of the temperature model that will convert and store the temperatures
        # in different unit
        self.temperature = Temperature(celsius=0)

        # master is the tk widget that the TemperatureConverterFrame is attached to
        self.master = master
        self.temp_celsius = tk.StringVar()
        self.temp_celsius.trace_add("write", self.do_conversion)
        
        validation = self.register(only_decimal)

        self.temperature_label = tk.Label(self, text="Celsius")
        self.temperature_entry = tk.Entry(self, textvariable=self.temp_celsius,
                                          validate="key",
                                          validatecommand=(validation, '%S', '%P'),
                                          width=10,
                                          justify="center")
        self.convert_button = tk.Button(self, text="Convert", command=self.do_conversion)
        self.output_label = tk.Label(self)

        # Place the widgets in the TemperatureConverterGUI Frame
        self.place_widgets()

        # Put the focus on the entry box, so that values can be typed in directly
        self.temperature_entry.focus()

        # Bind the return key to run the do_conversion method
        self.master.bind("<Return>", self.do_conversion)

        # Bind all keys. The callback will determine the action depending on the key pressed
        self.master.bind("<KeyRelease>", self.on_key_release)

        # Run the do_conversion to get the initial message
        self.do_conversion()

    def place_widgets(self):
        padding_options = {'padx': 5, 'pady': 5}

        # Use this method to place the widgets using the grid layout manager
        self.temperature_label.grid(row=0, column=0, sticky="w", **padding_options)
        self.temperature_entry.grid(row=0, column=1, **padding_options)
        self.convert_button.grid(row=0, column=2, **padding_options)
        self.output_label.grid(row=1, column=0, columnspan=3)

    def do_conversion(self, *args):
        """ Method uses the underlying temperature model in self.temperature_model to do the conversion
        and show the converted value in the message box. """
        # *args is used to take any event parameters that are passed due to a key press or
        # a change in a tk.StrVar with a trace_add
        try:
            temp_c = float(self.temp_celsius.get())
            self.temperature.celsius = temp_c
            temp_f = self.temperature.fahrenheit
            output_message = f'{temp_c:.1f} \N{DEGREE CELSIUS} = {temp_f:.1f} \N{DEGREE FAHRENHEIT}'
        except ValueError :
            output_message = f'Enter a temperature in Celsius'
        self.output_label.config(text=output_message)

    def on_key_release(self, event):
        """ Callback function that runs if any key is pressed and released"""
        print(event)
        if event.keysym == 'Escape':
            self.master.destroy()

        

if __name__ == '__main__':
    app = TemperatureGUIApp()
    app.mainloop()
