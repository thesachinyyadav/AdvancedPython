class Interviewer:
    def __init__(self, officername):
        self.officername = officername

    def askquestion(self):
        raise NotImplementedError("Subclasses must implement this method")


class PersonalInterview(Interviewer):
    def askquestion(self):
        print(f"{self.officername}: Introduce yourself.")


class SituationalInterview(Interviewer):
    def askquestion(self):
        print(f"{self.officername}: What will be your response if you don't clear this SSB attempt?")


def conductinterview(interviewerobject):
    interviewerobject.askquestion()


officerrao = PersonalInterview("Captain Rao")
officersingh = SituationalInterview("Major Singh")

conductinterview(officerrao)
conductinterview(officersingh)
