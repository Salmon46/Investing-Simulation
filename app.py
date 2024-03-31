from flask import Flask, render_template

investing_simulation = Flask(__name__)

investing_simulation.config['SECRET_KEY'] = 'Sudin@110508'

@investing_simulation.route("/")
def webpage():
    
    return render_template('Interface.html')