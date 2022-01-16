1. Build the "builder" image

   ```docker build . --file Dockerfile.builder --tag kanjiexplorer-builder```
1. Use the "builder" image to generate files

   ```docker run -v $(pwd)/takadb:/taka -v $(pwd)/web:/web kanjiexplorer-builder /builder/taka_to_web.sh```

1. Serve `/web` in any way you want (nginx, GitHub Pages, ...)
