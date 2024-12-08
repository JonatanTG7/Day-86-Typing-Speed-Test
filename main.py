import time
from tkinter import Tk
from gui import GUI
from typing_speed import start_timer, calculate_wpm

# Initializes the MainApp class, which represents the application.
# It initializes the GUI and other variables related to the test.
class MainApp:
    def __init__(self, root):
        self.root = root
        self.gui = GUI(root, self)
        self.start_time = None
        self.end_time = None
        self.timer_running = False #Flag to check if the time is running 

#Starts the typing test by recording the start time using the start_timer function.
    def start_test(self):
        self.start_time = start_timer()  

#Ends the typing test: calculates elapsed time and computes WPM based on typed text.
    def end_test(self, typed_text):
        if self.timer_running:
            self.end_time = time.time() 
            wpm = calculate_wpm(self.start_time, self.end_time, typed_text)
            self.gui.display_result(wpm)  

if __name__ == "__main__":
    window = Tk()
    window.title("Typing Speed Test")
    window.minsize(500,500)
    app = MainApp(window)
    window.mainloop()