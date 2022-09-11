from flask import Flask, url_for, redirect, request, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
from tkinter import *
import extcolors
from colormap import rgb2hex
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image
import requests
from io import BytesIO


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'SECRET_KEY'

class ImageForm(FlaskForm):
    img_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Submit')


def color_to_df(input):
    colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

    # convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
    return df


@app.route('/', methods =['GET','POST'])
def color_platte():
    form = ImageForm()
    if form.validate_on_submit():
        link = form.img_url.data
        img = requests.get(link).content
        colors_x = extcolors.extract_from_path(BytesIO(img))
        df_color = color_to_df(colors_x)
        list_color = list(df_color['c_code'])
        return render_template('image.html', list_color=list_color, link=link)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
