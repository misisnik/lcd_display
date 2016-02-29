#4line test
#lib for ili9341 and MCP2210
import numbers
import time
import numpy as np

from PIL import Image
from PIL import ImageDraw

from mcp2210.commands import ChipSettings, SPISettings, USBSettings
from mcp2210.device import MCP2210, CommandException

# Constants for interacting with display registers.
ILI9341_TFTWIDTH    = 240
ILI9341_TFTHEIGHT   = 320

ILI9341_NOP         = 0x00
ILI9341_SWRESET     = 0x01
ILI9341_RDDID       = 0x04
ILI9341_RDDST       = 0x09

ILI9341_SLPIN       = 0x10
ILI9341_SLPOUT      = 0x11
ILI9341_PTLON       = 0x12
ILI9341_NORON       = 0x13

ILI9341_RDMODE      = 0x0A
ILI9341_RDMADCTL    = 0x0B
ILI9341_RDPIXFMT    = 0x0C
ILI9341_RDIMGFMT    = 0x0A
ILI9341_RDSELFDIAG  = 0x0F

ILI9341_INVOFF      = 0x20
ILI9341_INVON       = 0x21
ILI9341_GAMMASET    = 0x26
ILI9341_DISPOFF     = 0x28
ILI9341_DISPON      = 0x29

ILI9341_CASET       = 0x2A
ILI9341_PASET       = 0x2B
ILI9341_RAMWR       = 0x2C
ILI9341_RAMRD       = 0x2E

ILI9341_PTLAR       = 0x30
ILI9341_MADCTL      = 0x36
ILI9341_PIXFMT      = 0x3A

ILI9341_FRMCTR1     = 0xB1
ILI9341_FRMCTR2     = 0xB2
ILI9341_FRMCTR3     = 0xB3
ILI9341_INVCTR      = 0xB4
ILI9341_DFUNCTR     = 0xB6

ILI9341_PWCTR1      = 0xC0
ILI9341_PWCTR2      = 0xC1
ILI9341_PWCTR3      = 0xC2
ILI9341_PWCTR4      = 0xC3
ILI9341_PWCTR5      = 0xC4
ILI9341_VMCTR1      = 0xC5
ILI9341_VMCTR2      = 0xC7

ILI9341_RDID1       = 0xDA
ILI9341_RDID2       = 0xDB
ILI9341_RDID3       = 0xDC
ILI9341_RDID4       = 0xDD

ILI9341_GMCTRP1     = 0xE0
ILI9341_GMCTRN1     = 0xE1

ILI9341_PWCTR6      = 0xFC

ILI9341_BLACK       = 0x0000
ILI9341_BLUE        = 0x001F
ILI9341_RED         = 0xF800
ILI9341_GREEN       = 0x07E0
ILI9341_CYAN        = 0x07FF
ILI9341_MAGENTA     = 0xF81F
ILI9341_YELLOW      = 0xFFE0  
ILI9341_WHITE       = 0xFFFF

