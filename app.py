from flask import Flask, render_template

investing_simulation = Flask(__name__)

@investing_simulation.route("/")
def load_webpage():
    return render_template('Interface.html')