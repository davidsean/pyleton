# pyleton
speed tracker using repurposed reed switch.


# Quick start

Install requirements
```bash
pip install -r requirements.txt
```

Download demo track
```bash
wget -O track.mp3 https://freemusicarchive.org/track/holle-mangler-next-exit-nowhere-frau-holle-remix/download 
```

Start
```bash
python -m pyleton
```

# Hookup
Connect the reed switch to physical pins 39 (`GND`) and 40 (wiring pi `29` / `GPIO_21`). Get this right, if you mistakingly plug `3v3` to `5v`, you may blow up your pi. See orientation diagram in (pinout.xyz)[pinout.xyz].
You can use differnt pins if you know what you are doing, make sure to modify the code).

# Dev


activate venv
```bash
source pyleton-venv/bin/activate
```

