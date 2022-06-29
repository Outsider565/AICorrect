from flask import Flask
from flask import request, render_template
from engine import run_debug



app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/api/run")
def get_path():
    path = request.args.get("path")
    crush = request.args.get("crush")
    cpu = request.args.get("cpu")
    mem = request.args.get("mem")
    time = request.args.get("time")
    correct = request.args.get("correct")
    user_report = {
        "crush": int(crush) if crush else 0,
        "cpu": int(cpu) if cpu else 0,
        "mem": int(mem) if mem else 0,
        "time": int(time) if time else 0,
        "correct": int(correct) if correct else 0
    }
    print(path, user_report)
    return run_debug(path, user_report)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
