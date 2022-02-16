#!/bin/bash

mongo << EOF
use admin
db.auth({user: "coi", pwd: "1234"})
use carsdb
db.createUser({
    user: "alpruser",
    pwd: "1234", 
    roles: [{
        role: "readWrite", 
        db: "carsdb"
        }]
    })
exit
mongo "mongodb://127.0.0.1:27017" --username ${MONGODB_USERNAME} --password  ${MONGODB_PASSWORD} --authenticationDatabase ${MONGODB_DATABASE}
EOF