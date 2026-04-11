# Twitch downloader

This repository contains an utility script (along side its needed files) to download VODs from specified streamers and getting updates on Discord.  
This project is possible thanks to the [twitch-dl](https://github.com/ihabunek/twitch-dl) python library, made by [Ivan Habunek](https://github.com/ihabunek). Please check out his work if you appreciate this repository.  

## Setup & Usage

1. Create a virtual environment `python -m venv ./venv/`
2. Activate the virtual environment `.\venv\Scripts\activate`
3. Install the required packages `python install -r requirements`
4. Create a `.env` file that match the template
5. Create a `streamers.json` file that match the template and fill it with your wanted streamer(s)
6. Run the script with `py main.py`
7. You may need further setup to make `twitch-dl` work, see the README of the project for more information

## Disclaimer

### Generative AI

Generative AI such as ChatGPT, Claude and other programs alike has been used alongside classic researchs to help writing some parts of the program.  
The parts concerned are the `StdoutWrapper` and the `DotDict` classes.  
No code was generated directly and just slammed in the files, the AIs only directed me in certain directions for my researchs.
Here's some helpful documentation used in the process of creating those classes:
- [\_\_getattr__ documentation](https://docs.python.org/3/library/functions.html#getattr)
- [\_\_setattr__ documentation](https://docs.python.org/3/library/functions.html#setattr)
- [\_\_delattr__ documentation](https://docs.python.org/3/library/functions.html#delattr)
- [redirecting stdout](https://blog.pythonlibrary.org/2016/06/16/python-101-redirecting-stdout/) - The class was created to keep the stdout being written properly while performing custom actions. The property and the isatty method were needed because twitch-dl use the [click library](https://click.palletsprojects.com/en/stable/) that needs such methods.

### Respect and legal awareness

While downloading things is cool, distributing outside of the wanted scope of the streamer can be disrespectful or even be straight up illegal. Please be mindful while using this script, or other similar tools.