def color565(r, g, b):
    """Convert red, green, blue components to a 16-bit 565 RGB value. Components
    should be values 0 to 255.
    """
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def image_to_data(image):
    """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
    #NumPy is much faster at doing this. NumPy code provided by:
    #Keith (https://www.blogger.com/profile/02555547344016007163)
    pb = np.array(image.convert('RGB')).astype('uint16')
    color = ((pb[:,:,0] & 0xF8) << 8) | ((pb[:,:,1] & 0xFC) << 3) | (pb[:,:,2] >> 3)
    return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()

class MCP(object):
    def __init__(self, width=ILI9341_TFTWIDTH, height=ILI9341_TFTHEIGHT):
        self.width = width
        self.height = height
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
        self.buffer = Image.new('RGB', (width, height))

    def reset_display(self):
        self._gpio[2] = False
        time.sleep(0.02)
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

        spisettings.bit_rate = 110000000
        spisettings.idle_cs = 0b000001000
        spisettings.active_cs = 0b000000000
        spisettings.spi_mode = 0x00

        self.dev.transfer_settings = spisettings


    def init_display(self):
        # Initialize the display.  Broken out as a separate function so it can
        # be overridden by other displays in the future.
        self.WriteCommand(0xEF,True)
        self.WriteData(0x03)
        self.WriteData(0x80)
        self.WriteData(0x02)
        self.WriteFromBuffer()
        self.WriteCommand(0xCF,True)
        self.WriteData(0x00)
        self.WriteData(0XC1)
        self.WriteData(0X30)
        self.WriteFromBuffer()
        self.WriteCommand(0xED,True)
        self.WriteData(0x64)
        self.WriteData(0x03)
        self.WriteData(0X12)
        self.WriteData(0X81)
        self.WriteFromBuffer()
        self.WriteCommand(0xE8,True)
        self.WriteData(0x85)
        self.WriteData(0x00)
        self.WriteData(0x78)
        self.WriteFromBuffer()
        self.WriteCommand(0xCB,True)
        self.WriteData(0x39)
        self.WriteData(0x2C)
        self.WriteData(0x00)
        self.WriteData(0x34)
        self.WriteData(0x02)
        self.WriteFromBuffer()
        self.WriteCommand(0xF7,True)
        self.WriteData(0x20)
        self.WriteFromBuffer()
        self.WriteCommand(0xEA,True)
        self.WriteData(0x00)
        self.WriteData(0x00)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_PWCTR1,True)    # Power control 
        self.WriteData(0x23)                 # VRH[5:0] 
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_PWCTR2,True)    # Power control 
        self.WriteData(0x10)                 # SAP[2:0];BT[3:0] 
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_VMCTR1,True)    # VCM control 
        self.WriteData(0x3e)
        self.WriteData(0x28)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_VMCTR2,True)    # VCM control2 
        self.WriteData(0x86)                 # --
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_MADCTL,True)    #  Memory Access Control 
        self.WriteData(0x48)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_PIXFMT,True)
        self.WriteData(0x55)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_FRMCTR1,True)
        self.WriteData(0x00)
        self.WriteData(0x18)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_DFUNCTR,True)   #  Display Function Control 
        self.WriteData(0x08)
        self.WriteData(0x82)
        self.WriteData(0x27)
        self.WriteFromBuffer()
        self.WriteCommand(0xF2,True)              #  3Gamma Function Disable 
        self.WriteData(0x00)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_GAMMASET,True)  # Gamma curve selected 
        self.WriteData(0x01)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_GMCTRP1,True)   # Set Gamma 
        self.WriteData(0x0F)
        self.WriteData(0x31)
        self.WriteData(0x2B)
        self.WriteData(0x0C)
        self.WriteData(0x0E)
        self.WriteData(0x08)
        self.WriteData(0x4E)
        self.WriteData(0xF1)
        self.WriteData(0x37)
        self.WriteData(0x07)
        self.WriteData(0x10)
        self.WriteData(0x03)
        self.WriteData(0x0E)
        self.WriteData(0x09)
        self.WriteData(0x00)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_GMCTRN1,True)   # Set Gamma 
        self.WriteData(0x00)
        self.WriteData(0x0E)
        self.WriteData(0x14)
        self.WriteData(0x03)
        self.WriteData(0x11)
        self.WriteData(0x07)
        self.WriteData(0x31)
        self.WriteData(0xC1)
        self.WriteData(0x48)
        self.WriteData(0x08)
        self.WriteData(0x0F)
        self.WriteData(0x0C)
        self.WriteData(0x31)
        self.WriteData(0x36)
        self.WriteData(0x0F)
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_SLPOUT,True)    # Exit Sleep 
        time.sleep(0.120)
        self.WriteCommand(ILI9341_DISPON,True)    # Display on 

    def WriteCommand(self, data, ty = False):
        # Set DC low for command, high for data.
        self._gpio[1] = False
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]

        if ty == True:
            self.WriteByteNow([chr(x) for x in data])
        else:
            self.WriteByte([chr(x) for x in data])

        """
        # Write data a chunk at a time.
        for start in range(0, len(data), chunk_size):
            end = min(start+chunk_size, len(data))
            self._spi.write(data[start:end])
        """

    def WriteData(self, data):
        # Set DC low for command, high for data.
        self._gpio[1] = True
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]

        self.WriteByte([chr(x) for x in data])

    def WriteByteNow(self, dat):
        self.dev.transfer("".join(dat))

    def WriteByte(self, dat):
        self.var2 += "".join(dat)

    def WriteFromBuffer(self):
        self.dev.transfer(self.var2)
        self.var2 = ""

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1 
        should define the minimum and maximum y pixel bound.  If no parameters 
        are specified the default will be to update the entire display from 0,0
        to 239,319.
        """
        if x1 is None:
            x1 = self.width-1
        if y1 is None:
            y1 = self.height-1
        self.WriteCommand(ILI9341_CASET, True)     # Column addr set
        self.WriteData(x0 >> 8)
        self.WriteData(x0)                   # XSTART 
        self.WriteData(x1 >> 8)
        self.WriteData(x1)                   # XEND
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_PASET, True)     # Row addr set
        self.WriteData(y0 >> 8)
        self.WriteData(y0)                   # YSTART
        self.WriteData(y1 >> 8)
        self.WriteData(y1)                   # YEND
        self.WriteFromBuffer()
        self.WriteCommand(ILI9341_RAMWR, True)     # write to RAM

    def display(self, image=None):
        """Write the display buffer or provided image to the hardware.  If no
        image parameter is provided the display buffer will be written to the
        hardware.  If an image is provided, it should be RGB format and the
        same dimensions as the display hardware.
        """
        # By default write the internal buffer to the display.
        if image is None:
            image = self.buffer
        # Set address bounds to entire display.
        self.set_window()
        # Convert image to array of 16bit 565 RGB data bytes.
        # Unfortunate that this copy has to occur, but the SPI byte writing
        # function needs to take an array of bytes and PIL doesn't natively
        # store images in 16-bit 565 RGB format.
        pixelbytes = list(image_to_data(image))
        # Write data to hardware.
        self.WriteData(pixelbytes)
        self.WriteFromBuffer()

    def clear(self, color=(0,0,0)):
        """Clear the image buffer to the specified RGB color (default black)."""
        width, height = self.buffer.size
        self.buffer.putdata([color]*(width*height))

    def draw(self):
        """Return a PIL ImageDraw instance for 2D drawing on the image buffer."""
        return ImageDraw.Draw(self.buffer)

test = MCP()
# Load an image.
print('Loading image...')
image = Image.open('lena.jpg')

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(180).resize((240, 320))

# Draw the image on the display hardware.
print('Drawing image')
test.display(image)