#!/usr/bin/python
import sys

DEFAULT_DELAY     = 0x01
DELAY             = 0x01
MOD               = 0x02
KEY_PUSH_0        = 0x03
KEY_PUSH_1        = 0x13
KEY_PUSH_2        = 0x23
KEY_PUSH_3        = 0x33
KEY_PUSH_4        = 0x43
KEY_PUSH_5        = 0x53
KEY_PUSH_AND_SEND = 0x04

key_map = {
    'KEY_NONE'           : 0x00,
    'A'                  : 0x04,
    'B'                  : 0x05,
    'C'                  : 0x06,
    'D'                  : 0x07,
    'E'                  : 0x08,
    'F'                  : 0x09,
    'G'                  : 0x0A,
    'H'                  : 0x0B,
    'I'                  : 0x0C,
    'J'                  : 0x0D,
    'K'                  : 0x0E,
    'L'                  : 0x0F,
    'M'                  : 0x10,
    'N'                  : 0x11,
    'O'                  : 0x12,
    'P'                  : 0x13,
    'Q'                  : 0x14,
    'R'                  : 0x15,
    'S'                  : 0x16,
    'T'                  : 0x17,
    'U'                  : 0x18,
    'V'                  : 0x19,
    'W'                  : 0x1A,
    'X'                  : 0x1B,
    'Y'                  : 0x1C,
    'Z'                  : 0x1D,
    '1'                  : 0x1E,
    '2'                  : 0x1F,
    '3'                  : 0x20,
    '4'                  : 0x21,
    '5'                  : 0x22,
    '6'                  : 0x23,
    '7'                  : 0x24,
    '8'                  : 0x25,
    '9'                  : 0x26,
    '0'                  : 0x27,
    'ENTER'              : 0x28,
    'ESCAPE'             : 0x29,
    'BACKSPACE'          : 0x2A,
    'TAB'                : 0x2B,
    'SPACE'              : 0x2C,
    'MINUS'              : 0x2D,
    'EQUAL'              : 0x2E,
    'BRACKET_LEFT'       : 0x2F,
    'BRACKET_RIGHT'      : 0x30,
    'BACKSLASH'          : 0x31,
    'EUROPE_1'           : 0x32,
    'SEMICOLON'          : 0x33,
    'APOSTROPHE'         : 0x34,
    'GRAVE'              : 0x35,
    'COMMA'              : 0x36,
    'PERIOD'             : 0x37,
    'SLASH'              : 0x38,
    'CAPS_LOCK'          : 0x39,
    'F1'                 : 0x3A,
    'F2'                 : 0x3B,
    'F3'                 : 0x3C,
    'F4'                 : 0x3D,
    'F5'                 : 0x3E,
    'F6'                 : 0x3F,
    'F7'                 : 0x40,
    'F8'                 : 0x41,
    'F9'                 : 0x42,
    'F10'                : 0x43,
    'F11'                : 0x44,
    'F12'                : 0x45,
    'PRINTSCREEN'        : 0x46,
    'SCROLL_LOCK'        : 0x47,
    'PAUSE'              : 0x48,
    'INSERT'             : 0x49,
    'HOME'               : 0x4A,
    'PAGE_UP'            : 0x4B,
    'DELETE'             : 0x4C,
    'END'                : 0x4D,
    'PAGE_DOWN'          : 0x4E,
    'ARROW_RIGHT'        : 0x4F,
    'ARROW_LEFT'         : 0x50,
    'ARROW_DOWN'         : 0x51,
    'ARROW_UP'           : 0x52,
    'NUM_LOCK'           : 0x53,
    'KEYPAD_DIVIDE'      : 0x54,
    'KEYPAD_MULTIPLY'    : 0x55,
    'KEYPAD_SUBTRACT'    : 0x56,
    'KEYPAD_ADD'         : 0x57,
    'KEYPAD_ENTER'       : 0x58,
    'KEYPAD_1'           : 0x59,
    'KEYPAD_2'           : 0x5A,
    'KEYPAD_3'           : 0x5B,
    'KEYPAD_4'           : 0x5C,
    'KEYPAD_5'           : 0x5D,
    'KEYPAD_6'           : 0x5E,
    'KEYPAD_7'           : 0x5F,
    'KEYPAD_8'           : 0x60,
    'KEYPAD_9'           : 0x61,
    'KEYPAD_0'           : 0x62,
    'KEYPAD_DECIMAL'     : 0x63,
    'EUROPE_2'           : 0x64,
    'MENU'               : 0x65,
    'POWER'              : 0x66,
    'KEYPAD_EQUAL'       : 0x67,
    'F13'                : 0x68,
    'F14'                : 0x69,
    'F15'                : 0x6A,
    'CTRL'               : 0xE0,
    'SHIFT'              : 0xE1,
    'ALT'                : 0xE2,
    'GUI'                : 0xE3,
    'CTRLR'              : 0xE4,
    'SHIFTR'             : 0xE5,
    'ALTR'               : 0xE6,
    'GUIR'               : 0xE7,

    # Mod key bit location
    # The mod key is taken in as a byte
    # For: Ctrl + Alt + Delete (Assume Left Ctrl and Alt key)
    #      Mod Byte(0b0000 0101) + Delete(0x4C)
    'MOD_CTRL'    : 0,
    'MOD_SHIFT'   : 1,
    'MOD_ALT'     : 2,
    'MOD_GUI'     : 3,
    'MOD_CTRLR'   : 4,
    'MOD_SHIFTR'  : 5,
    'MOD_ALTR'    : 6,
    'MOD_GUIR'    : 7
    }

