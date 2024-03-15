import os
from os.path import join

from flask import Flask, send_file, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import InputRequired, Length

from utils import parse_and_export_excel, clear_directory

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12)

DEFAULT_FOLDER = join(os.getcwd(), "files")
DEFAULT_FILENAME = join(DEFAULT_FOLDER, "results.xlsx")


class TextForm(FlaskForm):
    text = TextAreaField(
        "Greatness.Compare pipeline output from the Extensions tab:",
        validators=[InputRequired(), Length(min=10)],
    )
    filename = StringField(
        "Filename",
        validators=[InputRequired(), Length(min=4)],
    )


@app.route("/download/<filename>")
def download(filename):
    # path = DEFAULT_FILENAME
    return send_file(filename, as_attachment=True)


@app.route("/", methods=("GET", "POST"))
def index():
    form = TextForm()
    if form.validate_on_submit():
        # Get the form data
        text = form.text.data
        filename = form.filename.data 

        if not filename.endswith(".xlsx"):
            filename = f"{filename}.xlsx"

        if filename is None:
            filename = DEFAULT_FILENAME
        else:
            filename = join(DEFAULT_FOLDER, filename)
        
        # Generate the excel file and redirect to download
        parse_and_export_excel(text=text, out_filename=filename)
        return redirect(url_for("download", filename=filename))
    return render_template("index.html", form=form)


if __name__ == "__main__":
    clear_directory(DEFAULT_FOLDER)
    app.run(port=5000, debug=True)
