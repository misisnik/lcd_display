import numbers
import time

import sys
import subprocess

from multiprocessing import Process, Queue

from mcp2210.commands import ChipSettings, SPISettings, USBSettings
from mcp2210.device import MCP2210, CommandException

import time


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

pic=[
0x7F,0x01,0x01,0x01,0x01,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xF8,0x48,
0x48,0x48,0x48,0x00,0xC0,0xB0,0x88,0xB0,0xC0,0x00,0x30,0x48,0x48,0x90,0x00,0x08,
0x08,0xF8,0x08,0x08,0x00,0xF8,0x48,0x48,0xC8,0x30,0x00,0x00,0xF8,0x00,0x00,0x30,
0x48,0x48,0x90,0x00,0x00,0xF8,0x00,0x00,0xF8,0x30,0x40,0x80,0xF8,0x00,0x00,0xF0,
0x08,0x08,0x48,0xD0,0x00,0x00,0x00,0x00,0x08,0x08,0xF8,0x08,0x08,0x00,0xF8,0x48,
0x48,0x48,0x48,0x00,0xF0,0x08,0x08,0x08,0x10,0x00,0x00,0xF8,0x40,0x40,0x40,0xF8,
0x00,0x00,0xF8,0x30,0x40,0x80,0xF8,0x00,0x00,0xF0,0x08,0x08,0x08,0xF0,0x00,0x00,
0xF8,0x00,0x00,0x00,0x00,0xF0,0x08,0x08,0x08,0xF0,0x00,0x00,0xF0,0x08,0x08,0x48,
0xD0,0x00,0x00,0x08,0x30,0xC0,0x30,0x08,0x00,0x00,0x00,0x00,0x00,0xF0,0x08,0x08,
0x08,0x10,0x00,0x00,0xF0,0x08,0x08,0x08,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0xF8,0x00,0x00,0x00,0x08,0x08,0xF8,0x08,0x08,0x00,0xF8,0x08,0x08,0x08,0xF0,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x7F,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x02,
0x02,0x02,0x02,0x02,0x01,0x00,0x00,0x00,0x01,0x02,0x01,0x02,0x02,0x01,0x00,0x00,
0x00,0x03,0x00,0x00,0xE0,0x03,0x00,0x00,0xC0,0x43,0x40,0x40,0xC3,0x00,0x00,0x01,
0x02,0xE2,0x21,0x20,0x20,0x23,0x20,0x20,0xE3,0x00,0x00,0x41,0x43,0x40,0x40,0xC1,
0x62,0x42,0x42,0x41,0x40,0x40,0x00,0x80,0x80,0x80,0x83,0x80,0xA0,0xC0,0x83,0x82,
0xC2,0x82,0x02,0x40,0x41,0xC2,0x22,0x22,0x01,0x40,0x80,0x03,0xE0,0x00,0x00,0x83,
0x80,0xE0,0x83,0x00,0x80,0x81,0xE3,0x80,0x80,0x81,0x02,0x42,0x42,0x41,0x40,0xC0,
0x63,0x42,0x42,0x42,0x40,0x41,0x02,0xE2,0x22,0x21,0xE0,0x00,0xE1,0xA2,0xA2,0xA2,
0xE1,0x00,0x00,0x00,0x00,0x03,0xE0,0x00,0x00,0x60,0x80,0x00,0x00,0x01,0x02,0x02,
0x22,0x21,0x20,0x20,0x21,0xA2,0x22,0x22,0xE1,0x00,0x00,0x02,0x00,0x08,0x06,0x00,
0x00,0x03,0x02,0x02,0x02,0x00,0x00,0x03,0x00,0x00,0x00,0x03,0x02,0x02,0x02,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0xC1,0x3F,0x01,0xFF,0x80,0xBF,0x92,0x92,0x92,0xBF,0xC0,0x00,0x00,
0x00,0xFF,0x42,0x42,0x42,0x42,0x42,0x42,0xFF,0x00,0x00,0x40,0x44,0x26,0x15,0x84,
0xFF,0x04,0x0C,0x14,0x24,0x40,0x00,0x80,0x80,0x40,0x30,0x0F,0x82,0x82,0x82,0x7E,
0x00,0x00,0x00,0x31,0x0D,0xFF,0x05,0x09,0x10,0x12,0x14,0x10,0xFF,0x08,0x00,0x88,
0x88,0xFF,0x04,0x80,0x8C,0x54,0x27,0x54,0x8C,0x80,0x00,0x08,0x04,0x02,0xFF,0x29,
0x29,0x29,0xA9,0xFF,0x00,0x00,0x00,0xFF,0x10,0x13,0x1C,0x00,0xFF,0x84,0x5C,0x24,
0x57,0x88,0x00,0x04,0x82,0xC1,0xA0,0x98,0x86,0x50,0x61,0xC2,0x04,0x04,0x00,0x01,
0x01,0x3D,0x25,0x25,0x25,0x3D,0x81,0x80,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,0x0F,0x01,0x01,0xFD,0xFD,0x8D,
0x8D,0x8D,0x8D,0x8D,0x8D,0x8D,0x01,0x01,0xFD,0xFD,0x8D,0x8D,0x8D,0x8D,0x8D,0xDD,
0xF9,0x71,0x01,0x01,0xE1,0xF9,0x19,0x0D,0x0D,0x0D,0x0D,0x1D,0x39,0x11,0x01,0x01,
0x61,0x31,0x19,0xFD,0xFD,0x01,0x01,0x01,0xF1,0xF9,0x8D,0x0D,0x0D,0x9D,0xF9,0xE1,
0x01,0x31,0x39,0x1D,0x0D,0x0D,0x8D,0xF9,0x71,0x01,0xE1,0xF9,0x9D,0xCD,0xCD,0xCD,
0x9D,0x19,0x01,0x01,0x01,0xC1,0xE1,0x39,0xFD,0xFD,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x61,0x31,0x19,0xFD,0xFD,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xC1,0xE1,
0x21,0x21,0x61,0x41,0x01,0x01,0x81,0x81,0x81,0x81,0x01,0x01,0x81,0x81,0x81,0x81,
0x01,0xA1,0xA1,0x01,0x01,0x81,0x81,0x81,0x81,0x01,0x01,0x01,0x81,0x81,0x81,0x81,
0x01,0x01,0x0F,0x0F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xF0,0xF0,0x80,0x80,0xBF,0xBF,0xB1,
0xB1,0xB1,0xB1,0xB1,0xB1,0xB1,0x80,0x80,0xBF,0xBF,0x81,0x81,0x81,0x83,0x87,0x9E,
0xBC,0xB0,0xA0,0x80,0x87,0x9F,0x98,0xB0,0xB0,0xB0,0xB0,0xB8,0x9C,0x88,0x80,0x80,
0x80,0x80,0x80,0xBF,0xBF,0x80,0x80,0x80,0x98,0xB9,0xB3,0xB3,0xB3,0xB9,0x9F,0x87,
0x80,0xB0,0xB8,0xBC,0xB6,0xB7,0xB3,0xB1,0xB0,0x80,0x87,0x9F,0xB9,0xB0,0xB0,0xB1,
0x9F,0x8F,0x80,0x8E,0x8F,0x8D,0x8C,0x8C,0xBF,0xBF,0x8C,0x80,0x80,0x86,0x86,0x86,
0x86,0x80,0x80,0x80,0x80,0xBF,0xBF,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x89,0x99,
0x93,0x93,0x9E,0x8E,0x80,0x8F,0x9F,0x92,0x92,0x9B,0x8B,0x80,0x9F,0x9F,0x80,0x80,
0x80,0x9F,0x9F,0x80,0x8F,0x9F,0x92,0x92,0x9B,0x8B,0x80,0x8B,0x9B,0x96,0x96,0x9D,
0x8D,0x80,0xF0,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x80,0xC0,0x00,0x00,0x00,0x80,0x40,0x40,0x40,0x80,0x00,0x80,0x40,
0x40,0x40,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x81,0x41,0x41,0x41,0x81,0x01,
0x01,0x01,0x81,0xC1,0x01,0x01,0x01,0x01,0x01,0xC1,0x41,0x41,0x41,0x81,0x01,0x41,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xC1,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xC1,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xC1,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0xC1,0x01,0x01,0x01,0x01,0x01,0x41,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFE,0x80,0x81,0x80,0xBF,0x80,0x80,0x00,0x13,0x24,0x24,0x24,0x1F,0x00,0x20,0x30,
0x28,0x24,0x23,0x00,0x21,0x12,0x0C,0x12,0x21,0x00,0x1F,0x22,0x22,0x22,0x1C,0x00,
0x0C,0x0B,0x08,0x3F,0x08,0x00,0x00,0x00,0x00,0x3F,0x04,0x04,0x04,0x03,0x00,0x3F,
0x00,0x21,0x12,0x0C,0x12,0x21,0x00,0x1E,0x25,0x25,0x25,0x16,0x00,0x3F,0x00,0x12,
0x25,0x25,0x29,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x0C,0x30,0x0E,0x01,0x0E,
0x30,0x0C,0x03,0x00,0x03,0x0C,0x30,0x0E,0x01,0x0E,0x30,0x0C,0x03,0x00,0x03,0x0C,
0x30,0x0E,0x01,0x0E,0x30,0x0C,0x03,0x00,0x00,0x20,0x00,0x3F,0x00,0x1E,0x21,0x21,
0x21,0x12,0x00,0x1E,0x21,0x21,0x12,0x3F,0x00,0x08,0x08,0x08,0x00,0x1E,0x21,0x21,
0x21,0x12,0x00,0x3F,0x02,0x01,0x01,0x3E,0x00,0x3F,0x00,0x3F,0x01,0x01,0x01,0x3E,
0x00,0x1A,0x25,0x25,0x15,0x3E,0x00,0x00,0x20,0x00,0x1E,0x21,0x21,0x21,0x12,0x00,
0x1E,0x21,0x21,0x21,0x1E,0x00,0x3F,0x02,0x01,0xBF,0x81,0x81,0xBE,0x80,0x80,0xFE,
]


