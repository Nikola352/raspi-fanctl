# Raspberry Pi Fan Control – Setup & Usage

This setup lets you control your Raspberry Pi fan with **automatic temperature-based PWM** plus **manual override** via a simple command-line tool (`fanctl`).

---

## 1. Files in this project
- `fan_control.py` – Main Python script that runs as a systemd service and controls fan speed.
- `fanctl.bash` – Command-line utility for setting override mode or checking status.
- `fanctlcomplete` – bash completion script for `fanctl`.
- `fan_test.py` – Optional test script for experimenting with PWM manually.

---

## 2. Hardware requirements
- Raspberry Pi 4 (or compatible Pi)
- 2-wire, 3-wire, or 4-wire fan (PWM works best on low-current fans or via transistor/MOSFET)
- Fan connected to **BCM GPIO14** (Physical pin 8) for control, and GND for ground.

⚠️ **Warning:** Do not power high-current fans directly from GPIO. Use a transistor/MOSFET if fan draws more than ~30mA.

---

## 3. Installation

### 3.1 Install dependencies
```bash
sudo apt update
sudo apt install python3-gpiozero python3-rpi.gpio
```

### 3.2 Copy scripts to proper locations
```bash
sudo mkdir -p /opt/fan_control
sudo cp fan_control.py /opt/fan_control/fan_control.py
sudo chmod +x /opt/fan_control/fan_control.py

sudo cp fanctl.bash /usr/local/bin/fanctl
sudo chmod +x /usr/local/bin/fanctl

sudo cp fanctlcomplete /etc/bash_completion.d/fanctl
```

### 3.3 Enable bash completion
```bash
source /etc/bash_completion.d/fanctl
```

## 4. Systemd service setup
Create service file:
```bash
sudo nano /etc/systemd/system/fan-control.service
```

Paste:
```
[Unit]
Description=Raspberry Pi Fan Control Service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /opt/fan_control/fan_control.py
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fan-control.service
sudo systemctl start fan-control.service
```

Check status:
```bash
systemctl status fan-control.service
```

## 5. Usage

### 5.1 Automatic mode (temperature-based, default mode)
```bash
fanctl auto
```

### 5.2 Force fan ON (100% duty cycle)
```bash
fanctl on
```

### 5.3 Force fan OFF
```bash
fanctl off
```

### 5.4 Set custom duty cycle (0–100%)

This will keep the manually set duty cycle forever, unless you set it back to `"auto"`.

```bash
fanctl 40
```
(Example: 40% duty cycle)

### 5.5 Check current status
```bash
fanctl status
# or just:
fanctl
```

## 6. Autocomplete support

With `fanctlcomplete` installed and sourced, you can type:

```bash
fanctl [TAB]
```

and see:

```bash
auto  on  off  status
```

## 7. Notes

- The script writes `/tmp/fan_override` to store manual override state.
- The script writes `/tmp/fan_status` to store the last duty cycle and mode.
- If you need to stop fan control temporarily:
    ```bash
    sudo systemctl stop fan-control.service
    ```

## 8. Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 9. License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Nikola352/raspi-fanctl/blob/main/LICENSE) file for details.