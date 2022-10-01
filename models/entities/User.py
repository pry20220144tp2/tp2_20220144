from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, nombre, correo, password, rol="") -> None:
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol
    
  
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)