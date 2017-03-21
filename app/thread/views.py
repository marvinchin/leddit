from flask import render_template, redirect, url_for, flash
from forms import ThreadForm
from .. import threadManager
from . import thread

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

@thread.route('/<int:threadId>')
def view_thread(threadId):
    thread = threadManager.getThread(threadId)
    title = "Thread {0}".format(threadId)
    return render_template('thread/thread.html', title = title, thread = thread)

@thread.route('/upvote/<int:threadId>')
def upvote_thread(threadId):
    threadManager.upvoteThread(threadId)
    return redirect(url_for('thread.view_thread', threadId = threadId))

@thread.route('/downvote/<int:threadId>')
def downvote_thread(threadId):
    threadManager.downvoteThread(threadId)
    return redirect(url_for('thread.view_thread', threadId = threadId))
