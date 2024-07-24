micromamba create -n apply_room python==3.11.4
micromamba activate apply_room

pip install -e .
pip install pyinstaller

$ENV:PLAYWRIGHT_BROWSERS_PATH = 0
$ENV:HTTPS_PROXY = "http://127.0.0.1:7890"

playwright install chromium
pyinstaller --optimize 2 -y -D -n ApplyRoom src/applyroom/__main__.py