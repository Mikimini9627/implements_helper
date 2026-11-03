if exist dist rmdir /s /q dist

uv build
uvx twine upload --repository pypi dist/*
