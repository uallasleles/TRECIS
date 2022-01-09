#!/usr/bin/env bash

echo "Setting up mongo user"

echo $MONGO_INITDB_ROOT_USERNAME
echo $MONGO_INITDB_ROOT_PASSWORD

set -eu
mongo -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var user    = '$MONGODB_USERNAME';
    var pwd     = '$MONGODB_PASSWORD';
    db.createUser({user: user, pwd: pwd, roles: [{role: 'readWrite', db: '$MONGODB_DATABASE'}]});
EOF

