#!/bin/bash

cd /usr/share/indextank-engine
exec java -cp target/indextank-engine-1.0.0-jar-with-dependencies.jar com.flaptor.indextank.api.Launcher < /dev/null > /tmp/indextank-engine.log 2>&1 &
