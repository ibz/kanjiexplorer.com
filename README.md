# Kanji Explorer

To use Kanji Explorer you don't need to download or build anything. Simply go to [kanjiexplorer.com](http://kanjiexplorer.com) and have fun.

This repository contains the source code, the build scripts, as well as a copy of [the Taka database](http://taka.sourceforge.net/).

Feel free to download, study or modify the files in this repository in any way you want. If you make any improvements, you can contribute back by sending a [Pull Request on GitHub](https://github.com/ibz/kanjiexplorer.com/pulls).

## How it works

* The Taka Database contains all the data about the characters, in XML format.
* When a new commit is pushed to this repository, a GitHub workflow is run.
* The XML data is parsed and used to generate `.json` and `.svg` files needed for the web interface. These files are saved under `web/`.
* The `web/` directory (which now includes the Taka database in `.json` and `.svg` formats) is passed to a Jekyll builder and the output is then deployed to GitHub Pages.
