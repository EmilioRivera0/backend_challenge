# dependencies ------------>
from chalice import Chalice

# program variables ------------>
app = Chalice(app_name='backend_challenge')


# endpoints ------------>
@app.route('/')
def index():
    return {'hello': 'world'}