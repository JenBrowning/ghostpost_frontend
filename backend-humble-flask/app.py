#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jen Browning'

from flask import Flask, flash, redirect, render_template, request
from tinydb import TinyDB
import random
app = Flask(__name__)
db = TinyDB('db.json')


@app.route('/')
def index():
    """doc string """
    rdm_item = random.choice(db.all())
    return render_template('index.html', recipe=rdm_item)
    

# if __name__ == "__main__":
#     app.run()