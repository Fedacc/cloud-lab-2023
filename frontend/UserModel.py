class User():
    name = "tester"
    mail = "tester@yourmail.com"
    id = "testerUser0001"

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_active(self):
        return True
    
    def get_id(self):
        return self.id