pic1=[
0xFF,0x01,0x01,0x01,0x01,0x01,0x01,0xC1,0xF1,0xFD,0xFD,0x81,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0xC1,0xE1,0xF1,0xF9,0xF9,0xFD,0xFD,0xF9,0xF9,0x61,0xF1,0x51,
0x01,0x09,0x0D,0x0D,0x05,0x09,0x09,0x09,0x09,0x09,0x09,0x99,0xB9,0xC1,0x01,0x01,
0x01,0x81,0x81,0xC1,0xC1,0x81,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
0xFF,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xE1,0xF1,0xF1,0xF1,
0xE1,0xC1,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xF1,0x01,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0xFF,
0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x81,0xC1,0xC1,0x81,0x81,0x01,
0x01,0x01,0xC1,0xB9,0x99,0x09,0x09,0x09,0x09,0x09,0x09,0x05,0x0D,0x0D,0x09,0x01,
0x51,0xF1,0x61,0xF9,0xF9,0xFD,0xFD,0xF9,0xF9,0xF1,0xE1,0xC1,0x01,0x01,0x01,0x01,
0x01,0x01,0x01,0x01,0x81,0xFD,0xFD,0xF1,0xC1,0x01,0x01,0x01,0x01,0x01,0x01,0xFF,
0xFF,0x00,0x30,0x30,0x78,0x7C,0x7F,0x71,0x66,0x60,0x71,0x7F,0x7C,0x80,0x00,0x00,
0x00,0x00,0x00,0x00,0x07,0x8F,0x7F,0x1F,0x1F,0x3F,0x7F,0xFE,0xFE,0xFA,0xF3,0xF6,
0xF6,0xC4,0x48,0x18,0x18,0x78,0xF8,0xF8,0xF8,0xFC,0xF4,0xF4,0xEF,0xE8,0x99,0x71,
0x06,0x1F,0xFF,0xFF,0xFF,0xFF,0x7F,0x3E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xE0,0xFC,0xFE,0xFE,
0xFC,0x78,0x20,0x20,0x10,0x10,0x08,0x08,0x08,0x0C,0x04,0x04,0x07,0x07,0x0F,0x0F,
0x0F,0x0F,0x1F,0x10,0x10,0x20,0x20,0x40,0xC0,0x80,0xFF,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3E,0x7F,0xFF,0xFF,0xFF,0xFF,0x1F,0x06,
0x71,0x99,0xE8,0xEF,0xF4,0xF4,0xFC,0xF8,0xF8,0xF8,0x78,0x18,0x18,0x48,0xC4,0xF6,
0xF6,0xF3,0xFA,0xFE,0xFE,0x7F,0x3F,0x1F,0x1F,0x7F,0x8F,0x07,0x00,0x00,0x00,0x00,
0x00,0x00,0x80,0x7C,0x7F,0x71,0x60,0x66,0x71,0x7F,0x7C,0x78,0x30,0x30,0x00,0xFF,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0x23,0x7C,0x48,
0x48,0x88,0x78,0x30,0x0C,0xE3,0xF0,0xF8,0xFC,0x1E,0x4E,0x4E,0x6F,0xDF,0x7D,0x31,
0x01,0x00,0x00,0x00,0xC0,0xB0,0x98,0x99,0x39,0xF9,0xF9,0xF9,0xF1,0xE1,0xC0,0x00,
0x00,0x00,0x00,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0x70,0x08,0x07,0x03,0x01,
0x00,0x80,0x80,0x84,0x84,0x00,0x08,0x00,0x00,0x00,0x02,0x01,0xC0,0xF0,0xF8,0xFC,
0xFE,0xFE,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x7E,0x7C,0x7C,0x30,0x60,
0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00,0x00,0x00,
0x00,0xC0,0xE1,0xF1,0xF9,0xF9,0xF9,0x39,0x99,0x98,0xB0,0xC0,0x00,0x00,0x00,0x01,
0x31,0x7D,0xDF,0x6F,0x4E,0x4E,0x1E,0xFC,0xF8,0xF0,0xE3,0x0C,0x30,0x78,0x88,0x48,
0x48,0x7C,0x23,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x07,0x08,0x18,0x10,
0x10,0x3F,0xF8,0x60,0xC0,0x83,0x07,0x0F,0x0F,0x0E,0x0C,0x04,0x0E,0x8C,0x88,0x00,
0x80,0x00,0x00,0x00,0x00,0x04,0x0C,0x1D,0x1D,0x3F,0x3F,0x3F,0x3F,0x1F,0x0F,0x00,
0x00,0x80,0xE0,0x3F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xE0,0xFE,0xF1,0xFC,0xFC,0xFE,0xFF,0xFF,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x7E,0x7E,0x7C,0x38,0x20,0x1F,0x3F,0xFF,0xFF,
0xCF,0xC7,0xE7,0xE3,0xF3,0xF3,0xF1,0xF9,0xF9,0xFC,0xFC,0xFC,0xFE,0x7E,0x3F,0x00,
0x01,0x1F,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0xE0,0x80,0x00,
0x00,0x0F,0x1F,0x3F,0x3F,0x3F,0x3F,0x1D,0x1D,0x0C,0x04,0x00,0x00,0x00,0x00,0x80,
0x00,0x88,0x8C,0x0E,0x04,0x0C,0x0E,0x0F,0x0F,0x07,0x83,0xC0,0x60,0xF8,0x3F,0x10,
0x10,0x18,0x08,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x01,0x03,0x1C,0x71,0x83,0x02,0xE4,0xFC,0x78,0x39,0x11,0x10,0x10,0x10,
0x20,0x20,0x20,0x20,0x20,0xE0,0xE0,0xE0,0x70,0x30,0x30,0x78,0xF8,0xFC,0xE4,0x02,
0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0xCF,0x3F,0xFF,0xFF,0xC7,0xE7,0xE3,
0xF3,0xF3,0xF1,0xF9,0xF8,0xFC,0xFC,0xFC,0xFE,0xFE,0x7F,0x1F,0x03,0x00,0x00,0x01,
0x03,0x03,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x03,0x01,0x01,0x80,0x40,0x20,
0x18,0x0F,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,
0x02,0xE4,0xFC,0xF8,0x78,0x30,0x30,0x70,0xE0,0xE0,0xE0,0x20,0x20,0x20,0x20,0x20,
0x10,0x10,0x10,0x11,0x39,0x78,0xFC,0xE4,0x02,0x83,0x71,0x1C,0x03,0x01,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0xF1,0x1F,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x01,0x04,0x10,0x60,0x00,0x00,0x03,0x07,0x18,
0xE0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x06,0x08,0x11,0x31,0x23,0x43,
0x47,0xC7,0x87,0x87,0x87,0x83,0x03,0x03,0x01,0x00,0x00,0x04,0x04,0x84,0xA0,0x80,
0x80,0xC0,0xC0,0x20,0x20,0x10,0x10,0x08,0x08,0x04,0xFE,0xC2,0xC1,0xE0,0xF0,0x70,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xE0,
0x18,0x07,0x03,0x00,0x00,0x60,0x10,0x04,0x01,0x03,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x1F,0xF1,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x83,0x3E,0x1E,0x0C,0x04,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x01,0x07,0x07,0x83,0x43,0x67,0xA7,0x27,
0x27,0x27,0xC7,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x03,0x01,0x00,
0x00,0x00,0x00,0x00,0xE0,0x20,0x10,0x10,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x04,0x0C,0x1E,0x3E,0x83,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,
0xFF,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x87,0x90,0xA0,0xA0,0xC0,0xC1,0xC2,0xC2,0xA6,
0xB6,0xA2,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xA0,0x9E,0x8F,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0xFF,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x87,0xA8,0xA0,0xB8,0xA7,0xA2,
0x82,0x81,0xBD,0xA2,0xA2,0xB9,0xA7,0x90,0xB2,0x8F,0x83,0x82,0xB9,0xA7,0x80,0xB8,
0xA6,0xA1,0xB1,0xAF,0x90,0x80,0xBC,0xA2,0xA2,0xB9,0xA7,0x90,0x80,0x80,0x80,0xFF,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x8F,0x9E,0xA0,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xA2,0xB6,
0xA6,0xC2,0xC2,0xC1,0xC0,0xA0,0xA0,0x90,0x87,0x80,0x80,0x80,0x80,0x80,0x80,0x80,
0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0xFF,
]

