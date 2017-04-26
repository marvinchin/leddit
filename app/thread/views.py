from flask import render_template, redirect, url_for, flash
from forms import ThreadForm
from .. import threadManager
from . import thread

"""
Page for creation of new thread, redirects to homepage upon success, or backed
to page with error message if failure
"""
@thread.route('/new', methods=['GET', 'POST'])
def add_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        try:
            threadManager.newThread(form.topic.data)
        except ValueError:
            flash("Please limit topic to 255 characters")
            return redirect(url_for('thread.add_thread'))
        return redirect(url_for('home.homepage'))
    return render_template('thread/add.html', title = "New Thread", form = form)

"""
Page to view thread with given id
"""
@thread.route('/<int:threadId>')
def view_thread(threadId):
    try:
        thread = threadManager.getThread(threadId)
    except IndexError:
        flash("Thread does not exist!")
        return redirect(url_for('home.homepage'))
    title = "Thread {0}".format(threadId)
    return render_template('thread/thread.html', title = title, thread = thread)

"""
Upvote functionality for thread page, redirects to thread page
"""
@thread.route('/upvote/<int:threadId>')
def upvote_thread(threadId):
    try:
        threadManager.upvoteThread(threadId)
    except IndexError:
        flash("Thread does not exist!")
        return redirect(url_for('home.homepage'))
    return redirect(url_for('thread.view_thread', threadId = threadId))

"""
Downvote functionality for thread page, redirects to thread page
"""
@thread.route('/downvote/<int:threadId>')
def downvote_thread(threadId):
    try:
        threadManager.downvoteThread(threadId)
    except IndexError:
        flash("Thread does not exist!")
        return redirect(url_for('home.homepage'))
    return redirect(url_for('thread.view_thread', threadId = threadId))
