import numbers
import time

from mcp2210.commands import ChipSettings, SPISettings, USBSettings
from mcp2210.device import MCP2210, CommandException


picture = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x9F,0x10,0xCF,0xBC,0x46,0x24,0x47,0x07,0xDF,0x38,0x88,0x1C,0x38,0x02,0x3E,0xF1,
0x90,0x29,0x22,0x22,0x49,0x26,0x48,0x81,0x10,0x44,0x88,0x22,0x44,0x02,0x08,0x89,
0x90,0x29,0x02,0x22,0x48,0x26,0x48,0x01,0x10,0x40,0x88,0x20,0x44,0x02,0x08,0x89,
0x9F,0x44,0xC2,0x3C,0x46,0x25,0x49,0x81,0x1F,0x40,0xF8,0x20,0x44,0x02,0x08,0x89,
0x90,0x7C,0x22,0x24,0x41,0x24,0xC8,0x81,0x10,0x40,0x88,0x20,0x44,0x02,0x08,0x89,
0x90,0x45,0x22,0x22,0x49,0x24,0xC8,0x81,0x10,0x44,0x88,0x22,0x44,0x02,0x08,0x89,
0x9F,0x82,0xC2,0x22,0x46,0x24,0x47,0x01,0x1F,0x38,0x89,0x1C,0x38,0xB3,0xC8,0xF1,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x10,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x3E,0x00,0xD9,0x06,0x00,0x0F,0x30,0x60,0x00,0x00,0x00,0x0E,0x00,0x02,0x01,
0x80,0x33,0x00,0x1B,0x00,0x00,0x19,0xB0,0x00,0x00,0x00,0x00,0x18,0x00,0x06,0x01,
0x80,0x33,0x66,0xDF,0x86,0xF8,0x30,0x3E,0x6F,0x8F,0x1E,0x3C,0x3C,0xF3,0xEF,0x01,
0x80,0x3E,0x66,0xDB,0x06,0xCC,0x30,0x33,0x6C,0xD9,0xB3,0x66,0x19,0x9B,0x36,0x01,
0x80,0x33,0x66,0xDB,0x06,0xCC,0x30,0x33,0x6C,0xDF,0xBC,0x7E,0x19,0x9B,0x36,0x01,
0x80,0x33,0x66,0xDB,0x06,0xCC,0x30,0x33,0x6C,0xD8,0x0F,0x60,0x19,0x9B,0x36,0x01,
0x80,0x33,0x66,0xDB,0x06,0xCC,0x19,0xB3,0x6C,0xD9,0xB3,0x66,0x19,0x9B,0x36,0x01,
0x80,0x3E,0x3E,0xD9,0x86,0xCC,0x0F,0x33,0x6C,0xCF,0x1E,0x3C,0x18,0xF3,0x33,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xE0,0x00,0x00,0x01,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x00,0x01,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x00,0x01,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x00,0x01,
0x80,0x00,0x00,0x41,0xF7,0xC3,0xC3,0x1C,0x71,0xC1,0x80,0x70,0x20,0x00,0x00,0x01,
0x80,0x00,0x00,0x41,0x86,0x66,0x67,0x36,0xDB,0x63,0x80,0xD8,0x20,0x00,0x00,0x01,
0x80,0x00,0x00,0x41,0x86,0x6C,0x0F,0x06,0xDB,0x05,0x80,0xC0,0x20,0x00,0x00,0x01,
0x80,0x00,0x00,0x41,0xF6,0x6C,0x0B,0x06,0x73,0xC5,0x80,0xF0,0x26,0x00,0x40,0x01,
0x80,0x00,0x00,0x41,0x87,0xCC,0x03,0x0C,0xDB,0x69,0x9E,0xD8,0x29,0x00,0x00,0x01,
0x80,0x00,0x00,0x41,0x86,0xCC,0x03,0x18,0xDB,0x6F,0xC0,0xD8,0x28,0x33,0x4C,0x71,
0x80,0x00,0x00,0x41,0x86,0x66,0x63,0x30,0xDB,0x61,0x80,0xD8,0x26,0x4A,0x52,0x81,
0x80,0x00,0x00,0x41,0xF6,0x33,0xC3,0x3E,0x71,0xC1,0x80,0x70,0x21,0x7A,0x5E,0x61,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x29,0x42,0x50,0x11,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x26,0x3A,0x4E,0xE1,
0x80,0x00,0x00,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xE0,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x81,0x9B,0xE6,0x01,0x80,0x00,0x00,0x1B,0x00,0x01,0x80,0x00,0x00,0x00,0x00,0x01,
0x81,0x9B,0x36,0x01,0x80,0x00,0x00,0x18,0x00,0x01,0x80,0x00,0x00,0x00,0x00,0x01,
0x81,0x9B,0x36,0x0D,0xF3,0x3C,0x60,0xFB,0x3C,0xF9,0x9D,0x8C,0x38,0xF3,0xFE,0x01,
0x81,0x9B,0x36,0x0D,0x9B,0x36,0xC1,0x9B,0x66,0xCD,0xA6,0xD8,0x6D,0x9B,0x33,0x01,
0x81,0x9B,0xE6,0x01,0x9B,0x36,0xC1,0x9B,0x78,0xCD,0x9E,0xD8,0x61,0x9B,0x33,0x01,
0x81,0x9B,0x66,0x01,0x9B,0x36,0xDD,0x9B,0x1E,0xCD,0xB6,0xD8,0x61,0x9B,0x33,0x01,
0x81,0x9B,0x36,0x0D,0x9B,0x33,0x81,0x9B,0x66,0xCD,0xB6,0x73,0x6D,0x9B,0x33,0x01,
0x80,0xF3,0x1F,0xED,0xF1,0xF3,0x80,0xFB,0x3C,0xF9,0x9E,0x73,0x38,0xF3,0x33,0x01,
0x80,0x00,0x00,0x00,0x00,0x03,0x00,0x00,0x00,0xC0,0x00,0x60,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x0E,0x00,0x00,0x00,0xC0,0x01,0xC0,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

