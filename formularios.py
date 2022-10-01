from wtforms import Form
from wtforms import SearchField
from wtforms.validators import DataRequired,Length

class BuscarUsuario(Form):
    nombreusuario=SearchField('Buscar Usuario',validators=[Length(max=200,message="Ingrese un nombre de un usuario valido"),DataRequired(message="El nombre de usuario es requerido")])