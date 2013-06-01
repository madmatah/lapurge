import sys
import arguments
import purge


def main():
    try:
        args = arguments.parse()
        retval = purge.run(args)
        sys.exit(retval)
    except KeyboardInterrupt:
        sys.stderr.write('KeyboardInterrupt\nexiting ...\n')
        sys.exit(0)
    except Exception, info:
        sys.stderr.write("ERROR : %s\n" % info)
        sys.exit(1)