picture2 = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x04,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x06,0x00,0x06,0x03,0x80,0x00,0x01,
0x80,0x00,0x00,0xC0,0x00,0x00,0x00,0x00,0x00,0x0E,0x00,0x1F,0x07,0xFF,0xC0,0x01,
0x80,0x00,0x01,0xE0,0x00,0x00,0x00,0x00,0x00,0x1E,0x00,0x3F,0x9F,0x39,0xC0,0x01,
0x80,0x00,0x01,0xE0,0x00,0x00,0x00,0x00,0x00,0x1E,0x00,0x7F,0xF0,0x01,0x80,0x01,
0x80,0x00,0x03,0xE4,0x00,0x00,0x00,0x00,0x00,0x1F,0x00,0xFF,0xE0,0x00,0xC0,0x01,
0x80,0x00,0x07,0xEF,0xC0,0x00,0x00,0x00,0x00,0x3F,0x00,0xFF,0xF0,0x00,0xE1,0xE1,
0x80,0x00,0x0F,0xEF,0xFE,0x00,0x00,0x00,0x00,0x3F,0x01,0xFF,0xE0,0x00,0xF7,0xF1,
0x80,0x00,0x0F,0xE7,0xFF,0xE0,0x00,0x00,0x00,0x77,0x01,0xFF,0xF0,0x00,0xFF,0xF1,
0x80,0x00,0x07,0xE7,0x3F,0xFE,0x00,0x00,0x00,0x59,0x01,0xFF,0xFC,0x01,0x8F,0xF9,
0x80,0x00,0x07,0xE7,0x07,0xFF,0xF0,0x00,0x00,0xFD,0x00,0xFF,0x8E,0x3F,0xEF,0xF9,
0x80,0x00,0x07,0xE7,0x00,0xFF,0xFE,0x00,0x01,0xE7,0x80,0xFF,0xF7,0xFC,0x77,0xF9,
0x80,0x00,0x07,0xF7,0x00,0x1F,0xFE,0x00,0x07,0xF7,0x80,0x77,0xFB,0xFF,0xF7,0xF9,
0x80,0x00,0x03,0xF7,0x00,0x03,0xFE,0x00,0x07,0xFF,0x80,0x27,0xFE,0x7F,0xF3,0xF1,
0x80,0x00,0x03,0xF7,0x00,0x00,0x7E,0x00,0x00,0x01,0x80,0x27,0xFE,0x7F,0xF1,0xF1,
0x80,0x00,0x03,0xF3,0x00,0x00,0x1C,0x00,0x00,0x00,0xC0,0x41,0xFC,0x3F,0xF1,0xE1,
0x80,0x00,0x01,0xF3,0x00,0x00,0x1C,0x00,0x00,0x00,0xC0,0xC1,0xF0,0x1F,0xE1,0x01,
0x80,0xC0,0x01,0xF3,0x80,0x00,0x1C,0x00,0x00,0x00,0x40,0x87,0xE0,0x03,0x01,0x01,
0x80,0xF8,0x01,0xF3,0x80,0x00,0x3C,0x00,0x00,0x00,0x61,0x9F,0xF0,0x1C,0x01,0x81,
0x80,0x7F,0x00,0xF3,0x80,0x00,0x3C,0x00,0x00,0x00,0x7F,0xBF,0xF0,0x7F,0x01,0x81,
0x80,0x7F,0xC0,0xF3,0x80,0x00,0x38,0x00,0x00,0x00,0x63,0x7E,0x70,0x7F,0xC1,0x81,
0x80,0x3F,0xF8,0xF3,0x80,0x00,0x38,0x00,0x00,0x00,0xF3,0xFD,0xF0,0xFF,0xE1,0x81,
0x80,0x3F,0xFE,0xF9,0x80,0x00,0x38,0x00,0x00,0x01,0xBE,0xFF,0x60,0xE7,0xE1,0x81,
0x80,0x1D,0xFF,0x79,0x80,0x00,0x78,0x00,0x00,0x01,0x1E,0xFE,0x60,0xF7,0xE1,0x01,
0x80,0x1C,0x3F,0x79,0x80,0x00,0x70,0x00,0x00,0x01,0x1E,0xFC,0x80,0x97,0xF1,0x81,
0x80,0x1C,0x07,0x79,0x80,0x00,0x70,0x00,0x00,0x01,0x8E,0xFF,0x80,0x07,0xE1,0x81,
0x80,0x0E,0x00,0x39,0x80,0x00,0x70,0x00,0x00,0x00,0xC6,0x7F,0xE0,0x7F,0xE1,0x81,
0x80,0x0E,0x00,0x39,0xC0,0x00,0x70,0x00,0x00,0x00,0xEE,0x3E,0xE0,0x7F,0xE1,0x81,
0x80,0x06,0x00,0x39,0xC0,0x00,0x60,0x00,0x00,0x00,0x7E,0x00,0x40,0x1F,0xC1,0x81,
0x80,0x07,0x00,0x18,0xC0,0x00,0xE0,0x00,0x00,0x00,0x0F,0x00,0x00,0x07,0x03,0x01,
0x80,0x03,0x00,0x18,0xC0,0x00,0xE0,0x00,0x00,0x00,0x07,0x80,0x00,0x00,0x07,0x01,
0x80,0x03,0x00,0x1C,0xC0,0x00,0xE0,0x00,0x00,0x00,0x02,0xC3,0xF8,0x00,0x06,0x01,
0x80,0x01,0x80,0x1C,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x03,0x61,0xF0,0x00,0x0C,0x01,
0x80,0x01,0x80,0x0C,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x03,0x30,0x00,0x00,0x38,0x01,
0x80,0x00,0x80,0x0C,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x01,0x9C,0x00,0x00,0x70,0x01,
0x80,0x00,0x80,0x0C,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x87,0x00,0x01,0xC0,0x01,
0x80,0x00,0x00,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC7,0xFC,0x7F,0xC0,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xCF,0x1F,0xFF,0xE0,0x01,
0x87,0xE0,0x00,0x02,0x3F,0x0C,0x00,0xC0,0x00,0x00,0x00,0x6E,0x00,0x3B,0xE0,0x01,
0x86,0x00,0x00,0x06,0x31,0x80,0x00,0x00,0x00,0x00,0x00,0x38,0x00,0x30,0xE0,0x01,
0x86,0x03,0xC3,0xCF,0x31,0x8C,0x78,0xCD,0x86,0xC0,0x00,0x38,0x00,0x30,0x60,0x01,
0x86,0x04,0x66,0x66,0x31,0x8C,0xCC,0xCE,0xCD,0xC0,0x00,0x10,0x00,0x38,0x20,0x01,
0x87,0xE1,0xE7,0x06,0x3F,0x0C,0xE0,0xCC,0xCC,0xC0,0x00,0x30,0x00,0x0C,0x30,0x01,
0x86,0x03,0x63,0xC6,0x33,0x0C,0x78,0xCC,0xCC,0xC0,0x00,0x30,0x00,0x04,0x18,0x01,
0x86,0x06,0x60,0xE6,0x31,0x8C,0x1C,0xCC,0xCC,0xC0,0x00,0x30,0x00,0x06,0x18,0x01,
0x86,0x06,0x66,0x66,0x31,0x8C,0xCC,0xCC,0xCD,0xC0,0x00,0x20,0x00,0x03,0x0C,0x01,
0x87,0xE3,0xE3,0xC3,0x30,0xCC,0x78,0xCC,0xC6,0xC0,0x00,0x20,0x00,0x02,0x08,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x08,0xC0,0x00,0x20,0x00,0x02,0x08,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x07,0x80,0x00,0x20,0x00,0x03,0x98,0x01,
0xBF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xF0,0x00,0x20,0x00,0x01,0xF0,0x01,
0xBF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xF0,0x00,0x20,0x00,0x01,0xE0,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x01,0xC0,0x01,
0xA0,0x00,0x00,0x28,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x20,0x00,0x01,0x80,0x01,
0xA0,0x00,0x00,0x20,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x30,0x00,0x03,0x00,0x01,
0xBC,0x8A,0x21,0xE8,0xEF,0x27,0x22,0x18,0xE7,0x60,0x00,0x30,0x00,0x03,0x00,0x01,
0xA2,0x89,0x42,0x29,0x08,0xA0,0x94,0x25,0x14,0x90,0x00,0x30,0x00,0x02,0x00,0x01,
0xA2,0x89,0x5A,0x28,0xC8,0xA3,0x94,0x21,0x14,0x90,0x00,0x10,0xFC,0x02,0x00,0x01,
0xA2,0x89,0x42,0x28,0x28,0xA4,0x94,0x25,0x14,0x90,0x00,0x10,0x3C,0x06,0x00,0x01,
0xBC,0x78,0x81,0xE9,0xCF,0x23,0x88,0x98,0xE4,0x90,0x00,0x18,0x08,0x06,0x00,0x01,
0x80,0x00,0x80,0x00,0x08,0x00,0x08,0x00,0x00,0x00,0x00,0x18,0x08,0x06,0x00,0x01,
0x80,0x03,0x00,0x00,0x08,0x00,0x30,0x00,0x00,0x00,0x00,0x0C,0x18,0x0C,0x00,0x01,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x07,0xFF,0x3C,0x00,0x01,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,]

