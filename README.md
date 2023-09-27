# TwitchTTSBot
A Twitch bot that reads point redemptions.

## Dependencies

#### Anaconda

- Install anaconda and gcc
- Create the conda environment: `conda create -n tts python=3.9`, and then activate it with `conda activate tts`
- Install pyTorch (if you want to use GPU): `conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.7 -c pytorch -c nvidia -y`

#### RVC-based TTS

##### Install

- Get the repo: `git clone https://github.com/litagin02/rvc-tts-webui.git && cd rvc-tts-webui`
- Download the models: `curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt ; curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt`
- Install the dependencies: `python3 -m pip install -r requirements.txt`

If the install raises the error `Failed building wheel for pyworld`, run `python3 -m pip install numpy pyworld --no-build-isolation`

##### Get the model

- Train a RVC model
- Set the logs path (`<RVC path>/logs`) in the variable `model_root`, in `app.py`
- Copy the latest `.pth` file of the desired speaker from `<RVC path>/weights` into `<RVC path>/logs/<speaker>`

#### PythonTwitchBotFramework

##### Install

- Run `python3 -m pip install PythonTwitchBotFramework`

##### Creating the Twitch bot

- Create a Twitch account to be used as a bot
- [Create a new app](https://dev.twitch.tv/console/apps/create). Set a name, `Loyalty Tool` as category, and (if you don't want to use it) `http://localhost` as OAuth redirect

##### Config setup

The first time you run the script it will raise a token exception, and it will generate some config files.

You'll have to edit `config.json`:

- Remove all commands in `command_whitelist`; leave only `"command_whitelist": []`

#### Website audio player

TODO

##### Generating the SSL credentials

Inside the `TwitchTTSBot/` folder, run `openssl req -new -x509 -keyout key.pem -out server.pem -days 365 -nodes`.