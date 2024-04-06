#!/usr/bin/env python3

""" Tests Settings class """

from tempfile import TemporaryDirectory
from os.path import join
from string import ascii_lowercase
from itertools import product

from helpers import setup_settings, ensure, write

from devopsdriver import settings  # debug access
from devopsdriver.settings import Settings


def __setup_files(directory: str, dir1: str, dir2: str) -> None:
    """
    Priorities:
        <dir>/main.yml a
        <dir>/main.yaml b
        <dir>/main.json c
        <dir1>/main.yml d
        <dir1>/main.yaml e
        <dir1>/main.json f
        <dir2>/main.yml g
        <dir2>/main.yaml h
        <dir2>/main.json i
        <pref>/main.yml j
        <pref>/main.yaml k
        <pref>/main.json l
        <dir>/test.yml m
        <dir>/test.yaml n
        <dir>/test.json o
        <dir1>/test.yml p
        <dir1>/test.yaml q
        <dir1>/test.json r
        <dir2>/test.yml s
        <dir2>/test.yaml t
        <dir2>/test.json u
        <pref>/test.yml v
        <pref>/test.yaml w
        <pref>/test.json x
    """
    lin_dir = ensure(Settings.PREF_DIR["Linux"])
    mac_dir = ensure(Settings.PREF_DIR["Darwin"])
    win_dir = ensure(Settings.PREF_DIR["Windows"])
    letters = list(ascii_lowercase)

    for name in ("test", "main"):
        for letter, os_dir in (("l", lin_dir), ("w", win_dir), ("m", mac_dir)):
            write(
                join(os_dir, "test.json"),
                **{l: f"{name[0]}{letter}{l}" for l in letters},
                dp={l: f"{name[0]}{letter}{l}" for l in letters},
            )

        letters.pop()

    for directory, name, ext in product(
        (dir2, dir1, directory), ("test", "main"), (".json", ".yaml", ".yml")
    ):
        write(
            join(directory, name + ext),
            **{l: f"{directory[-1]}{ext[2]}{name[0]}{letter}{l}" for l in letters},
            dp={l: f"{directory[-1]}{ext[2]}{name[0]}{letter}{l}" for l in letters},
        )
        letters.pop()


def test_basic():
    """test the basic functionality"""
    with TemporaryDirectory() as working_dir:
        base_dir = join(working_dir, "base")

        for os in ("Linux", "Darwin", "Windows", "Unknown"):
            setup_settings(
                os=os,
                shared="test",
                Linux=join(base_dir, "Linux"),
                Darwin=join(base_dir, "macOS"),
                Windows=join(base_dir, "Windows"),
            )
            dir1 = join(base_dir, "dir1")
            dir2 = join(base_dir, "dir2")

            __setup_files(base_dir, dir1, dir2)
            settings.ENVIRON = {
                "alpha": "aaenviron",
                "yota": "yyenviron",
                "zeta": "zzenviron",
            }
            settings.ARGV = ["exe", "--beta", "bbcli", "--zeta", "zzcli"]
            opts = (
                Settings(join(base_dir, "main.py"), dir1, dir2, aa=1, bb=2, cc=3)
                .cli("bb", "--beta")
                .cli("zz", "--zeta")
                .env("aa", "alpha")
                .env("yy", "yota")
            )
            ltr = {"Linux": "l", "Darwin": "m", "Windows": "w", "Unknown": "l"}
            assert opts["yy"] == "yyenviron", opts["yy"]
            assert opts["aa"] == 1, f"{opts['aa']} {os}"
            assert opts["bb"] == 2, f"{opts['bb']} {os}"
            assert opts["cc"] == 3, f"{opts['cc']} {os}"
            assert opts["zz"] == "zzcli", opts["zz"]
            assert opts["a"] == "emmma", f"{opts['a']} {os}"
            assert opts["dp.a"] == "emmma", f"{opts['dp.a']} {os}"
            assert opts["b"] == "emmmb", f"{opts['b']} {os}"
            assert opts["dp.b"] == "emmmb", f"{opts['dp.b']} {os}"
            assert opts["c"] == "emmmc", f"{opts['c']} {os}"
            assert opts["dp.c"] == "emmmc", f"{opts['dp.c']} {os}"
            assert opts["d"] == "emmmd", f"{opts['d']} {os}"
            assert opts["dp.d"] == "emmmd", f"{opts['dp.d']} {os}"
            assert opts["e"] == "emmme", f"{opts['e']} {os}"
            assert opts["dp.e"] == "emmme", f"{opts['dp.e']} {os}"
            assert opts["f"] == "emmmf", f"{opts['f']} {os}"
            assert opts["dp.f"] == "emmmf", f"{opts['dp.f']} {os}"
            assert opts["g"] == "emmmg", f"{opts['g']} {os}"
            assert opts["dp.g"] == "emmmg", f"{opts['dp.g']} {os}"
            assert opts["h"] == "eammh", f"{opts['h']} {os}"
            assert opts["dp.h"] == "eammh", f"{opts['dp.h']} {os}"
            assert opts["i"] == "esmmi", f"{opts['i']} {os}"
            assert opts["dp.i"] == "esmmi", f"{opts['dp.i']} {os}"
            assert opts["j"] == "1mmmj", f"{opts['j']} {os}"
            assert opts["dp.j"] == "1mmmj", f"{opts['dp.j']} {os}"
            assert opts["k"] == "1mmmk", f"{opts['k']} {os}"
            assert opts["dp.k"] == "1mmmk", f"{opts['dp.k']} {os}"
            assert opts["l"] == "1mmml", f"{opts['l']} {os}"
            assert opts["dp.l"] == "1mmml", f"{opts['dp.l']} {os}"
            assert opts["m"] == "1mmmm", f"{opts['m']} {os}"
            assert opts["dp.m"] == "1mmmm", f"{opts['dp.m']} {os}"
            assert opts["n"] == "1ammn", f"{opts['n']} {os}"
            assert opts["dp.n"] == "1ammn", f"{opts['dp.n']} {os}"
            assert opts["o"] == "1smmo", f"{opts['o']} {os}"
            assert opts["dp.o"] == "1smmo", f"{opts['dp.o']} {os}"
            assert opts["p"] == "2mmmp", f"{opts['p']} {os}"
            assert opts["dp.p"] == "2mmmp", f"{opts['dp.p']} {os}"
            assert opts["q"] == "2mmmq", f"{opts['q']} {os}"
            assert opts["dp.q"] == "2mmmq", f"{opts['dp.q']} {os}"
            assert opts["r"] == "2mmmr", f"{opts['r']} {os}"
            assert opts["dp.r"] == "2mmmr", f"{opts['dp.r']} {os}"
            assert opts["s"] == "2mmms", f"{opts['s']} {os}"
            assert opts["dp.s"] == "2mmms", f"{opts['dp.s']} {os}"
            assert opts["t"] == "2ammt", f"{opts['t']} {os}"
            assert opts["dp.t"] == "2ammt", f"{opts['dp.t']} {os}"
            assert opts["u"] == "2smmu", f"{opts['u']} {os}"
            assert opts["dp.u"] == "2smmu", f"{opts['dp.u']} {os}"
            assert opts["v"] == "2mtmv", f"{opts['v']} {os}"
            assert opts["dp.v"] == "2mtmv", f"{opts['dp.v']} {os}"
            assert opts["w"] == "2atmw", f"{opts['w']} {os}"
            assert opts["dp.w"] == "2atmw", f"{opts['dp.w']} {os}"
            assert opts["x"] == "2stmx", f"{opts['x']} {os}"
            assert opts["dp.x"] == "2stmx", f"{opts['dp.x']} {os}"
            assert opts["y"] == f"m{ltr[os]}y", f"{opts['y']} m{ltr[os]}y {os}"
            assert opts["dp.y"] == f"m{ltr[os]}y", f"{opts['dp.y']} m{ltr[os]}y {os}"

            try:
                assert opts["yoodle"] is not None
                assert True, "Should have thrown exception"

            except KeyError:
                pass


