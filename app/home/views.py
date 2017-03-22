from flask import render_template, redirect, url_for

from . import home
from .. import threadManager

"""
Homepage that displays threads ordered by score
"""
@home.route('/', defaults = {'pageNo' : 0})
@home.route('/<int:pageNo>')
def homepage(pageNo):
    threads = threadManager.getThreads(pageNo * 20, (pageNo + 1) * 20)
    return render_template('home/index.html', title = "Home",
        pageNo = pageNo, threads = threads)

"""
Upvote functionality for homepage, updates and redirects back to homepage
"""
@home.route('/upvote/<int:threadId>/<int:pageNo>')
def upvote_thread(threadId, pageNo):
    threadManager.upvoteThread(threadId)
    return redirect(url_for('home.homepage', pageNo = pageNo))

"""
Downvote functionality for homepage, updates and redirects back to homepage
"""
@home.route('/downvote/<int:threadId>')
def downvote_thread(threadId):
    threadManager.downvoteThread(threadId)
    return redirect(url_for('home.homepage'))
