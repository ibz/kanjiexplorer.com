docker run -d -e VIRTUAL_HOST=kanjiexplorer.com --network=webproxy --name=kanjiexplorer -e LETSENCRYPT_HOST=kanjiexplorer.com -e LETSENCRYPT_EMAIL=kanjiexplorer@ibz.me ibz0/kanjiexplorer.com