pic2=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0xE0,0xF0,0x30,0x10,0x18,
0x18,0x18,0x10,0x30,0x18,0x0C,0x84,0x8F,0xCC,0xCC,0xDC,0xFC,0x70,0x40,0xC0,0xF0,
0xF8,0xF8,0xF8,0xF8,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0xC0,0xF8,0xFC,0xFF,0xFE,0xE0,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x80,0xE0,0xF0,0xF8,0xFC,0xFC,0xFE,0xFE,0xFC,0xF8,0xF0,0xF0,0x58,0x08,
0x0C,0x0E,0x0E,0x06,0x04,0x0C,0x0C,0x0C,0x04,0x04,0x1C,0xFC,0xEC,0xC0,0x80,0x00,
0x80,0x80,0xC0,0xC0,0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xF8,0xFC,
0xFE,0xFE,0xFF,0xFF,0xBF,0xFF,0xFE,0xC3,0xC3,0xC1,0xC3,0xC3,0xC6,0xC6,0x86,0xC6,
0xCC,0xF8,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0xF0,0xF8,0xFC,0xFC,0xFC,0xFC,0xFC,0xF8,0xE0,
0x90,0x98,0x08,0x0C,0x08,0x08,0x0C,0x14,0x1C,0x2C,0xE0,0x40,0x00,0x00,0x00,0x00,
0xE0,0xE0,0xF8,0xF8,0xF8,0xF8,0xF8,0xF0,0xF0,0x78,0x1C,0x3F,0x3F,0xBE,0xBF,0xFF,
0xDF,0xDD,0x8F,0x87,0x03,0x03,0x07,0x87,0xEF,0xEF,0x7F,0x7F,0xF7,0xF2,0xF3,0xE7,
0xEF,0xDF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0x38,0x10,0x00,0x00,
0x30,0x30,0x38,0x3C,0x3F,0x3D,0x37,0x26,0x3D,0x39,0x7F,0xF8,0x80,0x00,0x00,0x00,
0x00,0x00,0x03,0x0F,0x9F,0x7F,0x1F,0x0F,0x7F,0x7F,0xFF,0xFF,0xFB,0xFB,0xFB,0xF6,
0xEE,0x7C,0x18,0x18,0x78,0xFC,0xFC,0xFC,0xFC,0xF4,0xF6,0xF7,0xFD,0xFD,0xF9,0x07,
0x1F,0x3F,0xFF,0xFF,0xFF,0xFF,0x7F,0x1E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xC0,0x40,0xE0,0xF0,0x3C,0x1E,0x9B,0xD9,
0xD9,0x3B,0x03,0x03,0x03,0x03,0x81,0xC7,0x4F,0x7F,0x7F,0xFF,0xFE,0xFE,0x9E,0x1E,
0x0D,0x07,0x06,0x01,0x03,0x06,0x7C,0xF8,0xFC,0xFC,0xFC,0xFC,0xF8,0xF0,0x00,0x00,
0x00,0x00,0x00,0x80,0x60,0x30,0x19,0x0F,0x07,0x07,0x07,0x07,0x07,0x03,0x01,0x00,
0x00,0x01,0x01,0x1F,0x3F,0x7F,0x7F,0xFF,0x7F,0x7F,0x7F,0x33,0x1C,0xE0,0x00,0x00,
0x07,0x07,0x0F,0x1F,0x1F,0x1F,0xFF,0xFF,0x01,0x00,0xF8,0xFE,0xFF,0xFF,0x0F,0x03,
0x73,0x11,0x11,0xB3,0x0F,0x00,0x00,0x0F,0x03,0x18,0x04,0x0C,0xC8,0xC0,0xE3,0xFF,
0xFF,0xFF,0x7F,0x3F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x03,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0x61,0x3F,0x7C,0xE8,0xC8,
0xC8,0xF8,0x3C,0xEF,0xF1,0xF8,0xFC,0xFC,0xFE,0xDE,0x6F,0x2F,0xFF,0xFF,0x3D,0x00,
0x00,0x00,0x00,0xE0,0xF8,0xF8,0xBD,0x3D,0xFD,0xFB,0xFB,0xF1,0xF1,0xE1,0x00,0x00,
0x00,0x00,0xFF,0x7C,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0xF0,0xFC,0x06,0x03,0x61,0xC0,0x00,0x03,0x07,0x04,0x9A,0x1B,0x1B,
0x10,0x00,0x00,0x00,0x3C,0x7E,0xCF,0xC7,0xC0,0xE0,0xF0,0xFF,0xFF,0x7F,0x3F,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0xE0,0xFF,0x1F,0x1F,0x1F,0x0F,0x0F,0x03,0x00,0xC0,
0x70,0x0C,0x07,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x70,0xFC,0xFE,0x0F,0x07,0xE7,0xEE,0x09,0x1F,0xF0,
0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x07,0x0F,0x0F,0x0F,0x0F,0x0E,
0x0E,0x06,0x03,0x01,0x30,0x32,0x33,0x1F,0x1B,0x10,0x10,0x1C,0x0C,0x00,0x00,0x00,
0x00,0x00,0x00,0x80,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x0E,0x1C,0x18,0x11,0x3B,
0x7F,0xFF,0x60,0xC3,0x87,0x0F,0x0F,0x0F,0x0F,0x8E,0x86,0x8F,0x9C,0x8C,0x80,0x80,
0x00,0x00,0x00,0x01,0x0C,0x0C,0x1D,0x1C,0x3F,0x3F,0x3F,0x1F,0x1F,0x0F,0x01,0x00,
0xC0,0xE0,0x7F,0x1F,0x00,0x00,0x00,0x00,0x00,0xC0,0xE0,0xF0,0xF8,0xFC,0xFE,0xFC,
0xF8,0xE0,0xE0,0xE1,0xC7,0xDC,0xB0,0xE0,0x80,0x01,0x03,0x03,0x01,0x01,0x07,0x0C,
0x18,0x30,0x20,0x60,0x40,0x40,0x40,0x40,0x41,0x41,0x61,0x20,0x30,0x10,0x00,0x00,
0x00,0x00,0x00,0x00,0xC0,0x7C,0x0F,0x00,0x00,0x00,0x00,0x00,0x00,0x3C,0x7E,0xC7,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x07,0x06,0x01,0x01,0xC0,0x60,0x80,
0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x0F,0x1C,0x38,0x30,0x20,0x60,0x60,0x40,0x40,
0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0x40,0x40,0x00,0x00,0x20,0x20,0x10,0x18,
0x08,0x0C,0x1E,0x1F,0x3F,0x3F,0xFF,0xFF,0x7F,0x03,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x03,0x0F,0x3C,0xF1,0xC3,0x06,0xE4,0xFC,0x78,0x39,0x11,0x11,0x11,0x31,0x30,
0x30,0x20,0x20,0x20,0x30,0xF0,0xF0,0x70,0x30,0x70,0xF8,0xF8,0xFC,0xE6,0x06,0x03,
0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0xF1,0xFF,0x7F,0xDF,0x87,0xC3,0x7E,
0x9E,0xE1,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xFE,0xFC,0xF8,0xF8,
0xF8,0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xE0,0xF0,0xF0,0xF0,0xF0,0x10,0x18,0x18,0x08,
0x0C,0x0C,0x06,0x03,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x03,0x00,0x0C,0x08,0x10,0xB0,0xE0,0xE0,0xE0,0xC0,0xE0,0xF0,0xF0,0xF0,0xF0,0xE0,
0x80,0x00,0x00,0xC0,0x40,0xC0,0xE0,0x20,0x30,0x10,0x18,0x0C,0x05,0x06,0x03,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xF0,0xFC,
0xFE,0xFF,0xFF,0xFF,0xFF,0x63,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0xFC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0xFB,0x3F,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x07,0x07,0x0C,0x38,0xE0,0x40,0x01,0x03,0x0F,0x38,0xF0,
0x40,0x00,0x00,0x00,0x00,0x00,0x07,0x07,0x0F,0x1F,0x3F,0x3F,0x7E,0x7E,0x7E,0xFF,
0xFF,0xE3,0xC9,0x88,0x9A,0xB1,0xC1,0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x1F,0x1F,0x3F,
0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x07,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0xE0,0xFE,0xFF,0xFE,0xFB,0xFC,0xFF,0xFF,0xFF,0xFF,0x3F,0x0F,0x03,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x07,0xFC,0xF8,0xF0,0xF0,0xF0,0xE0,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,
0x07,0xEF,0xFF,0x0F,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x7C,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0xFF,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC3,0xFE,0x3E,0x1C,0x0C,0x06,0x03,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x07,0xFF,0xC3,0x03,0x43,0xC7,0x87,0x87,0x87,0x03,0x01,0x00,0x00,0x00,0x00,
0x00,0x00,0x01,0x01,0xF3,0x7F,0x07,0x07,0x07,0x03,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x0F,0x1F,0x3F,0xFF,0x7F,0x9F,0x9F,0x1F,0x07,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0xE0,0xFF,0x07,0x07,0x07,0x03,0x01,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x80,0xBF,0xE1,0xC0,0x80,0x80,0x80,0x80,0x80,0x80,0xE4,0xBC,0x88,0x88,0xF8,0xC8,
0x80,0x80,0x80,0x80,0x80,0xC0,0xC0,0xF8,0xCF,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x01,0x1F,0x38,0x60,0x40,0x40,0x00,0x0C,0x30,0xC0,0x38,
0x04,0x38,0xC0,0x30,0x0C,0x00,0x0C,0x30,0xC0,0x38,0x04,0x38,0xC0,0x30,0x0C,0x00,
0x0C,0x30,0xC0,0x38,0x04,0x38,0xC0,0x30,0x0C,0x00,0x00,0x80,0x00,0xFF,0x00,0x78,
0x84,0x84,0x84,0x48,0x00,0x78,0x84,0x84,0x48,0xFF,0x00,0x20,0x20,0x20,0x00,0x78,
0x84,0x84,0x84,0x48,0x00,0xFF,0x08,0x04,0x04,0xF8,0x00,0xFD,0x00,0xFC,0x04,0x04,
0x04,0xF8,0x00,0x68,0x94,0x94,0x54,0xF8,0x00,0x00,0x80,0x00,0x78,0x84,0x84,0x84,
0x48,0x00,0x78,0x84,0x84,0x84,0x78,0x00,0xFC,0x08,0x04,0xFC,0x04,0x04,0xF8,0x00,
0xC0,0x80,0x80,0x80,0xC0,0x40,0x60,0x31,0x0F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
]
int0=0;
key_add=0;
key_dec=0
Contrast_level=45;
log=0;

