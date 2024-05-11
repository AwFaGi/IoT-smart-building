@REM for /L %%B in (0,1,5) do (
@REM     set DEVICE_INDEX=%%B && docker-compose up -d --build --scale 1 device
@REM )
@REM
@REM docker-compose up -d --build server

docker build . -t device -f ./device/Dockerfile && for /L %%B in (0,1,5) do (
    set DEVICE_INDEX=%%B && docker run -d device --name device%%B
)

docker build . -t server -f ./server/Dockerfile && docker run -d server
