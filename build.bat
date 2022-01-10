docker-compose up -d --build

@REM docker exec -it mongodb bash

@REM mongo -u coi -p 1234

@REM use carsdb

@REM db.createUser({user: 'alpruser', pwd: '1234', roles: [{role: 'readWrite', db: 'carsdb'}]})

@REM exit

@REM mongo -u alpruser -p 1234 --authenticationDatabase carsdb

@REM exit

@REM exit

@REM docker exec -it openalpr /bin/bash -c "export RTSP_SOURCE=rtsp://admin:1234@192.168.0.80:8554/h264_pcm.sdp"

@REM docker exec -it openalpr /bin/bash -c "python3 /home/recognize.py"

