from flask import render_template

from . import home
from .. import threadManager

@home.route('/')
def homepage():
    threads = threadManager.getThreads(0, 20)
    print threads
    return render_template('home/index.html', title="Title", threads=threads)
