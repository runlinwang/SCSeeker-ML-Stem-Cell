import os

from flask import Flask, render_template, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras

from helpers import apology

# preventing warning indications from showing up, which clutter the interface
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/demonstration", methods=["GET", "POST"])
def demonstration():
    if request.method == "POST":

        model = keras.models.load_model("model.h5")

        FGF13 = request.form.get("FGF13")
        GDF3 = request.form.get("GDF3")
        SKIL = request.form.get("SKIL")
        ERAS = request.form.get("ERAS")
        TRIM28 = request.form.get("TRIM28")
        ZFX = request.form.get("ZFX")

        try:
            float(FGF13)
            float(GDF3)
            float(SKIL)
            float(ERAS)
            float(TRIM28)
            float(ZFX)
        except:
            return render_template("premodel.html", errorinput=True)

        if isinstance(float(FGF13),float) and 100 >= float(FGF13) >= 0 and isinstance(float(GDF3), float) and 100 >= \
                float(GDF3) >= 0 and isinstance(float(SKIL), float) and 100 >= float(SKIL) >= 0 and \
                isinstance(float(ERAS), float) and 100 >= float(ERAS) >= 0 and isinstance(float(TRIM28), float) \
                and 100 >= float(TRIM28) >= 0 and isinstance(float(ZFX), float) and 100 >= float(ZFX) >= 0:
            issue = False
        else:
            issue = True

        if issue == True:
            return render_template("premodel.html", errorinput=True)

        FGF13 = str(float(FGF13) / 100)
        GDF3 = str(float(GDF3) / 100)
        SKIL = str(float(SKIL) / 100)
        ERAS = str(float(ERAS) / 100)
        TRIM28 = str(float(TRIM28) / 100)
        ZFX = str(float(ZFX) / 100)



        dataframe = pd.DataFrame({"FGF13": [FGF13],
                                  "GDF3": [GDF3],
                                  "SKIL": [SKIL],
                                  "ERAS": [ERAS],
                                  "TRIM28": [TRIM28],
                                  "ZFX": [ZFX]})

        predictions = model.predict(dataframe).flatten()

        percentage = 100*predictions[0]

        if float(percentage) > 100:
            percentage = "over 100"
        elif float(percentage) < 0:
            percentage = "less than 0"
        else:
            percentage = round(percentage * 100) / 100

        return render_template("postmodel.html", percentage=percentage)
    else:
        return render_template("premodel.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/methodology")
def methodology():
    return render_template("methodology.html")

@app.route("/impact")
def impact():
    return render_template("impact.html")

@app.route("/context")
def context():
    return render_template("context.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology()


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
