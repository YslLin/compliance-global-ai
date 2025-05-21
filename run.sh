if ! command -v uv &> /dev/null; then
  pip install --upgrade pip
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
uv sync
uv pip install -e . --no-cache-dir
nohup uv run cg-api >> run.log 2>&1 &
