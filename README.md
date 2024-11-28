This tool can be used to measure the speed of TCP data transfer using [mirrord](https://github.com/metalbear-co/mirrord).

### Usage

System prerequisites:

- IDE: VSCode
- run config: default VSCode "run and debug"
- mirrord: VSCode plugin
- cluster: local docker-desktop
- server image: [tcp-echo image from test-images repo](https://github.com/metalbear-co/test-images/pkgs/container/mirrord-tcp-echo)
- deployment: `kubectl apply -f ./timing.yaml`
- [mirrord config](/.mirrord/mirrord.json): use to explicitly enable or disable operator (make sure operator is installed)
- [script](/tcp-client.py): python script that measures time elapsed from starting to send bytes to the socket to finished receiving the reply from the server
	- prints speed in bytes per second
	- also prints average speed over all tests in `multi_test()` function

Steps to reproduce:

- choose which tests to run (you can run them multiple times) by invoking `single_test()` and/or `multi_test()` at the bottom of `tcp-client.py`
- measuring mirrord
	- set `"operator": false/true` and `"target": "deployment/tcp-echo-deployment"` in the config file
	- ensure that `PORT` is set to 80 in `tcp-client.py`
	- enable mirrord
	- hit F5/ run debug mode
	- record results (optional: repeat with `"operator": true/false`)
- measuring kubectl port-forward
	- ensure that `PORT` is set to 8009 in `tcp-client.py` (or any unused port)
	- run `k port-forward deployment/tcp-echo-deployment 8009:80`
	- disable mirrord
	- hit F5/ run debug mode
	- record results

### Improvements
- [ ] Print in more sensible units (kilobytes, milliseconds)
- [ ] Output results as .csv
- [ ] Wrapper script that runs all three tests automatically