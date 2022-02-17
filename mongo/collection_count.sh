
mongo << EOF
use carsdb
db.auth('alpruser', '1234')
db.plate.count()
EOF