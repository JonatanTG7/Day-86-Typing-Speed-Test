import time

def start_timer():
    return time.time()

#calc the wmp
def calculate_wpm(start_time, end_time, typed_text):
    time_taken = end_time - start_time
    word_count = len(typed_text.split())
    wpm = (word_count / time_taken) * 60
    return round(wpm, 2)

