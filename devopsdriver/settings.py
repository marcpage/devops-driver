#!/usr/bin/env python3


""" Settings that can be in files, environment, or on the command line 

    Settings can be set on the command line, environment, in the code, or in files.
    
    Priority order:
    - in code
    - command line
    - environment
    - files
    
    Files can be JSON or YAML.
    They must have .json, .yml, or .yaml extension.
    Files can be named after the file passed in (__file__) or "devopsdriver".
    All files named after the file passed in have priority over "devopsdriver".
    This allows for shared settings for multiple scripts as well as specific settings.
    Files can be in an OS-specific preferences location, a series of specified directories, 
        or next to the file passed in (__file__).
    This allows for secrets, keys, and tokens to be stored on the machine and not in the repo.
    
    The OS specific directories are:
    - macOS: ~/Library/Preferences/
    - Windows: %APPDATA%/
    - Linux: ~/.devopsdriver/
    
    You can have environment variable substitutions in the values in the files.
    For instance, you can specify:
    
    output: ${home}/reports
    
    The `${home}` will be replaced with the value of the HOME environment variable, if it exists.
    If the environment variable does not exist, no change is made.
    
    Use case 1: Secrets not in repo
        tokens, passwords, etc can be stored in <pref>/devopsdriver.yml
        This will allow for all scripts to access those secrets
            but they are not in the repo.
        For pipeline runs these secrets can be passed on the command line or in the environment.
    
    Use case 2: common settings among scripts
        Store your common settings in devopsdriver.yml next to your script.
        All scripts in this directory will have access to these settings.
        For instance, say you want all emails sent from the same person.
        You could set 'email: me@domain.com' in devopsdriver.html.
        You could also, store report paths, emails, groups, holidays, etc.
        Any data all scripts may want to have access to.
        
    Use case 3: configurable settings
        Any settings in your script that you may want to configure.
        If your script is `cool_script.py` then put the settings in `cool_script.yml` next to it.
        This could be colors, emails, repos, queries, whatever.
    
    Use case 4: override secrets for specific script
        Overriding secrets stored in <pref>/devopsdrive.yml for specific scripts.
        If your script is `cool_script.py` save them to <pref>cool_script.yml.
    
    *Note*: You can override a specific setting in a sub-dictionary.
    For instance, say <pref>/devopsdrive.yml:
    
    ```yaml
    api:
        user: johndoe
        password: Setec Astronomy
    ```
    
    You could override this for `cool_script.py` be adding <pref>cool_script.yml:
    
    ```yaml
    api:
        user: janedoe
    ```
    
    johndoe and janedoe share the same password, so you just need to update the `user`
"""


from json import load
from os.path import dirname, basename, splitext, join
from os import environ as os_environ, makedirs as os_makedirs
from re import compile as regex
from platform import system as os_system
from sys import argv as sys_argv
from getpass import getpass as os_getpass

from yaml import safe_load
from keyring import get_password, set_password
from keyring.backends import fail


# for testing
ENVIRON = os_environ
ARGV = sys_argv
SYSTEM = os_system
MAKEDIRS = os_makedirs
SHARED = "devopsdriver"
PRINT = print
GET_PASSWORD = get_password
SET_PASSWORD = set_password
GET_PASS = os_getpass


def load_json(path: str) -> dict:
    """Load a dictionary from a JSON file

    Args:
        path (str): Path to JSON file

    Returns:
        dict: The contents as a dictionary, or empty dictioanry if unable to load the file
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return load(file)

    except FileNotFoundError:
        return {}


def load_yaml(path: str) -> dict:
    """Load a dictionary from a JSON file

    Args:
        path (str): Path to JSON file

    Returns:
        dict: The contents as a dictionary, or empty dictioanry if unable to load the file
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return safe_load(file)

    except FileNotFoundError:
        return {}


