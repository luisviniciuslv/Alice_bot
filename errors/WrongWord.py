class WrongWord(Exception):
    def __init__(self, attempts):
        self.attempts = attempts
    def __str__(self):
        return f"Você errou, agora tem {self.attempts} tentativas"