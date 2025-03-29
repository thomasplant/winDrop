# winDrop


## How to run
If your in any system you can run winDrop form any of the files which specify the type.

To run inside of our testing docker containers run in WSL2

```export DISPLAY=$(echo $DISPLAY)```

```docker-compose up --build```

Note: if your on mac you may need to use 

```DISPLAY=host.docker.internal:0```


After the first time running there is no need to perform the export command.

