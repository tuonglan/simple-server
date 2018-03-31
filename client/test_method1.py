import requests, os, random, string
from threading import Thread, Lock
from datetime import datetime


def _random_str(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def callback1(th_index, elapse, response):
    print "Thread %03d: Server responded in %3.3f seconds with message: %s" % (
                th_index, elapse, r.text)

def callback2(th_index, elapse, response):
    fname = "/tmp/sample_%s.jpg" % _random_str(7)
    try:
        start_tv = datetime.utcnow()
        with open(fname, 'wb') as sout:
            sout.write(response.content)
        save_time = (datetime.utcnow() - start_tv).total_seconds()
        print "Thread %03d: Server return in %3.3f, file name: %s, size: %s, save time: %3.6f" % (
                    th_index, elapse, fname, os.path.getsize(fname), save_time)
    finally:
        if os.path.isfile(fname):
            os.remove(fname)


def request_thread(api, is_verbose, count, th_index, response_times, callback):
    for i in range(0, count):
        start_tv = datetime.utcnow()
        r = requests.get(api)
        end_tv = datetime.utcnow()
        elapse = (end_tv - start_tv).total_seconds()
        callback(th_index, elapse, r)
        response_times[th_index] += elapse


def test(api, is_verbose, conc, req_num, callback):
    response_times = [0 for i in range(0, conc)]
    threads = [Thread(target=request_thread, args=(api, is_verbose, req_num, i, response_times, callback, ))
               for i in range(0, conc)]
    for th in threads: th.start()
    for th in threads: th.join()
    print "\t\t-----------------"
    for i in range(0, conc):
        print "Thread %03d has average response time: %3.3f seconds" % (i, response_times[i]/req_num)


def test1(api, is_verbose, conc, req_num):
    test(api, is_verbose, conc, req_num, callback1)

def test2(api, is_verbose, conc, req_num):
    test(api, is_verbose, conc, req_num, callback2)
