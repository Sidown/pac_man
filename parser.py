import json
import sys

from pydantic import BaseModel, ValidationError


class Config(BaseModel):
    """
    Pydantic model for the game configuration loaded from the json file.
    """
    highscore_filename: str
    lives: int
    level_max_time: int
    seed: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    levels: list[dict[str, int]]


def dict_raise_on_duplicate(pairs: list[tuple[str, str | int]]
                            ) -> dict[str, str | int]:
    """
    Build a dict from keys and values raising on duplicate keys.
    Used as the object_pairs_hook for json.load to reject
    a configuration file with two same keys.
    Arguments:
    pairs -> ordered list of key value tuples from the json parser
    return value:
    a dict built from pairs

    raise value error if a key appear more than once
    """
    d: dict[str, str | int] = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f'Double key: "{k}"')
        d[k] = v
    return d


def load_config(path: str) -> dict[str, str | int]:
    """
    Read and parse the json config file.
    Lines that beggin by '#' are ignored before parsing.
    Arguments:
    path -> path to the json config file
    return value:
    a dict with the type of config as a key and it's value as value

    Raise sys.exit on error on error
    """
    try:
        with open(path, "r") as f:
            lines = [line for line in f if not line.strip().startswith("#")]
            config = "".join(lines)

            if not config:
                raise ValueError("Config file empty")
            result: dict[str, str | int] = (
                json.loads(config, object_pairs_hook=dict_raise_on_duplicate)
                )
            return result

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
    """
    Check the config values.
    arguments:
    config -> the config parsed in the Config class
    Return value:
    true if ok, false in case of errors

    All detected errors are printed to stdout before
    returning a value
    """
    errors = []
    try:
        open(f"{config.highscore_filename}", "r")
    except FileNotFoundError:
        errors.append(f"File not found at {config.highscore_filename}")
    if config.lives <= 0:
        errors.append(f"Lives must be potive int (currently {config.lives})")
    if config.lives > 10:
        errors.append("No more than 10 lives !")
    if config.level_max_time <= 0:
        errors.append(
            "Level max time must be positive int (currently"
            f"{config.level_max_time})"
        )
    if config.points_per_pacgum <= 0:
        errors.append(
            "Points per pacgum must be positive int (currently "
            f"{config.points_per_pacgum})"
        )
    if config.points_per_super_pacgum <= 0:
        errors.append(
            "Point per super pacgum must be positive int"
            f"(currently {config.points_per_super_pacgum})"
        )
    if config.points_per_ghost <= 0:
        errors.append(
            "Points per ghost must be postivie int"
            f"(currently {config.points_per_ghost})"
        )
    if len(config.levels) < 10:
        errors.append(
            "The game must have at least 10 levels"
            f"(currently {len(config.levels)})"
        )
    for level in config.levels:
        if len(level) > 2:
            errors.append("A level must only contain a width and height")
        if len(level) < 2:
            errors.append("A level must have a width and a height key")
        try:
            if level["width"] <= 2:
                errors.append("The width of a level must be at least 3")
            if level["width"] > 20:
                errors.append("The width of a level should not be >20")
            if level["height"] <= 2:
                errors.append("The height of a level must be at least 3")
            if level["height"] > 20:
                errors.append("The height of a level should not be >20")
        except KeyError:
            errors.append("Level must have a width an height key")
    if errors:
        for error in errors:
            print(f"Error: {error}")
        return False
    return True


def parser(path: str) -> Config:
    """
    Load, parse and validate the game configuration from the json file
    Arguments:
    path -> path to the json configuration file
    return value:
    A validated Config class
    In case of error raise sys.exit
    """
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