reverse = [0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0, 0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,
                      0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8, 0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,
                      0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4, 0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,
                      0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC, 0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,
                      0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2, 0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,
                      0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA, 0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,
                      0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6, 0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,
                      0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE, 0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,
                      0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1, 0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,
                      0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9, 0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,
                      0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5, 0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,
                      0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED, 0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,
                      0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3, 0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,
                      0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB, 0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,
                      0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7, 0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,
                      0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF, 0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF]

class MCP(object):
    def __init__(self):
        self.Contrast_level = 40
        self.var = []
        self.var2 = ""

        self.last_dc = False
        #initialize mcp
        self.dev = MCP2210(0x04D8, 0x00DE)
        #gpio
        self._gpio = self.dev.gpio
        self._gpio_direction = self.dev.gpio_direction
        #default seignation pins
        self.gpio_designations()
        #spi setting
        self.spi_designations()
        
        #reset display
        self.reset_display()

        #init display
        self.init_display()

    def reset_display(self):
        self._gpio[2] = False
        time.sleep(0.1)
        self._gpio[2] = True

    def gpio_designations(self):
        self.settings = self.dev.chip_settings
        self.settings.pin_designations[0] = 0x00
        self.settings.pin_designations[1] = 0x00
        self.settings.pin_designations[2] = 0x00
        self.settings.pin_designations[3] = 0x01

        self.settings.pin_designations[4] = 0x00
        self.settings.pin_designations[5] = 0x00
        self.settings.pin_designations[6] = 0x00
        self.settings.pin_designations[7] = 0x00
        self.settings.pin_designations[8] = 0x00
        self.dev.chip_settings = self.settings

        for i in range(0,9):
            if i == 4 or i == 5 or i == 6 or i == 7 or i == 8:
                self._gpio_direction[i] = 1
            else:
                self._gpio_direction[i] = 0
        for i in range(0,9):
            if i != 4 or i != 5 or i != 6 or i != 7 or i != 8:
                self._gpio[i] = 0

    def joystick(self):
        #joystick
        #load gpio setting
        gpio = self._gpio

        if not gpio[4]:
            print('prostredni')
        elif gpio[5]:
            print('doprava')
        elif gpio[6]:
            print('doleva')
        elif gpio[7]:
            print('nahoru')
        elif gpio[8]:
            print('dolu')

    def spi_designations(self):
        spisettings = self.dev.transfer_settings

        spisettings.bit_rate = 1000000
        spisettings.idle_cs = 0b000001000
        spisettings.active_cs = 0b000000000
        spisettings.spi_mode = 0x00
        spisettings.interbyte_delay = 0
        spisettings.cs_data_delay = 0
        spisettings.lb_cs_delay = 0
        self.dev.transfer_settings = spisettings


    def init_display(self):
        self.WriteCommand(0xab)  #Built-in Oscillator ON]
        self.WriteCommand(0xa0)    #s1-s132    
        self.WriteCommand(0xc8)        #c64-c1
        self.WriteCommand(0xa2)        #1/9bias
        self.WriteCommand(0x2c)        #VC ON
        self.WriteFromBuffer()
        time.sleep(0.01)      #Delay >1ms
        self.WriteCommand(0x2e, True)        #VR ON
        time.sleep(0.01)      #Delay >1ms
        self.WriteCommand(0x2f, True)        #VF ON
        time.sleep(0.01)      #Delay >1ms
        self.WriteCommand(0x20)        #Regulor_Resistor_Select
        self.WriteCommand(0x81)        #Set Reference Voltage Select Mode
        self.WriteCommand(38) #Set Reference Voltage Register
        self.WriteCommand(0x70)        #external capacitor
        self.WriteCommand(0x40)    #set start line
        self.WriteCommand(0xaf)    #display on
        self.WriteCommand(0x90)
        self.WriteCommand(0x00)
        self.WriteFromBuffer()

    def WriteCommand(self, data, ty = False):
        # Set DC low for command, high for data.
        if self.last_dc != False:
            self._gpio[1] = False
            self.last_dc = False
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]

        if ty == True:
            self.WriteByteNow([chr(x) for x in data])
        else:
            self.WriteByte([chr(x) for x in data])

    def WriteData(self, data):
        # Set DC low for command, high for data.
        if self.last_dc != True:
            self._gpio[1] = True
            self.last_dc = True
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]

        #self.WriteByte([chr(reverse[x]) for x in data])
        self.WriteByte([chr(x) for x in data])

    def WriteByteNow(self, dat):
        self.dev.transfer("".join(dat))

    def WriteByte(self, dat):
        self.var2 += "".join(dat)

    def WriteFromBuffer(self, a=False):
        self.dev.transfer(self.var2)
        self.var2 = ""

    def Set_Page_Address(self, add):
        add=0xb0|add
        self.WriteCommand(add)

    def Set_Column_Address(self, add):
        self.WriteCommand((0x10|(add>>4)))
        self.WriteCommand((0x0f&add))

    def Display_Picture(self, pic):
        for i in range(0, 0x08):
            self.Set_Page_Address(i)
            self.Set_Column_Address(0x00)
            self.WriteFromBuffer("c")

            self.WriteData(pic[i*192:i*192+192])
            self.WriteFromBuffer('d')
        
        return

    def plot(self, data):
        #time.sleep(0.01)

        self.WriteCommand(0xa6)
        self.WriteCommand(0xa4)
        self.WriteFromBuffer()

        d = [0]*192
        d[0] = 0xff
        self.Display_Picture(data[::-1])
        return
        while 1:
            self.Display_Picture(data[::-1])
            # self.Display_Picture(pic1[::-1])
            # self.Display_Picture(pic2[::-1])
            while 1:
                test.joystick()

test = MCP()
#main program
image = Image.new('1', (192, 64))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('fonts/arial.ttf', 10)
draw.text((0,-2), 'Hello test test test test', font=font, fill = 1)

font = ImageFont.truetype('fonts/time_new_roman.ttf', 10)
draw.text((0,15), 'Hello test test test test', font=font, fill = 1)

font = ImageFont.truetype('fonts/EHSMB.ttf', 7)
draw.text((0,30), 'Hello test test test test', font=font, fill = 1)
data = image.load()

font = ImageFont.truetype('fonts/open24.ttf', 12)
draw.text((0,45), 'Hello test test test test', font=font, fill = 1)
data = image.load()

#parse data
d = [""]*1536
page = 0
for i in range(0, 64):
    if i%8 == 0 and i != 0:
        page += 1
    for c in range(0, 192):
        d[(page * 192) + c] += str(data[(c,i)])

data = [int(i,2) for i in d]


test.plot(data)