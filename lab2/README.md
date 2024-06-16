# Самостоятельная работа 2

### Usage


`docker build . -t mtu_finder`

`docker run --network host --rm mtu_finder`

```
usage: ./MTUFinder <hostname>

positional arguments:
  hostname

options:
  -h, --help            show this help message and exit
  --count COUNT, -c COUNT
                        Number of packets > 0, host is considered reachable if
                        at least one packet reaches.
  --verbose, -v         Enable aditional output
```

`docker run --network host --rm mtu_finder 123`

```
<hostname> must be a valid hostname, value given: 123
```


`docker run --network host --rm mtu_finder google.com`

```
MTU to google.com is 1480
```

`docker run --network host --rm mtu_finder 8.8.8.8 -v`

```
MTU >= 784
MTU >= 1142
MTU >= 1321
Host 8.8.8.8 was not reached, trying again
Host 8.8.8.8 was not reached, trying again
MTU >= 1411
Host 8.8.8.8 was not reached, trying again
MTU >= 1456
Host 8.8.8.8 was not reached, trying again
Host 8.8.8.8 was not reached, trying again
MTU >= 1478
Host 8.8.8.8 was not reached, trying again
Host 8.8.8.8 was not reached, trying again
MTU < 1489
Host 8.8.8.8 was not reached, trying again
Host 8.8.8.8 was not reached, trying again
MTU < 1483
Host 8.8.8.8 was not reached, trying again
MTU >= 1480
Host 8.8.8.8 was not reached, trying again
Host 8.8.8.8 was not reached, trying again
MTU < 1481
MTU to 8.8.8.8 is 1480
```