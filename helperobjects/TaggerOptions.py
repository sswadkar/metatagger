from dataclasses import dataclass

@dataclass
class TaggerOptions():
    align = None
    include_model = False
    include_location = False
    include_cam_settings = False