class Settings:
    """Settings object"""

    FORMATS = ((".yml", load_yaml), (".yaml", load_yaml), (".json", load_json))
    DEFAULT_PREF_DIR = "Linux"
    PREF_DIR = {
        "Darwin": join(ENVIRON.get("HOME", ""), "Library", "Preferences"),
        "Windows": join(ENVIRON.get("APPDATA", "")),
        "Linux": join(ENVIRON.get("HOME", ""), ".devopsdriver"),
    }
    ENV_VAR_PATTERN = regex(r"\${(\S+)}")

    def __init__(self, file: str, *directories, **settings):
        """Create a settings object using a file, directories to search, and settings overrides

        Args:
            file (str): The basename to use and a directory to search. pass __file__
        """
        self.overrides = settings
        directories = [dirname(file), *directories, Settings.__preferences_dir()]
        search_info = Settings.__all_paths(file, directories)
        self.search_files = [join(d, n + e) for e, n, d, _ in search_info]
        self.settings = Settings.__find_all_settings(search_info)
        self.opts = {}
        self.environ = {}
        self.secrets = {}

    def __bypass(self, key: str, name: str, store: dict):
        if name is None:
            for setting_key, store_name in self.settings.get(key, {}).items():
                store[setting_key] = store_name
            return self

        store[key] = name
        return self

    def key(self, key: str, name: str = None):
        """Sets a keychain name to map to a settings value.

        Args:
            key (str): The settings key it maps to, dotted for inside dictionary
            name (str): Name of the keychain key
                            If name is not specified, the key is a settings value
                            to lookup up the mappings for keys to switches

        Returns:
            Settings: Returns self so you can chain calls
        """
        return self.__bypass(key, name, self.secrets)

    def cli(self, key: str, name: str = None):
        """Sets a command line switch to map to a settings value.

        Args:
            key (str): The settings key it maps to, dotted for inside dictionary
            name (str): Name of the command line switch, eg '-p' or '--path'
                            If name is not specified, the key is a settings value
                            to lookup up the mappings for keys to switches

        Returns:
            Settings: Returns self so you can chain calls
        """
        return self.__bypass(key, name, self.opts)

    def env(self, key: str, name: str = None):
        """Sets an environment variable to map to a settings value.

        Args:
            key (str): The settings key it maps to, dotted for inside dictionary
            name (str): Name of the environment variable
                            If name is not specified, the key is a settings value
                            to lookup up the mappings for keys to environment names

        Returns:
            Settings: Returns self so you can chain calls
        """
        return self.__bypass(key, name, self.environ)

    @staticmethod
    def __patch_instance(key: str) -> str:
        for env_key, value in ENVIRON.items():
            if env_key.lower() == key.lower():
                return value

        return "${" + key + "}"

    @staticmethod
    def __patch(value: any) -> any:
        if isinstance(value, str):
            return Settings.ENV_VAR_PATTERN.sub(
                lambda m: Settings.__patch_instance(m.group(1)), value
            )

        return value

    @staticmethod
    def split_key(key: str) -> tuple[str, str]:
        """Splits a keychain name into service and name

        Args:
            key (str): If there is a / then it is service/name
                        otherwise it is "system"/name

        Returns:
            tuple[str, str]: The service and name
        """
        parts = key.split("/", 1)
        assert len(parts) in {1, 2}, parts
        service = parts[0] if len(parts) == 2 else "system"
        secret_name = parts[1] if len(parts) == 2 else parts[0]
        return (service, secret_name)

    def __lookup(self, key: str, check: bool, default: any = None) -> any:
        # Settings passed in override everything
        if key in self.overrides:
            return True if check else self.overrides[key]

        # Settings on the command line take next precedence
        if key in self.opts:
            for nth, name in enumerate(ARGV[1:]):
                if name.lower() == self.opts[key].lower() and nth + 2 < len(ARGV):
                    return True if check else ARGV[nth + 2]

        # Settings in the environment are next
        if key in self.environ:
            for e_key in ENVIRON:
                if e_key.lower() == self.environ[key].lower():
                    return True if check else ENVIRON[e_key]

        # Settings in the keychain are next
        if key in self.secrets:
            value = GET_PASSWORD(*Settings.split_key(self.secrets[key]))

            if value is not None and not isinstance(value, fail.Keyring):
                return True if check else value

        # Last check the files for settings
        keys = key.split(".")
        level = self.settings

        for key_part in keys[:-1]:
            level = level.get(key_part, {})

        if check:
            return keys[-1] in level

        return Settings.__patch(level.get(keys[-1], default))

    def get(self, key: str, default: any = None) -> any:
        """Dictionary-like get

        Args:
            key (str): The key to load, dotted format
            default (any, optional): The value to return if there is no value. Defaults to None.

        Returns:
            any: The value or `default` if not found
        """
        return self.__lookup(key, check=False, default=default)

    def has(self, key: str) -> bool:
        """Check if the key exists in any of the environments

        Args:
            key (str): The dotted key

        Returns:
            bool: True if the key exists
        """
        return self.__lookup(key, check=True)

    def __contains__(self, key: str) -> bool:
        return self.has(key)

    def __getitem__(self, key: str) -> any:
        if not self.has(key):
            raise KeyError(key)

        return self.get(key)

    @staticmethod
    def __preferences_dir() -> str:
        default_dir = Settings.PREF_DIR[Settings.DEFAULT_PREF_DIR]
        directory = Settings.PREF_DIR.get(SYSTEM(), default_dir)
        MAKEDIRS(directory, exist_ok=True)
        return directory

    @staticmethod
    def __merge(base: dict, new: dict):
        """Add new information to an existing dictionary, if it doesn't already exist.
            If new has keys that base doesn't, they are added.
            If new has a key that base does and they both are dictionaries, they are merged.

        Args:
            base (dict): The is the existing values to add to
            new (dict): The new values to possible add
        """
        for key in new:
            if key not in base:
                base[key] = new[key]
                continue

            if isinstance(base[key], dict) and isinstance(new[key], dict):
                Settings.__merge(base[key], new[key])

    @staticmethod
    def __all_paths(file: str, directories: list[str]) -> list[tuple]:
        names = [splitext(basename(file))[0], SHARED]
        return [
            (e, n, d, f)
            for n in names
            for d in directories
            for e, f in Settings.FORMATS
        ]

    @staticmethod
    def __find_all_settings(search_info: list[tuple]) -> dict:
        settings = {}

        for extension, name, directory, loader in search_info:
            contents = loader(join(directory, name + extension))
            Settings.__merge(settings, contents)

        return settings
