import tkinter as tk

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.txt = tk.Label(self,
                            text="My tkinter app",
                            bg="blue",
                            fg="white",
                            )
        self.btn = tk.Button(self,
                             text="Press me",
                             bg="red",
                             fg="yellow",
                             activebackground="grey",
                             )

        self.edt = tk.Entry(self,
                            bg="green",
                            fg="pink",
                            )
        self.sld = tk.Scale(self,
                            from_=0,
                            to=100,
                            orient=tk.VERTICAL,
                            )

        # Changes the 'configuration' of an existing widget (the MainFrame)
        self.config(bg="cadetblue2")

        self.place_widgets()

    def place_widgets(self):
        self.txt.grid(row=0,
                      column=0,
                      padx=10,
                      pady=10,
                      sticky="NEWS",
                      )
        self.btn.grid(row=0, column=1)
        self.edt.grid(row=1, column=0)
        self.sld.grid(row=1, column=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tkinter Class Example")
    main_frame = MainFrame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()