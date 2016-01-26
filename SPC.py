"""Library to help facilitate reading SPC files.

SPC Specification:
    http://wiki.superfamicom.org/snes/show/SPC+and+RSN+File+Format
"""

offsets = [
    "0x00",  # File header SNES-SPC700 Sound File Data v0.30
    "0x21",  # 0x26, 0x26
    "0x23",  # 0x26 = Header Has ID666 Information / 0x27 = Header Has No ID666 Tag
    "0x24",  # Version Minor (i.e. 30)
    "0x25",  # PC
    "0x27",  # A
    "0x28",  # X
    "0x29",  # Y
    "0x2A",  # PSW
    "0x2B",  # SP (Lower Byte)
    "0x2C",  # Reserved
    "0x2E",  # Song Title
    "0x4E",  # Game Title
    "0x6E",  # Name of Dumper
    "0x7E",  # Comments
    "0x9E",  # Date SPC was Dumped (MM/DD/YYYY)
    "0xA9",  # Number of Seconds to Play Song before Fading Out
    "0xAC",  # Length of Fade in Milliseconds
    "0xB1",  # Artist of Song
    "0xD1",  # Default Channel Disables (0=Enable, 1=Disable)
    "0xD2",  # Emulator used to dump SPC (0=unknown, 1=ZSNES, 2=Snes9x)
    "0xD3",  # Reserved(0x00)
    "0x2E",  # Song Title
    "0x4E",  # Game Title
    "0x6E",  # Name of Dumper
    "0x7E",  # Comments
    "0x9E",  # Date SPC was Dumped (YYYYMMDD)
    "0xA2",  # Unused
    "0xA9",  # Number of Seconds to Play Song before Fading Out
    "0xAC",  # Length of Fade in Milliseconds
    "0xB0",  # Artist of Song
    "0xD0",  # Default Channel Disables (0=Enable, 1=Disable)
    "0xD1",  # Emulator used to dump SPC (0=unknown, 1=ZSNES, 2=Snes9x)
    "0xD2",  # Reserved (Set to 0x00)
    "0x100",  # 64KB RAM
    "0x10100",  # DSP Registers
    "0x10180",  # Unused
    "0x101C0",  # Extra RAM (Memory Region used when the IPL ROM region is set to read-only)
    "0x10200",  # Extended ID666
    "-1",  # EOF
]

header_keys = ["header", "bits", "tags", "version_minor"]

register_keys = ["pc", "a", "x", "y", "psw", "sp", "reserved"]

metadata_keys = [
    "song_title",
    "game_title",
    "dumper_name",
    "comments",
    "date_dumped",
    "num_of_sec_before_fade",
    "fade_length",
    "artist",
    "default_channel_disables",
    "emulator_used",
    "reserved",
]

binary_metadata_keys = [
    "song_title",
    "game_title",
    "dumper_name",
    "comments",
    "date_dumped",
    "unused",
    "num_of_sec_before_fade",
    "fade_length",
    "artist",
    "default_channel_disables",
    "emulator_used",
    "reserved",
]

ram_keys = ["64k_ram", "dsp_registers", "unused", "extra_ram", "extended_ID666"]


def _get_chunk(data, fr, to):
    """Cut the slice from the raw data, using the offsets."""
    return data[int(offsets[fr], 16) : int(offsets[to], 16)]


class SPC:
    def __init__(self, data):
        """Ingest an SPC file according to the specification."""
        self.headers = {}
        self.registers = {}
        self.song = {}
        self.binary_song = {}
        self.ram = {}

        tmp = 0
        for key in header_keys:
            self.headers[key] = _get_chunk(data, tmp, tmp + 1)
            tmp += 1

        for key in register_keys:
            self.registers[key] = _get_chunk(data, tmp, tmp + 1)
            tmp += 1

        for key in metadata_keys:
            # strip ending zero characters
            self.song[key] = "".join(
                [c for c in _get_chunk(data, tmp, tmp + 1) if hex(ord(c)) != "0x0"]
            )
            tmp += 1

        for key in binary_metadata_keys:
            self.binary_song[key] = _get_chunk(data, tmp, tmp + 1)
            tmp += 1

        for key in ram_keys:
            self.ram[key] = _get_chunk(data, tmp, tmp + 1)
            tmp += 1

    def __str__(self):
        """game name: artists - song name"""
        return "{}: {} - {}".format(
            self.song["game_title"], self.song["artist"], self.song["song_title"]
        )
