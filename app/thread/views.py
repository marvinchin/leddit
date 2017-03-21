from flask import render_template, redirect, url_for
from forms import ThreadForm
from .. import threadManager
from . import thread

@thread.route('/new', methods=['GET', 'POST'])
def add_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        threadManager.newThread(form.topic.data)
        return redirect(url_for('home.homepage'))
    return render_template('thread/add.html', title = "New Thread", form = form)

@thread.route('/<int:threadId>')
def view_thread(threadId):
    thread = threadManager.getThread(threadId)
    title = "Thread {0}".format(threadId)
    return render_template('thread/thread.html', title = title, thread = thread)
