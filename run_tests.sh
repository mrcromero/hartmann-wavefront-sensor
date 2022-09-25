#!/bin/bash
BASEDIR=$(dirname $0)
for f in $BASEDIR/tests/*.py; do python "$f"; done