from flask import render_template, redirect, url_for

from . import home
from .. import threadManager

"""
Homepage that displays top 20 threads
"""
@home.route('/')
def homepage():
    threads = threadManager.getThreads(0, 20)
    return render_template('home/index.html', title="Title", threads=threads)

"""
Upvote functionality for homepage, updates and redirects back to homepage
"""
@home.route('/upvote/<int:threadId>')
def upvote_thread(threadId):
    threadManager.upvoteThread(threadId)
    return redirect(url_for('home.homepage'))

"""
Downvote functionality for homepage, updates and redirects back to homepage
"""
@home.route('/downvote/<int:threadId>')
def downvote_thread(threadId):
    threadManager.downvoteThread(threadId)
    return redirect(url_for('home.homepage'))
