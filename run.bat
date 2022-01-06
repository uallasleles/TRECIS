@REM docker exec -it openalpr /bin/bash -c "export RTSP_SOURCE=rtsp://admin:1234@192.168.0.80:8554/h264_pcm.sdp"

docker exec -it openalpr /bin/bash -c "python /home/recognize.py"