picture3 = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x60,0x00,0x60,0x38,0x00,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x60,0x01,0xF8,0x77,0xF8,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0xE0,0x03,0xFB,0x00,0x18,0x00,0x00,0x80,0x00,0x00,0x07,0x00,0x20,0x00,0x01,
0x80,0xE0,0x07,0xFE,0x00,0x08,0x00,0x00,0x80,0x00,0x00,0x0F,0x80,0x20,0x00,0x01,
0x81,0xE0,0x0F,0xFF,0x00,0x04,0x18,0x00,0x80,0x00,0x00,0x0F,0xC0,0x20,0x00,0x01,
0x81,0xF0,0x0F,0xFA,0x00,0x1C,0x7C,0x00,0x80,0x00,0x00,0x0F,0xC0,0x20,0x00,0x01,
0x83,0x30,0x0F,0xE2,0x00,0x0B,0x7E,0x00,0x80,0x00,0x00,0x0F,0xE0,0x20,0x00,0x01,
0x82,0x90,0x0F,0xFF,0x80,0x08,0xFF,0x00,0x80,0x03,0x00,0x0F,0xE0,0x20,0x00,0x01,
0x86,0x98,0x0F,0xF9,0xC0,0x78,0xFF,0x00,0x80,0x07,0x80,0x7F,0xE0,0x20,0x00,0x01,
0x8E,0x18,0x07,0xFC,0x3F,0xCE,0x7F,0x00,0x80,0x07,0xC3,0xC3,0xE0,0x20,0x00,0x01,
0xBF,0x38,0x03,0xFF,0x9F,0xF3,0x7F,0x00,0x80,0x07,0xCC,0x00,0x38,0x20,0x00,0x01,
0xBF,0xF8,0x02,0x7F,0x87,0xFD,0x3F,0x00,0x80,0x0F,0xF0,0x00,0x06,0x20,0x00,0x01,
0x8F,0xF8,0x02,0x3F,0xE7,0xFD,0x3E,0x00,0x80,0x0F,0xC0,0x00,0x01,0xA0,0x00,0x01,
0x80,0x04,0x04,0x1F,0xC3,0xFE,0x3C,0x00,0x80,0x0F,0x80,0x00,0x00,0xE0,0x00,0x01,
0x80,0x04,0x04,0x0F,0x81,0xFC,0x10,0x00,0x80,0x07,0x00,0x10,0x3F,0xE0,0x00,0x01,
0x80,0x04,0x04,0x7C,0x00,0x00,0x10,0x00,0x80,0x06,0x00,0x20,0xFF,0xF0,0x00,0x01,
0x80,0x02,0x08,0xFE,0x00,0x00,0x10,0x00,0x80,0x04,0x18,0x01,0xFF,0xFC,0x00,0x01,
0x80,0x03,0xE9,0xFE,0x03,0xF0,0x10,0x00,0x80,0x08,0x02,0x03,0xFF,0xFC,0x00,0x01,
0x80,0x02,0x33,0xC7,0x07,0xF8,0x10,0x00,0x80,0x10,0x00,0x07,0xFF,0xFE,0x00,0x01,
0x80,0x06,0x37,0x8B,0x04,0xFC,0x10,0x00,0x80,0x10,0x00,0x07,0xFF,0xFF,0x00,0x01,
0x80,0x0B,0xA7,0xBE,0x08,0x7E,0x10,0x00,0x80,0x30,0x00,0x0F,0xFF,0xFD,0x80,0x01,
0x80,0x08,0x47,0x84,0x0F,0x7E,0x10,0x00,0x80,0x20,0x78,0x0F,0xFF,0xE0,0x80,0x01,
0x80,0x08,0x47,0x80,0x01,0xFE,0x10,0x00,0x80,0x23,0xFE,0x0F,0xFF,0x82,0xC0,0x01,
0x80,0x08,0x47,0xC8,0x00,0x7E,0x10,0x00,0x80,0x47,0xFF,0x8F,0xFC,0x0E,0x40,0x01,
0x80,0x08,0x43,0xFC,0x07,0xFE,0x10,0x00,0x80,0x5F,0xFF,0xCF,0xE0,0x7E,0x40,0x01,
0x80,0x06,0x61,0xEE,0x03,0xFE,0x10,0x00,0x80,0x5F,0xFF,0xEF,0x81,0xFE,0x40,0x01,
0x80,0x03,0xE0,0x00,0x01,0xFC,0x10,0x00,0x80,0x7F,0xFF,0xEF,0x0F,0xFE,0x60,0x01,
0x80,0x00,0x70,0x00,0x00,0x78,0x30,0x00,0x80,0xFF,0xFF,0xF7,0x3F,0xFE,0x20,0x01,
0x80,0x00,0x38,0x00,0x00,0x00,0x20,0x00,0x80,0xFF,0xFF,0xC3,0xFF,0xFC,0x20,0x01,
0x80,0x00,0x2C,0x06,0x80,0x00,0x60,0x00,0x80,0xFF,0xFE,0x03,0xFF,0xF8,0x20,0x01,
0x80,0x00,0x36,0x18,0x00,0x00,0xC0,0x00,0x80,0xFF,0xF0,0x39,0xFF,0xF8,0x60,0x01,
0x80,0x00,0x13,0x00,0x00,0x01,0x00,0x00,0x80,0xFF,0xC0,0xF8,0xFF,0xE0,0x40,0x01,
0x80,0x00,0x08,0xC0,0x00,0x06,0x00,0x00,0x80,0xFE,0x07,0xF0,0x3F,0xC0,0x40,0x01,
0x80,0x00,0x08,0x70,0x00,0x1C,0x00,0x00,0x80,0xF8,0x1F,0xF0,0x00,0x00,0xC0,0x01,
0x80,0x00,0x0C,0x7F,0x00,0xFC,0x00,0x00,0x80,0xB8,0xFF,0xF0,0x00,0x00,0x80,0x01,
0x80,0x00,0x04,0xF0,0xFF,0xFE,0x00,0x00,0x80,0xBB,0xFF,0xE0,0x00,0x01,0x00,0x01,
0x80,0x00,0x04,0xE0,0x07,0x9E,0x00,0x00,0x80,0x5F,0xFF,0xE0,0x00,0x02,0x00,0x01,
0x80,0x00,0x02,0xC0,0x07,0x0E,0x00,0x00,0x80,0x5F,0xFF,0xC0,0x00,0x04,0x00,0x01,
0x80,0x00,0x03,0x80,0x07,0x06,0x00,0x00,0x80,0x4F,0xFF,0x80,0x00,0x08,0x00,0x01,
0x80,0x00,0x01,0x00,0x02,0x06,0x00,0x00,0x80,0x23,0xFF,0x00,0x00,0x30,0x00,0x01,
0x80,0x00,0x01,0x00,0x00,0x82,0x00,0x00,0x80,0x20,0xF8,0x1C,0x00,0x60,0x00,0x01,
0x80,0x00,0x01,0x00,0x00,0x01,0x00,0x00,0x80,0x10,0x00,0x00,0x01,0xA0,0x00,0x01,
0x80,0x00,0x03,0x00,0x00,0x41,0x00,0x00,0x80,0x0C,0x00,0x00,0x06,0x23,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x20,0x80,0x00,0x80,0x06,0x00,0x02,0x18,0x27,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x20,0x80,0x00,0x80,0x01,0xC0,0x00,0x60,0x3F,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x00,0x80,0x00,0x80,0x00,0x7C,0x07,0xE0,0x3E,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x20,0x00,0x00,0x80,0x00,0x07,0xFF,0xFF,0xFE,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x38,0x00,0x00,0x80,0x00,0x00,0x7F,0xFF,0xFC,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x1E,0x00,0x00,0x80,0x00,0x00,0x67,0xFF,0xF8,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x1C,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x02,0x00,0x03,0x00,0x00,0x00,0x36,0x00,0x03,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x02,0x00,0x03,0x00,0x00,0x00,0x30,0x00,0x03,0x00,0x00,0x00,0x00,0x01,
0x80,0x00,0x03,0x00,0x03,0xE6,0x78,0xC1,0xF6,0x79,0xF3,0x3B,0x18,0x71,0xE7,0xFD,
0x80,0x00,0x01,0x08,0x03,0x36,0x6D,0x83,0x36,0xCD,0x9B,0x4D,0xB0,0xDB,0x36,0x67,
0x80,0x00,0x01,0x07,0xC3,0x36,0x6D,0x83,0x36,0xF1,0x9B,0x3D,0xB0,0xC3,0x36,0x67,
0x80,0x00,0x01,0x01,0x83,0x36,0x6D,0xBB,0x36,0x3D,0x9B,0x6D,0xB0,0xC3,0x36,0x67,
0x80,0x00,0x00,0x00,0x03,0x36,0x67,0x03,0x36,0xCD,0x9B,0x6C,0xE6,0xDB,0x36,0x67,
0x80,0x00,0x00,0x80,0x83,0xE3,0xE7,0x01,0xF6,0x79,0xF3,0x3C,0xE6,0x71,0xE6,0x67,
0x80,0x00,0x00,0x61,0xC0,0x00,0x06,0x00,0x00,0x01,0x80,0x00,0xC0,0x00,0x00,0x01,
0x80,0x00,0x00,0x1E,0x38,0x00,0x1C,0x00,0x00,0x01,0x80,0x03,0x80,0x00,0x00,0x01,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,]


