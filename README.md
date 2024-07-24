# applyRoom

apply a room from berklee with playwright

**For educational/personal use only!**

## Requirement

- python >= `3.10`
- playwright

# Installation

```bash
git clone https://github.com/mokurin000/applyRoom.git
cd applyRoom
pip install -e . # editable installation, if you want to patch source code
```

## Fill Cookies

- Goto [berklee onelogin](https://berklee.onelogin.com/), login with `Keep me signed in` checked.
- Press `Ctrl-SHift-I` or `F12`, to open devtool.

> click `>>` if `Application` was folded
- Open `Application` (or `Storage` for  firefox), click `Cookies`, `https://berklee.onelogin.com`
- Check the entry named `persistent`, copy it's `Value`.
- Copy `.env.example` to `.env`
- Paste the value after `APPLY_ROOM_PERSISTENT=`.

