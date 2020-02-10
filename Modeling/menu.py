class M_Menu:
    """Data Model for Menu"""

    def __init__(self, user: str, date: str, name: str, meal: str, dish: str):
        self.user = user
        self.date = date
        self.name = name
        self.meal = meal
        self.dish = dish    
    