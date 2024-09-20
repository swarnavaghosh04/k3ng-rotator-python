# K3NG Rotator Python Controller
A Python wrapper for controlling a [K3NG Rotator Controller](https://github.com/k3ng/k3ng_rotator_controller) over serial/USB. 
This code has a specific bend towards satellite control, as the primary use for us is tracking the [HERON MkII](https://heron.utat.space/) satellite. 

## Installing
Dependencies are managed by `poetry`: `poetry install` to get 'em all. 
Poetry automatically creates a venv instead of installing globally, this is usually a good thing!
For most stuff, this is all you need. 

If, for whatever reason, you need this available globally, you *can* run `pip3 install . --break-system-packages`, but this carries risks as the command implies. 

To install development dependencies, use `poetry install --with=dev`

## Usage
See `/examples` for various ways to control the rotator. 
It may be useful to use `udev` rules to always map the Arduino connected to the rotator to a more meaningful serial devices (such as `/dev/ttyRotator`), especially if you have multiple serial devices which can change designators across boot. 
In my experience, the Arduino can be pretty finicky around its serial connection and not constantly resetting -- tweak the `SEND_DELAY` and `RECV_DELAY` variables in `k3ng.py` if you're having issues with that.

For testing and development, the usage of `ipython` is reccomended. 
There is a useful starter script located in `/examples` that can help you get started: `ipython3 -i ipython_start.py /dev/tty12345`

Please note: each time a script is run and a new `K3NG` object is instantiated, the Arduino will reset! 
This will lose the current time, stored state, and stored TLEs. 
This is a limitation of Arduinos, not this script; generally this is considered a feature but clearly there are some downsides.

## RPC
In some cases, it may be useful to have a single persistent serial connection to avoid the aforementioned resets whenever a new connection is created. 
For that reason, this repo provides the ability to run a RPC server as a service on Linux machines. 

To install the script, you can use the `install.sh` script in the `/rpc_daemon` directory. 
Be warned, it's a pretty risky script with few safeguards and assumes a somewhat specific configuration. 
Use at your own risk! 

The service installs itself as `k3ng_rotator`, and can be checked on using `sudo systemctl status k3ng_rotator`. 
By default, it tries to connect to `/dev/ttyRotator`, and binds to port `18866`. 

Using it in this remote state is designed to be plug and play with standard local usage. 
Instead of calling something like `rot = K3NG("/dev/ttyRotator")`, instead create an RPC connection:

```python
import rpyc
rot = rpyc.connect("localhost", args.rpc_port).root.K3NG
```

Once initialized in this way, the K3NG object is exactly the same as if it was running locally, but `rpyc` will be handling back-and-forth behind the scenes. 
Pretty neat!
(ok, not exactly the same, for example tab completion doesn't work quite right currently...)

Again, for development, it is useful to use `ipython`, and in `/examples` there is another helper script for RPC environments: `ipython3 -i ipython_start_rpc.py`

## Contributing
Issues and PRs are always welcome! 
If contributing code, please first run the linting + style suite as follows: `isort . && black . && flake8 . && mypy .`. 
