#!/bin/bash

mongo <<EOF

# mongo -u coi -p 1234;
use admin;
db.auth('coi', '1234');

use carsdb;
db.createUser({user: 'alpruser', pwd: '1234', roles: [{role: 'readWrite', db: 'carsdb'}]});

EOF