class MCP(object):
    def __init__(self):
        self.var = []
        self.var2 = ""
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
            self._gpio_direction[i] = 0
        for i in range(0,9):
            self._gpio[i] = 0

    def spi_designations(self):
        spisettings = self.dev.transfer_settings

        spisettings.bit_rate = 3000000
        spisettings.idle_cs = 0b000000000
        spisettings.active_cs = 0b000001000
        spisettings.spi_mode = 0x01

        self.dev.transfer_settings = spisettings


    def init_display(self):
        time.sleep(0.01)
        self.WriteCommand(0x30,True)
        time.sleep(0.0001)
        self.WriteCommand(0x30,True)
        time.sleep(0.00011)
        self.WriteCommand(0x0c,True)
        time.sleep(0.000100)
        self.WriteCommand(0x01,True)
        time.sleep(0.002)
        self.WriteCommand(0x06,True)
        time.sleep(0.00008)
        self.WriteCommand(0x02, True)

    def WriteCommand(self,CMD, ty = False):
        H_data = CMD
        H_data &= 0xf0
        L_data = CMD
        L_data &= 0x0f
        L_data <<= 4

        if ty == True:
            self.WriteByteNow([chr(x) for x in [0xf8,H_data,L_data]])
        else:
            self.WriteByte([chr(x) for x in [0xf8,H_data,L_data]])

    def WriteData(self,CMD):
        H_data = CMD
        H_data &= 0xf0
        L_data = CMD
        L_data &= 0x0f
        L_data <<= 4

        self.WriteByte([chr(x) for x in [0xfa,H_data,L_data]])

    def WriteByteNow(self, dat):
        self.dev.transfer("".join(dat))

    def WriteByte(self, dat):
        self.var2 += "".join(dat)
        if len(self.var2) == -1:
            self.dev.transfer(self.var2)
            self.var2 = ""
    def WriteFromBuffer(self):
        self.dev.transfer(self.var2)
        self.var2 = ""

    def Set_GraphicMode(self):
        self.WriteCommand(0x34)  # Extended instuction set, 8bit
        time.sleep(0.0001)
        self.WriteCommand(0x36)   # Repeat instrution with bit1 set
        time.sleep(0.0001)

    def Clear_Graphics(self):
        for y in range(0,64):
            if y < 32:
                self.WriteCommand(0x80 | y)
                self.WriteCommand(0x80)
            else:
                self.WriteCommand(0x80 | (y-32))
                self.WriteCommand(0x88)

            for x in range(0,16):
                self.WriteData(0x00)

    def WriteString(self, data):
        for i in data:
            self.WriteData(ord(i))

    def plot(self, img,img2,img3):
        
        self.WriteCommand(0x80)    # Setting location to write characters. In this case 0,0 - Top Left Corner
        """
        self.WriteData(0x03)             # Sending a PREDEFINED character as described in ST7920 Datasheet.
        self.WriteData(0x04)             # another one
        self.WriteData(0x05)             # another one
        self.WriteData(0x06)             # and another one.
        """

        #self.WriteCommand(0x90)
        """while 1:
            for i in range(0,1024):
                self.WriteString(str(i))
                self.WriteCommand(0x80)
        
        self.WriteString("ahoj jak se mas")
        self.WriteCommand(0x81)
        self.WriteString("mam se dobre")
        self.WriteCommand(0x90)
        self.WriteString("QWERTY")
        exit()"""
        
        self.Set_GraphicMode()                 # Set the display in Extended mode
        #self.Clear_Graphics()                     # Must send a Clear command otherwise display could be corrupt.
        while 1:
            self.DisplayGraphic(img)
            self.WriteFromBuffer()
            time.sleep(1)
            self.DisplayGraphic(img2)
            self.WriteFromBuffer()
            time.sleep(1)
            self.DisplayGraphic(img3)
            self.WriteFromBuffer()
            time.sleep(1)
        return
        #self.Set_GraphicMode()

        for page in range(0xB0,0xB4):
            self.WriteCommand(page)
            self.WriteCommand(0x10)
            self.WriteCommand(0x04)
            
            i = (0xB3-page)*128
            
            for column in range(0,128):
                self.WriteData(img[i+column])

            self.WriteCommand(0x34)
            self.WriteCommand(0x36)

    def DisplayGraphic(self, data):
        cis = 0
        for i in range(0,32):
            self.WriteCommand(0x80+i)
            self.WriteCommand(0x80)
            for j in range(0,16):
                self.WriteData(data[cis])
                cis += 1

        for i in range(0,32):
            self.WriteCommand(0x80+i)
            self.WriteCommand(0x88)
            for j in range(0,16):
                self.WriteData(data[cis])
                cis += 1

test = MCP()
test.plot(picture,picture2, picture3)