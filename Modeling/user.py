class M_User():
    """Data Model for User"""

    def __init__(self, email: str, name: str, password: str, activate_url: str, reset_url: str, accept_terms: int, accept_pub: int):
        self.email = email
        self.name = name
        self.password = password
        self.activate_url = activate_url
        self.reset_url = reset_url
        self.accept_terms = accept_terms
        self.accept_pub = accept_pub