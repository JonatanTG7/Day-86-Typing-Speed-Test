from tkinter import Label, Button, Entry, Text
import random
import time

class GUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        #Creating a Text widget to display sample text (non-editable)
        self.text_widget = Text(root, wrap="word", height=6, width=50, font=("Arial", 14))
        self.text_widget.pack(pady=20, padx=10)  
        self.text_widget.config(state="disabled")

        #Input field for typing the text
        self.entry_widget = Entry(root, font=("Arial", 14))
        self.entry_widget.pack(pady=10, padx=10) 
        self.entry_widget.config(state="disabled")
 
        #start button
        self.start_button = Button(root, text="Start Test", font=("Arial", 16), width=20, height=2, command=self.start_test)
        self.start_button.pack(pady=10, padx=10)  

        #Timer label to show the seconds 
        self.timer_label = Label(root, text="Time left: 60", font=("Arial", 14), fg="red")
        self.timer_label.pack(pady=10, padx=10)  

        
        #Label to display result in real time
        self.result_real_time_label = Label(root, text="")
        self.result_real_time_label.pack(pady=10, padx=10)

        #Label to display result after test completion
        self.result_label = Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20, padx=10)

        #reset button
        self.reset_button = Button(root, text="Reset", font=("Arial", 12), width=10, height=2, command=self.reset_test)
        self.reset_button.pack(pady=10, padx=10) 

        # Bind the entry field to real-time feedback function
        self.entry_widget.bind("<KeyRelease>", self.real_time_feedback)
        
        self.current_text = None
        self.start_time = None
        self.end_time = None
        self.timer_running = False
        self.words_incorrect = 0
        self.words_correct = 0  
        self.time_left = 6 
        self.timer_id = None 

        self.simple_words = [
    "cat", "dog", "apple", "book", "chair", "table", "pencil", "pen", "computer", 
    "phone", "car", "tree", "window", "shoe", "orange", "banana", "pear", "grape", 
    "watermelon", "mango", "peach", "lemon", "kiwi", "strawberry", "melon", "school", 
    "teacher", "student", "classroom", "homework", "lesson", "test", "quiz", "grade", 
    "study", "book", "house", "door", "window", "room", "kitchen", "living", "bedroom", 
    "bathroom", "garden", "yard", "football", "basketball", "baseball", "tennis", "soccer",
    
    "computer", "apple", "orange", "dog", "cat", "book", "pen", "pencil", "ball", "shirt",
    "glove", "hat", "lamp", "window", "floor", "tree", "chair", "desk", "notebook", "bottle",
    "water", "phone", "table", "fruit", "mango", "banana", "peach", "grape", "lemon", "kiwi", 
    "snow", "rain", "weather", "school", "homework", "quiz", "grade", "student", "lesson", 
    "study", "paper", "map", "garden", "house", "room", "door", "kitchen", "living", "bathroom", 
    "sofa", "couch", "car", "bus", "train", "bike", "sports", "soccer", "football", "baseball", 
    "basketball", "tennis", "hockey", "swimming", "gym", "exercise", "run", "walk", "jog", "play",
    
    "computer", "laptop", "keyboard", "mouse", "screen", "monitor", "printer", "camera", "headphones", 
    "speaker", "charger", "battery", "phone", "tablet", "phone", "game", "app", "website", "internet", 
    "social", "network", "post", "tweet", "story", "profile", "comment", "like", "share", "emoji"
]

    #create a text contain 50 words 
    def generate_random_words(self, word_count=50):
        random_words = random.sample(self.simple_words, word_count)
        return " ".join(random_words)

    #func to display the text
    def display_sample_text(self,text):
        self.text_widget.config(state="normal")
        self.text_widget.delete(1.0, "end")
        self.text_widget.insert("end", text)
        self.text_widget.config(state="disabled")

    #start func after clicking the button to start the test 
    def start_test(self):

        self.entry_widget.config(state="normal")
        self.entry_widget.delete(0, 'end')
        self.result_label.config(text="")  
        random_text = self.generate_random_words(50)
        self.display_sample_text(random_text)
        self.app.start_test()

        # Start the timer if it’s not already running
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()

    #Update the time label each second.
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.end_test()

    #Provide real-time feedback on the text entered by the user.
    def real_time_feedback(self, event=None):
        self.text_widget.tag_remove("correct", "1.0", "end")
        self.text_widget.tag_remove("incorrect", "1.0", "end")

        user_input = self.entry_widget.get().strip() 
        reference_text = self.text_widget.get("1.0", "end-1c").strip() 

        user_words = user_input.split()
        reference_words = reference_text.split()

        correct_count = 0
        incorrect_count = 0

        for i, word in enumerate(user_words):
            try:
                start_idx = f"1.0 + {sum(len(w) + 1 for w in reference_words[:i])} chars"
                end_idx = f"{start_idx} + {len(word)} chars"

                if i < len(reference_words) and word == reference_words[i]:
                    self.text_widget.tag_add("correct", start_idx, end_idx)
                    correct_count += 1
                else:
                    self.text_widget.tag_add("incorrect", start_idx, end_idx)
                    incorrect_count += 1
            except:
                pass

        self.text_widget.tag_configure("correct", foreground="green")
        self.text_widget.tag_configure("incorrect", foreground="red")

        self.words_correct = correct_count  
        self.words_incorrect = incorrect_count

        self.result_real_time_label.config(
            text=f"correct word: {correct_count}, Incorrect word: {incorrect_count}, Total: {len(user_words)}"
        )

    #Reset the test to start over: clear input, reset timer, and display instructions.
    def reset_test(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.time_left = 60  
        self.timer_label.config(text="Time left: 60")  

        self.result_label.config(text="")
        self.result_real_time_label.config(text="") 

        self.text_widget.config(state="normal")  
        self.text_widget.delete(1.0, "end")  
        self.text_widget.config(state="disabled") 
        self.entry_widget.config(state="normal")
        self.entry_widget.delete(0, 'end')
        self.entry_widget.config(state="disabled")
        self.current_text = None

        self.timer_running = False 

    #End the typing test: calculate WPM and show results.
    def end_test(self):
        self.is_test_active = False
        self.entry_widget.config(state="disabled")
        self.result_real_time_label.pack_forget()
        elapsed_time = 60 - self.time_left
        if elapsed_time > 0:  
            wpm = (self.words_correct / elapsed_time) * 60
        else:
            wpm = 0
        self.result_label.config(text=f"Your Write {self.words_correct + self.words_incorrect} words and {self.words_incorrect} incorrect words \n Your WPM is: {wpm:.2f}")

