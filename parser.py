import json
import sys
from pydantic import BaseModel, ValidationError

class Config(BaseModel):
    highscore_filename: str
    lives: int
    level_max_time: int
    seed: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    levels: list[dict[str, int]]


def dict_raise_on_duplicate(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f'Double key: "{k}"')
        d[k] = v
    return d


def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            lines = [line for line in f if not line.strip().startswith('#')]
            config = "".join(lines)

            if not config:
                raise ValueError("Config file empty")
            return json.loads(config, object_pairs_hook=dict_raise_on_duplicate)
        
    except json.JSONDecodeError:
        print("Error: JSON not valid")
        sys.exit()
    
    except FileNotFoundError:
        print(f"File {path} not found")
        sys.exit()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit()


def config_check(config: Config) -> bool:
    errors = []
    try:
        open(config.highscore_filename, 'r')
    except FileNotFoundError:
        errors.append(f"File not found at {config.highscore_filename}")
    if config.lives <= 0:
        errors.append(f"Lives must be potive int (currently {config.lives})")
    if config.level_max_time <= 0:
        errors.append(f"Level max time must be positive int (currently {config.level_max_time})")
    if config.points_per_pacgum <= 0:
        errors.append(f"Points per pacgum must be positive int (currently {config.points_per_pacgum})")
    if config.points_per_super_pacgum <= 0:
        errors.append(f"Point per super pacgum must be positive int (currently {config.points_per_super_pacgum})")
    if config.points_per_ghost <= 0:
        errors.append(f"Points per ghost must be postivie int (currently {config.points_per_ghost})")
    if len(config.levels) < 10:
        errors.append(f"The game must have at least 10 levels (currently {len(config.levels)})")
    for level in config.levels:
        if len(level) > 2:
            errors.append("A level must only contain a width and height")
        if len(level) < 2:
            errors.append("A level must have a width and a height key")
        try:
            if level['width'] <= 0:
                errors.append("The width of a level must be postive int")
            if level['height'] <= 0:
                errors.append("The height of a level must be positive int")
        except KeyError:
            errors.append("Level must have a width an height key")
    if errors: 
        for error in errors:
            print(f"Error: {error}")
        return False
    return True
    


def parser(path: str) -> Config:
    try:
        config = Config(**load_config(path))
        if config_check(config):
            return config
        else:
            sys.exit()

    except ValidationError as e:
        print(f"Error: {e}")
        sys.exit()
    except TypeError as e:
        print(f"Error: {e}")
        sys.exit()




test = parser("./config.json")
print(test)
