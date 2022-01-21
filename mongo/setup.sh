#!/bin/bash

mongo <<EOF

mongo -u coi -p 1234;
use carsdb;
db.createUser({user: 'alpruser', pwd: '1234', roles: [{role: 'readWrite', db: 'carsdb'}]});

EOF

mongo -u alpruser -p 1234 --authenticationDatabase carsdb