# 
# Args:
#   E: Expression representing some key combination requiring mod keys.
#
# TODO(nqbit): Add support for multiple non-modifier keys.
def getModCommand(E):
    i = 0
    val = 0
    while('MOD_' + E[i] in key_map):
        val = val | (1 << key_map['MOD_' + E[i]])
        i = i + 1
    key = (E[i]).upper().strip()
    return [val, KEY_PUSH_AND_SEND, key_map[key]]

# Args:
#   b: the byte to be padded
#
# Returns:
#   A string representing the byte in hex.
def hex_padded(b):
    b = hex(b)
    s = len(b[2:])
    return '0x' + '0'*(2-s) + b[2:]
    
# Args:
#   L: A list of bytes representing the input commands.
#
# Returns:
#   A list of strings representing the bytes in hex.
def str_bytecode(L):
    return [hex_padded(b & 0xFF) for b in L]

def print_usage():
    print "Usage: wixel_sk FILENAME -[c|b|i]"
    exit()

if len(sys.argv) == 1:
    print_usage()

f = open(sys.argv[1])
byte_code = []

for line in f:
    items = line.split(' ')
    # Modifier commands
    if (items[0] == 'GUI' or
        items[0] == 'GUIR' or
        items[0] == 'CTRL' or
        items[0] == 'CTRLR' or
        items[0] == 'ALT' or
        items[0] == 'ALTR' or
        items[0] == 'SHIFT' or
        items[0] == 'SHIFTR'):
        
        if len(items) > 1:
            byte_code.append(MOD)
            byte_code.extend(getModCommand(items))
        else:
            byte_code.append(KEY_PUSH_AND_SEND)
            byte_code.append(key_map[items[0]])

    # Ignore line. It is like a comment.
    elif (items[0] == 'REM'):
        pass

    # Default Delay functionality
    elif (items[0] == 'DEFAULT_DELAY'):
        byte_code.append(DEFAULT_DELAY)
        # High byte
        byte_code.append((int(items[1]) >> 8) & 0xFF)
        # Low byte
        byte_code.append(int(items[1]) & 0xFF)

    # Delay functionality
    elif (items[0] == 'DELAY'):
        byte_code.append(DELAY)
        # High byte
        byte_code.append((int(items[1]) >> 8) & 0xFF)
        # Low byte
        byte_code.append(int(items[1]) & 0xFF)

    # String functionality to type out full strings
    elif (items[0] == 'STRING'):
        for item in items[1:]:
            for c in item:
                if c.isalnum():
                    if c.isupper():
                        byte_code.append(MOD)
                        byte_code.append(1 << key_map['MOD_SHIFT'])

                    # Send key press
                    byte_code.append(KEY_PUSH_AND_SEND)
                    byte_code.append(key_map[c.upper()])
                # Non-alphanumeric
                else:
                    byte_code.append(KEY_PUSH_AND_SEND)
                    if c == '~':
                        print "Error: '~' not yet implemented"
                        exit()
                    if c == '-' or c == '_':
                        if c == '_':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['MINUS'])
                    if c == '=':
                        if c == '+':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['EQUAL'])
                    if c == '[':
                        if c == '{':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['BRACKET_LEFT'])
                    if c == ']':
                        if c == '}':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['BRACKET_RIGHT'])
                    if c == '\\':
                        if c == '|':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['BACKSLASH'])
                    if c == ';':
                        if c == ':':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['SEMICOLON'])
                    if c == '\'':
                        if c == '"':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['APOSTROPHE'])
                    if c == ',':
                        if c == '<':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['COMMA'])
                    if c == '.':
                        if c == '>':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['PERIOD'])
                    if c == '/':
                        if c == '?':
                            byte_code.append(MOD)
                            byte_code.append(1 << key_map['MOD_SHIFT'])

                        byte_code.append(KEY_PUSH_AND_SEND)
                        byte_code.append(key_map['SLASH'])

            # Reached a space so send one!
            byte_code.append(KEY_PUSH_AND_SEND)
            byte_code.append(key_map['SPACE'])
        
    # Attempt to parse the rest of the keys.
    # TODO(nqbit): Handle erros as this should throw an error for
    # an undefined command.
    else:
        byte_code.append(KEY_PUSH_AND_SEND)
        byte_code.append(key_map[items[0].strip()])
                
if len(sys.argv) == 3 and byte_code:
    if sys.argv[2] == '-c':
        ba = str_bytecode(byte_code)
        sys.stdout.write('static uint8_t attack[]={')
        for b in ba[:-1]:
            sys.stdout.write(b + ',')
        sys.stdout.write(ba[-1] + '};')
    elif sys.argv[2] == '-b':
        print str_bytecode(byte_code)
    elif sys.argv[2] == '-i':
        print byte_code
else:
    print_usage()
    
        
        
