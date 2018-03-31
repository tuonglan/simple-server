from argparse import ArgumentParser

import test_method1 as TM1

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--addr', type=str, default='http://lando.sytes.net', help='Server domain name/ip address')
    parser.add_argument('--port', type=int, default=8888, help='Server port number')
    parser.add_argument('--end_point', type=str, default='status', help='API Endpoint')
    parser.add_argument('--verbose', action='store_true', help='Print verbosity')
    parser.add_argument('--conc', type=int, default=1, help='Number of concurrent requests')
    parser.add_argument('--req_num', type=int, default=1, help='Number of requests')
    parser.add_argument('--test_mode', type=str, default='STATUS', choices=['STATUS', 'FILE'], 
                        help='Select the mode of testing')
    args = parser.parse_args()

    if args.test_mode == 'STATUS':
        TM1.test1("%s:%s/%s" % (args.addr, args.port, args.end_point), args.verbose,
                  args.conc, args.req_num)
    elif args.test_mode == 'FILE':
        TM1.test2("%s:%s/test/file" % (args.addr, args.port), args.verbose, args.conc, args.req_num)
        
