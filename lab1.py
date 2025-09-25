class EmptyAnswerError(Exception):
    pass

class Interviewer:
    def __init__(self, officername):
        self.officername = officername

    def askquestion(self, candidate_name):
        raise NotImplementedError("Subclasses must implement this method")

class PersonalInterview(Interviewer):
    def askquestion(self, candidate_name):
        print(f"{self.officername}: Hello {candidate_name}, please introduce yourself.")
        answer = input("Your Answer: ")
        if answer.strip() == "":
            raise EmptyAnswerError("Answer cannot be empty.")
        print("Response received. Good introduction.\n")

class SituationalInterview(Interviewer):
    def askquestion(self, candidate_name):
        print(f"{self.officername}: {candidate_name}, what will be your response if you don't clear this SSB attempt?")
        answer = input("Your Answer: ")
        if len(answer.strip()) < 10:
            raise EmptyAnswerError("Answer is too short. Please think and respond properly.")
        print("Thank you for your honest response.\n")

def conductinterview(interviewerobject, candidate_name):
    try:
        interviewerobject.askquestion(candidate_name)
    except EmptyAnswerError as e:
        print("Error:", e, "\n")

candidate = input("Enter Candidate Name: ")

officerrao = PersonalInterview("Captain Rao")
officersingh = SituationalInterview("Major Singh")

print("\n--- Personal Interview Round ---")
conductinterview(officerrao, candidate)

print("--- Situational Interview Round ---")
conductinterview(officersingh, candidate)
