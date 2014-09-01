#!/bin/sh
#
# Wrapper script to nosetests
#
# Usage: run_nose_tests.sh [nose options] test_modules...
#
# Wrapper script to run tests using nose.
#
# To run tests:
# [cd to minipylib package directory]
# ./bin/run_nose_tests.sh minipylib
#
# To print diagnostic info when running tests:
# ./bin/run_nose_tests.sh -D minipylib
#
#
# * created: 2014-08-28 Kevin Chan <kefin@makedostudio.com>
# * updated: 2014-09-01 kchan

########################################################################
myname="${0##*/}"
OLD_PWD=$PWD
cd $(dirname "$0")
mydir="${PWD%/}"
cd "$OLD_PWD"
########################################################################


########################################################################
# helper functions

verbose=0

usage()
{
    cat <<EOF
# Usage: $myname [nose options] test_modules...
# options:
#    -h | --help    # print usage and exit
#    -D             # print debug message during tests
#
# * any other options not listed above will pass to nose.
@
# Wrapper script to run tests using nose.
#
# To run tests:
# [cd to minipylib package directory]
# ./bin/run_nose_tests.sh minipylib
#
# To print diagnostic info when running tests:
# ./bin/run_nose_tests.sh -D minipylib
EOF
    exit 1
}

error()
{
    [ "$1" ] && printf >&2 "### %s\n" "$*"
    exit 1
}



########################################################################
# execute command

NOSETESTS=$(which nosetests)
if [ -z "$NOSETESTS" ]; then
    error "nosetests not found!"
fi

NOSE_OPTS="--nocapture --nologcapture --with-ignore-docstrings"

nose_opts="$NOSE_OPTS"
debug_msgs=0
modules=

while [ $# -gt 0 ]
do
    case "$1" in
        -D)
            debug_msgs=1
            ;;
        -\?|-h|-help|--help)
            usage
            ;;
        -*)
            nose_opts="$nose_opts $1"
            ;;
        *)
            modules="$modules $1"
            ;;
    esac
    shift
done


if [ $# -eq 1 ]; then
    { [ "$1" = "-h" ] || [ "$1" = "--help" ]; } && usage
fi

# run nosetests

cleanup()
{
    unset TEST_DEBUG
}
trap "cleanup" EXIT

if [ "$debug_msgs" -gt 0 ]; then
    export TEST_DEBUG=1
fi

"$NOSETESTS" \
    $nose_opts \
    $modules

cleanup
exit
