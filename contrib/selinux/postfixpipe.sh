#!/bin/bash

set -e
set -x

semodule -r postfixpipe || :
checkmodule -M -m -o postfixpipe.mod postfixpipe.te
semodule_package -o postfixpipe.pp -m postfixpipe.mod
semodule -i postfixpipe.pp

