###
### daemon_helper.py
###
#
# Helps with the process of starting and stopping daemons described in
# config/daemons.py

import sys
import Settings
sys.path.insert(0, Settings.CONFIG_PATH)

import subprocess
import time
import os.path

import daemons_config

arguments = sys.argv[1:]

command = arguments[0] if arguments else 'help'

def get_config_name() :
    if len(arguments) > 1 :
        return arguments[1]
    else :
        print 'Using configuration "default" by default.'
        return "default"

def get_config() :
    config_name = get_config_name()
    try :
        config = daemons_config.configurations[config_name]
    except KeyError :
        print 'Missing configuration named "%s"' % config_name
        sys.exit(1)
    return config

def start() :
    config = get_config()
    make_payments = True
    for port in config.ports :
        print "** Starting on port %s **" % port
        command = ["python", "app.py",
                   "--db_name=%s" % config.db_name,
                   "--environment=%s" % config.environment,
                   "--port=%s" % port,
                   "--make_payments=%s" % make_payments,
                   "--daemonize=True"]
        print " ".join(command)
        subprocess.check_call(command)
        time.sleep(1)
        make_payments = False

def stop() :
    import pid
    import Settings
    config = get_config()
    for port in config.ports :
        print "** Stopping port %s **" % port
        pidfile_path = os.path.join(Settings.PIDFILE_PATH, '%d.pid' % port)
        pid.check(pidfile_path)
        pid.remove(pidfile_path)

def drop() :
    config = get_config()
    print 'This will drop database "%s".' % config.db_name
    resp = raw_input("Are you sure you want to drop the database? (yes/no) ")
    if resp != "yes" :
        print "Not dropping."
        return
    print "** Dropping %s **" % config.db_name
    command = ["python", "app.py",
               "--drop=REALLYREALLY",
               "--db_name=%s" % config.db_name,
               "--make_payments=False"]
    print " ".join(command)
    subprocess.check_call(command)

if command == "start" or command == "restart" :
    start()
elif command == "stop" :
    stop()
elif command == "drop" :
    stop()
    drop()
elif command == "list" :
    for name, config in daemons_config.configurations.iteritems() :
        print "*** %s ***" % name
        print "  ports: %r" % config.ports
        print "  db_name: %s" % config.db_name
        print "  environment: %s" % config.environment
else :
    print "Usage: daemons start|stop|drop|help [configuration-name]"
    print
    print "Controls daemons described in config/daemons.py"
    print "The default configuration is 'default' if no configuration is supplied."
    print
    print "Commands:"
    print " start   - starts or restarts configuration-name"
    print " stop    - stops configuration-name"
    print " restart - a synonym for 'start'"
    print " drop    - drops the database for configuration-name"
    print " list    - list available configurations"
    print " help    - prints this message"
