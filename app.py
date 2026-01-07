from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def calculate_risk(answers):
    total_risk = 0
    max_risk = 0
    failed = []

    with open("controls.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            control = row["Control"]
            likelihood = int(row["Likelihood"])
            impact = int(row["Impact"])

            risk_value = likelihood * impact
            max_risk += risk_value

            if answers.get(control) == "no":
                total_risk += risk_value
                failed.append((control, risk_value, row["ISO27001"], row["NIST"]))


    risk_percentage = (total_risk / max_risk) * 100

    if risk_percentage < 30:
        level = "LOW"
    elif risk_percentage < 60:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return risk_percentage, level, failed

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    failed = []

    if request.method == "POST":
        answers = request.form.to_dict()
        score, level, failed = calculate_risk(answers)
        result = (score, level)

    return render_template("index.html", result=result, failed=failed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

