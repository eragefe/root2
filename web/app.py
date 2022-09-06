from flask import Flask, flash, render_template, request, redirect
import subprocess
import os
import time

app = Flask(__name__)
app.debug = True


@app.route('/', methods = ['GET', 'POST'])
def index():
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return render_template('app.html', vol=vol, input=input, filter=filter)

@app.route("/volume2", methods = ['GET', 'POST'])
def volume2():
    if request.method == 'POST':
        a = request.form["c"]
        create_file(a)
        os.system('mpc volume $(cat /root/vol)> /dev/null 2>&1')
        with open("/root/vol", "r") as f:
             vol = f.read()
        return redirect('/')
    else:
        with open("/root/vol", "r") as f:
            vol = f.read()
            return vol

def create_file(a):
    temp_conf_file = open('/root/vol', 'w')
    temp_conf_file.write('' + a + '')
    temp_conf_file.close

@app.route("/volume", methods = ['GET', 'POST'])
def volume():
    if request.method == 'POST':
        a = request.form["a"]
        create_file(a)
        os.system('mpc volume $(cat /root/vol)> /dev/null 2>&1')
        with open("/root/vol", "r") as f:
                vol = f.read()
        return redirect('/')
    else:
        with open("/root/vol", "r") as f:
            vol = f.read()
            return vol

@app.route('/filter', methods = ['GET', 'POST'])
def filter():
    if request.method == 'POST':
        b = request.form["filter"]
        if b == "nos":
           os.system('amixer cset numid=5 1 >/dev/nul')
           os.system('echo "(N.O.S)" > /root/filter')
           os.system('systemctl restart volume')
        if b == "slow":
           os.system('amixer cset numid=5 0 >/dev/nul')
           os.system('amixer cset numid=4 1 >/dev/nul')
           os.system('echo "(Slow Rolloff)" > /root/filter')
           os.system('systemctl restart volume')
        if b == "fast":
           os.system('amixer cset numid=5 0 >/dev/nul')
           os.system('amixer cset numid=4 0 >/dev/nul')
           os.system('echo "(Fast Rolloff)" > /root/filter')
           os.system('systemctl restart volume')
        if b == "min":
           os.system('amixer cset numid=5 0 >/dev/nul')
           os.system('amixer cset numid=4 2 >/dev/nul')
           os.system('echo "(Minimal Phase)" > /root/filter')
           os.system('systemctl restart volume')
        return redirect('/')
    else:
        with open("/root/filter", "r") as f:
             filter = f.read()
             return filter

@app.route('/input', methods = ['GET', 'POST'])
def input():
    input = request.form["input"]
    if input == "S1":
         os.system('systemctl stop led')
         os.system('amixer cset numid=3 0 >/dev/nul')
         os.system('echo 0 >/sys/class/gpio/gpio65/value')
         os.system('echo "(spdif 1)" > /root/input')
    if input == "S2":
         os.system('systemctl stop led')
         os.system('amixer cset numid=3 0 >/dev/nul')
         os.system('echo 1 >/sys/class/gpio/gpio65/value')
         os.system('echo "(spdif 2)" > /root/input')
    if input == "i2s":
         os.system('systemctl stop led')
         os.system('amixer cset numid=3 1 >/dev/nul')
         os.system('echo "(i2s)" > /root/input')
    if input == "auto":
         os.system('systemctl start led')
         os.system('echo "(auto select)" > /root/input')
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/test', methods = ['GET', 'POST'])
def test():
    test = request.form["test"]
    if test == "channel":
        os.system('amixer cset numid=3 1 >/dev/nul')
        os.system('aplay -D plughw:0 /root/channel.wav')
        os.system('systemctl restart volume')
    if test == "phase":
        os.system('amixer cset numid=3 1 >/dev/nul')
        os.system('aplay -D plughw:0 /root/phase.wav')
        os.system('systemctl restart volume')
    if test == "net":
        os.system('bash /root/net')
        os.system('systemctl restart volume')
    if test == "sysupdate":
        return render_template('update.html')
    return redirect('/')

@app.route('/power')
def power():
    return render_template('power.html')

@app.route('/reboot', methods = ['GET', 'POST'])
def reboot():
    os.system('amixer cset numid=3 1 >/dev/nul')
    os.system('aplay -D plughw:0 /root/reboot.wav')
    os.system('systemctl restart volume')
    os.system('bash -c "sleep 1; reboot"&')
    return redirect('/')

@app.route('/update', methods = ['GET', 'POST'])
def update():
    os.system('bash -c "sleep 1; updateroot"&')
    return render_template('working.html'), {"Refresh": "4; url='/'"}

@app.route('/no', methods = ['GET', 'POST'])
def no():
    return redirect('/')

@app.route('/poweroff', methods = ['GET', 'POST'])
def poweroff():
    os.system('bash -c "sleep 1; poweroff"&')
    return redirect('/')

@app.route('/prev', methods = ['GET', 'POST'])
def prev():
    os.system('mpc prev')
    return redirect('/')

@app.route('/play', methods = ['GET', 'POST'])
def play():
    os.system('mpc toggle')
    return redirect('/')

@app.route('/stop', methods = ['GET', 'POST'])
def stop():
    os.system('mpc stop')
    return redirect('/')

@app.route('/next', methods = ['GET', 'POST'])
def next():
    os.system('mpc next')
    return redirect('/')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