def test_cli_env_in_yaml():
    """test setting cli and env lookups in the yaml itself"""
    with TemporaryDirectory() as working_dir:
        base_dir = join(working_dir, "base")
        setup_settings(
            os="Linux",
            shared="test",
            Linux=join(base_dir, "Linux"),
            Darwin=join(base_dir, "macOS"),
            Windows=join(base_dir, "Windows"),
        )
        write(
            join(base_dir, "main.yml"),
            env={"aa": "alpha", "yy": "yota"},
            cli={"bb": "--beta"},
            yy="main yy",
            aa="main aa",
            bb="main bb",
        )
        write(
            join(base_dir, "test.yml"),
            env={"zz": "zeta"},
            cli={"dd": "--delta"},
            zz="test zz",
            dd="test dd",
        )
        settings.ENVIRON = {
            "alpha": "environ aa",
            "yota": "environ yy",
            "zeta": "environ zz",
            "delta": "environ dd",
        }
        settings.ARGV = [
            "exe",
            "--beta",
            "cli bb",
            "--zeta",
            "cli zz",
            "--delta",
            "cli dd",
        ]
        opts = Settings(join(base_dir, "main.py"), aa="code aa").cli("cli").env("env")
        assert opts["aa"] == "code aa", opts["aa"]
        assert opts["bb"] == "cli bb", opts["bb"]
        assert opts["dd"] == "cli dd", opts["dd"]
        assert opts["yy"] == "environ yy", opts["yy"]
        assert opts["zz"] == "environ zz", opts["zz"]


def test_environ_values():
    """test environment variable substitution"""
    with TemporaryDirectory() as working_dir:
        base_dir = join(working_dir, "base")
        setup_settings(
            os="Linux",
            shared="test",
            Linux=join(base_dir, "Linux"),
            Darwin=join(base_dir, "macOS"),
            Windows=join(base_dir, "Windows"),
        )
        write(
            join(base_dir, "main.yml"),
            output="${home}/reports",
            settings="${appDir}/settings.json",
            value="testing ${noenv} for noenv",
        )
        settings.ENVIRON = {
            "HOME": "sweet home",
            "APPDIR": "app data dir",
        }
        opts = Settings(join(base_dir, "main.py"), aa="code aa").cli("cli").env("env")
        assert opts["output"] == "sweet home/reports", opts["output"]
        assert opts["settings"] == "app data dir/settings.json", opts["settings"]
        assert opts["value"] == "testing ${noenv} for noenv", opts["value"]


def test_secret():
    """test os secret storage"""
    with TemporaryDirectory() as working_dir:
        base_dir = join(working_dir, "base")
        passwords = {"system": {"john": "setec astronomy"}}
        setup_settings(
            os="Linux",
            shared="test",
            Linux=join(base_dir, "Linux"),
            Darwin=join(base_dir, "macOS"),
            Windows=join(base_dir, "Windows"),
        )
        settings.GET_PASSWORD = lambda s, e: passwords.get(s, {}).get(e, None)
        write(join(base_dir, "main.yml"), password="main")
        opts = Settings(join(base_dir, "main.py")).key("password", "system/john")
        assert opts["password"] == "setec astronomy", opts["password"]


if __name__ == "__main__":
    test_secret()
    test_environ_values()
    test_cli_env_in_yaml()
    test_basic()
