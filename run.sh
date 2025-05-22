if ! command -v uv &> /dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh

  sudo apt-get update
  sudo apt-get install -y poppler-utils
fi
uv sync
uv pip install -e . --no-cache-dir
nohup uv run cg-api >> run.log 2>&1 &
