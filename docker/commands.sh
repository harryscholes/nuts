docker build -t nuts .

docker run -v $PWD:/home/volume -it harryscholes/nuts:latest
