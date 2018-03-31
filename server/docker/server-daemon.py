import subprocess, time
from argparse import ArgumentParser

SLEEP_TIME = 60


def update_cluster(fin, fout, port_start, port_end):
    with open(fin, 'r') as sin:
        data = sin.read()

    servers_str = reduce(lambda x,y: x+"\n    server 127.0.0.1:%s;" % y, range(port_start+1, port_end+1),
                         "server 127.0.0.1:%s;" % port_start)
    data = data.replace('<%Clusters%>', servers_str)

    with open(fout, 'w') as sout:
        sout.write(data)
        


if __name__ == '__main__':
    # Parser the argument
    parser = ArgumentParser()
    parser.add_argument('--port_range', type=str, default='8888:8888', 
                        help='Select port range for listening')
    parser.add_argument('--update_nginx', action='store_true', help='Update nginx before start processes')
    args = parser.parse_args()
    ports = args.port_range.split(':')
    port_start, port_end = (int(ports[0]), int(ports[1]))

    # Update nginx file
    if args.update_nginx:
        update_cluster('nginx_frontend_template.com', 
                       '/etc/nginx/sites-enabled/sample-server_frontend.com', port_start, port_end)

        # Restart nginx
        try:
            subprocess.check_output(['service', 'nginx', 'restart'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print "Can't restart nginx: %s" %e
            import sys
            sys.exit(-1)
        except Exception as e:
            print "Error when restarting nginx: %s" % e
            import sys
            sys.exit(-1)

    # Generate subprocesses
    procs = [subprocess.Popen(['python', 'sample-server.py', '--port', "%s" % i]) 
             for i in range(port_start, port_end+1)]

    # Periodically check if any process has been killed, restart it
    while True:
        try:
            print "Server Daemon: checking processes' status"
            idx = 0
            for proc in procs:
                poll = proc.poll()
                if poll != None:
                    print "Process %s stopped: %s, try to restart it now" % (proc, poll)
                    print "Restarting: \"python sample-server.py --port %s\"" % (idx+port_start)
                    try:
                        procs[idx] = subprocess.Popen(['python', 'sample-server.py', '--port', "%s" % (idx+port_start)])
                    except Exception as e:
                        print "Can't restart process: %s" % e
                        raise Exception("Can't restart: \"python sample-server.py --port %s\n" % (idx_port_start))
                idx += 1
            time.sleep(SLEEP_TIME)
        except (KeyboardInterrupt, Exception) as e:
            print "Sample Server stops due to: %s..." % e
            for proc in procs:
                if proc.poll() == None:
                    proc.kill()
                    proc.wait()
            break
        
    print "Sample Server stopped"
