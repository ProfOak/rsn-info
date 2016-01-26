# -*- coding: utf-8 -*-
'''
    SPC Specification:
        http://wiki.superfamicom.org/snes/show/SPC+and+RSN+File+Format
'''

offsets = [
        '00',       # File header “SNES-SPC700 Sound File Data v0.30”
        '21',       # 0x26, 0x26
        '23',       # 0x26 = Header Has ID666 Information / 0x27 = Header Has No ID666 Tag
        '24',       # Version Minor (i.e. 30)
        '25',       # PC
        '27',       # A
        '28',       # X
        '29',       # Y
        '2A',       # PSW
        '2B',       # SP (Lower Byte)
        '2C',       # Reserved
        '2E',       # Song Title
        '4E',       # Game Title
        '6E',       # Name of Dumper
        '7E',       # Comments
        '9E',       # Date SPC was Dumped (MM/DD/YYYY)
        'A9',       # Number of Seconds to Play Song before Fading Out
        'AC',       # Length of Fade in Milliseconds
        'B1',       # Artist of Song
        'D1',       # Default Channel Disables (0=Enable, 1=Disable)
        'D2',       # Emulator used to dump SPC (0=unknown, 1=ZSNES, 2=Snes9x)
        'D3',       # Reserved(0x00)
        '2E',       # Song Title
        '4E',       # Game Title
        '6E',       # Name of Dumper
        '7E',       # Comments
        '9E',       # Date SPC was Dumped (YYYYMMDD)
        'A2',       # Unused
        'A9',       # Number of Seconds to Play Song before Fading Out
        'AC',       # Length of Fade in Milliseconds
        'B0',       # Artist of Song
        'D0',       # Default Channel Disables (0=Enable, 1=Disable)
        'D1',       # Emulator used to dump SPC (0=unknown, 1=ZSNES, 2=Snes9x)
        'D2',       # Reserved (Set to 0x00)
        '100',      # 64KB RAM
        '10100',    # DSP Registers
        '10180',    # Unused
        '101C0',    # Extra RAM (Memory Region used when the IPL ROM region is set to read-only)
        '10200',    # Extended ID666
        '-1'        # EOF (as far as slices are concerned)
]

header_keys = [
    'header', 'bits', 'tags', 'version_minor'
]

register_keys = [
    'pc', 'a', 'x', 'y', 'psw', 'sp', 'reserved'
]

metadata_keys = [
    'song_title', 'game_title', 'dumper_name', 'comments', 'date_dumped',
    'num_of_sec_before_fade', 'fade_length', 'artist',
    'default_channel_disables', 'emulator_used', 'reserved'
]

binary_metadata_keys = [
    'song_title', 'game_title', 'dumper_name', 'comments', 'date_dumped',
    'unused', 'num_of_sec_before_fade', 'fade_length', 'artist',
    'default_channel_disables', 'emulator_used', 'reserved'
]

ram_keys = [
    '64k_ram', 'dsp_registers', 'unused', 'extra_ram', 'extended_ID666'
]

def _get_chunk(data, fr, to):
    ''' cut the sice from the raw data, using the offsets '''
    return data[int(offsets[fr], 16) : int(offsets[to], 16)]

class SPC():
    def __init__(self, data):
        ''' sort the raw bits according to the SPC specification '''
        self.headers = {}
        self.registers = {}
        self.song = {}
        self.binary_song = {}
        self.ram = {}

        tmp = 0
        for i, key in enumerate(header_keys):
            self.headers[key] = _get_chunk(data, tmp, tmp+1)
            tmp += 1

        for i, key in enumerate(register_keys):
            self.registers[key] = _get_chunk(data, tmp, tmp+1)
            tmp += 1

        for i, key in enumerate(metadata_keys):
            # strip ending 0's
            # covnentional methods are futile
            # find a better way to do this
            self.song[key] = "".join([c for c in _get_chunk(data, tmp, tmp+1) if hex(ord(c)) != '0x0'])
            tmp += 1

        for i, key in enumerate(binary_metadata_keys):
            self.binary_song[key] = _get_chunk(data, tmp, tmp+1)
            tmp += 1
        #print "binary"

        for i, key in enumerate(ram_keys):
            self.ram[key] = _get_chunk(data, tmp, tmp+1)
            tmp += 1

    def __str__(self):
        ''' game name: artists - song name '''
        return "{}: {} - {}".format(self.song['game_title'], self.song['artist'],self.song['song_title'])

