class InterviewError(Exception):
    """Base exception for all interview related errors"""
    pass

class InvalidOfficerNameException(InterviewError):
    """Exception raised when officer name is invalid"""
    pass

class InvalidRankException(InterviewError):
    """Exception raised when officer rank is invalid"""
    pass

class Interviewer:
    VALID_RANKS = ['Captain', 'Major', 'Colonel', 'Brigadier']
    
    def __init__(self, officername, rank):
        if not isinstance(officername, str) or len(officername) < 2:
            raise InvalidOfficerNameException("Officer name must be at least 2 characters long")
        if rank not in self.VALID_RANKS:
            raise InvalidRankException(f"Rank must be one of {self.VALID_RANKS}")
        
        self.officername = officername
        self.rank = rank
        self.questions_asked = 0

    def askquestion(self):
        self.questions_asked += 1
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_stats(self):
        return f"{self.rank} {self.officername} has asked {self.questions_asked} questions"

class PersonalInterview(Interviewer):
    def __init__(self, officername, rank):
        super().__init__(officername, rank)
        self.questions = [
            "Introduce yourself.",
            "What are your hobbies?",
            "Why do you want to join the armed forces?",
            "Tell me about your family background."
        ]
    
    def askquestion(self):
        super().askquestion()
        question = self.questions[self.questions_asked % len(self.questions)]
        print(f"{self.rank} {self.officername}: {question}")

class SituationalInterview(Interviewer):
    def __init__(self, officername, rank):
        super().__init__(officername, rank)
        self.scenarios = [
            "What will be your response if you don't clear this SSB attempt?",
            "How would you handle a subordinate's misconduct?",
            "What would you do if you witness corruption in your unit?",
            "How would you boost team morale during a difficult mission?"
        ]
    
    def askquestion(self):
        super().askquestion()
        scenario = self.scenarios[self.questions_asked % len(self.scenarios)]
        print(f"{self.rank} {self.officername}: {scenario}")

class PsychologicalInterview(Interviewer):
    def __init__(self, officername, rank):
        super().__init__(officername, rank)
        self.psych_questions = [
            "How do you handle stress?",
            "What is your biggest fear?",
            "How do you react to failure?",
            "Describe your leadership style."
        ]
    
    def askquestion(self):
        super().askquestion()
        question = self.psych_questions[self.questions_asked % len(self.psych_questions)]
        print(f"{self.rank} {self.officername}: {question}")

def conductinterview(interviewers, rounds=2):
    print("\n=== SSB Interview Session Started ===")
    try:
        for round_num in range(rounds):
            print(f"\nRound {round_num + 1}:")
            for interviewer in interviewers:
                interviewer.askquestion()
        
        print("\n=== Interview Statistics ===")
        for interviewer in interviewers:
            print(interviewer.get_stats())
            
    except InterviewError as e:
        print(f"Interview Error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        print("\n=== SSB Interview Session Ended ===")

if __name__ == "__main__":
    try:
        interviewers = [
            PersonalInterview("Rao", "Captain"),
            SituationalInterview("Singh", "Major"),
            PsychologicalInterview("Sharma", "Colonel")
        ]
        
        conductinterview(interviewers, rounds=3)
        
        # Uncomment to test error handling:
        # invalid_interviewer = PersonalInterview("", "General")
        
    except InterviewError as e:
        print(f"Error during interview setup: {e}")
