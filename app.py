from flask import Flask, render_template
import psycopg2

investing_simulation = Flask(__name__)

@investing_simulation.route("/")
def connect_to_database():
    connection = psycopg2.connect(
        host="ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        database="d2o7fsji8voktj",
        user="u9ssoi3qi31nm8", 
        password="pd754de5e907f36c44793b6f4472fc3dd6e09ef86c61d0da2fd7afb648fbfcc97", 
        port="5432"
    )
def load_webpage():
    return render_template('Interface.html')