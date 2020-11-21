docker stop kanjiexplorer.com
docker container rm kanjiexplorer.com
docker run -d -e VIRTUAL_HOST=kanjiexplorer.com --network=webproxy --name=kanjiexplorer.com -e LETSENCRYPT_HOST=kanjiexplorer.com -e LETSENCRYPT_EMAIL=kanjiexplorer@ibz.me ibz0/kanjiexplorer.com
