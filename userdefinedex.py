class EmptyAnswerError(Exception):
    pass 
class Interview:
    def __init__(self, name):
        self.name = name

    def start(self):
        print("Welcome", self.name, "to the Virtual Interview!")

class HRInterview(Interview):
    def ask_question(self):
        print("HR Question: Tell me about yourself.")
        answer = input("Your Answer: ")
        if answer == "":
            raise EmptyAnswerError("Answer cannot be empty.")
        print("Thank you for your answer!")

try:
    name = input("Enter your name: ")
    interview = HRInterview(name)
    interview.start()
    interview.ask_question()
except EmptyAnswerError as e:
    print("Error:", e)
