# leddit
Reddit/Digg clone for Carousell Coding Quiz

A topic aggregator application that allows users to submit and up/downvote
topics. Homepage displays the top 20 topics ranked by their vote scores.  

## Setup
  Create virtual environment  
  `virtualenv venv`  
  Activate virtual environment  
  `source venv/bin/activate`  
  Install requirements  
  `pip install -r requirements.txt`  
  Configure flask  
  `export FLASK_APP=run.py`  
  Run flask application  
  `flask run`  

## Components

### Thread
The thread class represents a single thread, with the id, topic, and score.
Storage and ordering of the threads are handled in-memory by the ThreadManager
class.

### ThreadManager
Threads are handled by the ThreadManager class, which uses a list to store the
threads indexed by their id numbers. This allows for constant time retrieval of
thread information given their id numbers (which we should know!). Addition of
new threads is also a constant time operation, as we can simply append the thread
to the back of the list. The Id number of each thread should be their position
in the list. If we wish to add deletion, we can simply replace the thread with
a None object to represent that the thread has been removed.

Ordering of threads is backed by a linked list, which maintains the relative
position of each thread in the list. Upon any change to the score of a thread,
we remove the affected thread from the list, search up/down from its original
position until we find a suitable position to reinsert the node.

##### Insertion
A standard linked list implementation, however, would require O(n) time to find
the appropriate position to insert a new thread into the list. Thus we include
an additional pointer which keeps track of the point of insertion as threads
are added and updated. This allows us to provide constant time addition of new
threads.

##### Update
Although the
complexity of this operation is O(n) using a linked list, this only happens if
there are large numbers of threads with the same score clustered together. In
the case of an active application, with users voting on the topics, scores are
more likely to be spread out and a new position can be found by moving affected
threads a small number of nodes up/down from its original position. Given this
assumption a linked list implementation is likely to outperform a tree structure
which requires O(log n) for every update, especially where number of threads is
large.

##### Retrieval
Our application requires us to retrieve the top 20 threads to be displayed on the
front page. With the linked list implementation, this retrieval can be done in
constant time. However, with pagination involved, to display threads ranked from
k to k+20 on the kth page would be an O(k) operation, which could get expensive
as the number of threads grow and if users frequently view pages where k is
large. However, as threads are sorted by their score, we assume that earlier pages
are more frequently accessed, compared to later pages. Thus even where n is large,
we are still more likely to access pages where k is relatively small. Under this
assumption, the linked list implementation is once again likely to outperform
a tree structure, where retrieval for any page requires O(log n) time.
