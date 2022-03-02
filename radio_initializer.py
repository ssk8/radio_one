import json
from pathlib import Path
from gtts import gTTS


"""
This was supposed to be a helper to get the radio set up, i.e., generate the JSON file and navigation mp3, so I wouldn't need to hard code them in. Instead the data is hardcoded here. Garbage. I've got some work to do
"""

radio_data_path = Path(__file__).parent.parent / "media"
radio_nav_path = radio_data_path / "navigation"
radio_data_file = radio_data_path / "radio_data.json"

if not radio_data_path.exists():
    radio_data_path.mkdir(parents=True)
    radio_nav_path.mkdir(parents=True)

    radio_data = [
        {"id": "startup" ,"nav_file": "startup.mp3", "nav_message": "starting radio now"},
        {"id": "shutdown_instruction" ,"nav_file": "shutdown_instruction.mp3", "nav_message": "push top button to shut radio down now"},
        {"id": "shutdown" ,"nav_file": "shutdown.mp3", "nav_message": "shutting down"},
        {"id": "Brian Eno Music For Airports" ,"nav_file": "bemfa.mp3", "nav_message": "Brian Eno Music For Airports", "media_path": str(radio_data_path / "Brian Eno Ambient 1 Music For Airports"), "station": "True"},
        {"id": "ambient sleeping pill" ,"nav_file": "asp.mp3", "nav_message": "ambient sleeping pill", "media_path": "https://radio.stereoscenic.com/asp-s", "station": "True"},
        {"id": "station two" ,"nav_file": "s2.mp3", "nav_message": "some other station", "media_path": "", "station": "True"}
    ]

    with open(radio_data_file, "w") as f:
        json.dump(radio_data, f)


with open(radio_data_file) as f:
    media_data = json.load(f)

print(media_data)
for file in media_data:
    id = file.get("id")
    nav_path = radio_nav_path / Path(file.get("nav_file"))
    nav_message = file.get("nav_message")
    gtts = gTTS(nav_message, lang='en')
    print(f"writing {nav_message}")
    gtts.save(nav_path)