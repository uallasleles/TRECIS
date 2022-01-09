@REM Executing task in folder TRECIS
docker-compose -f "docker-compose.yml" -p "trecis" stop

@REM Executing task in folder TRECIS
docker-compose -f "docker-compose.yml" -p "trecis" down

cmd /c "e:\GitHub\Awesome-Compose\wmb\TRECIS\build.bat"