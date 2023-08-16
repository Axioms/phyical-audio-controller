import displayio, busio, json, board, time, terminalio
from adafruit_esp32s2tft import ESP32S2TFT
from adafruit_display_text import bitmap_label

BMP_WIDTH = 40
BMP_PADDING = 8
LABEL_HEIGHT = 40
BMP_HEIGHT = 70
TOTAL_ENCODERS = 5
TIME_INTERVAL = 0.001
labels = []
bmps = []
bmp_inversion_matrix = []
main_window = displayio.Group()
label_group = displayio.Group()
bmp_group = displayio.Group()
# init UART
uart = busio.UART(rx=board.RX, baudrate=1000000,timeout=0)

def padString(string, pad, delim = " "):
    strlen = len(string)
    if strlen > pad:
        string = string[0:pad]
    elif strlen < pad:
        delta = pad - len(string)
        string = (delim * delta) + string
    return string

display = board.DISPLAY

for encoder_index in range(TOTAL_ENCODERS):
    # create Text Label
    tmp_tabel = bitmap_label.Label(terminalio.FONT, scale=2, x=((BMP_WIDTH + BMP_PADDING) * encoder_index), y=LABEL_HEIGHT, text=padString(str(-1), 3))
    labels.append(tmp_tabel)
    label_group.append(tmp_tabel)
    # create image
    bmp_inversion_matrix.append(False)
    tmp_bmp = displayio.OnDiskBitmap("images/" + str(encoder_index) + "." + ("1" if bmp_inversion_matrix[encoder_index] else "0") + ".bmp")
    bmp_display = displayio.TileGrid(tmp_bmp, pixel_shader=tmp_bmp.pixel_shader, x=((BMP_WIDTH + BMP_PADDING) * encoder_index), y=BMP_HEIGHT)
    bmps.append(bmp_display)
    bmp_group.append(bmp_display)

main_window.append(label_group)
main_window.append(bmp_group)

display.show(main_window)

def ChangeVolume(encoder, volume):
    labels[encoder].text = padString(str(volume), 3)

def ToggleMute(encoder):
    bmp_inversion_matrix[encoder] = not bmp_inversion_matrix[encoder]
    tmp_bmp = displayio.OnDiskBitmap("images/" + str(encoder) + "." + ("1" if bmp_inversion_matrix[encoder] else "0") + ".bmp")
    bmp_display = displayio.TileGrid(tmp_bmp, pixel_shader=tmp_bmp.pixel_shader, x=((BMP_WIDTH + BMP_PADDING) * encoder), y=BMP_HEIGHT)
    bmp_group[encoder] = bmp_display

def SeedValues(data):
    seed_index = data.index("Seed Values: ")
    values = data[(seed_index + 13):].split(",")
    for value in range(len(values)):
        labels[value].text = padString(values[value], 3)

while True:
    text = uart.readline()
    if text is not None:
        data_string = ''.join([chr(b) for b in text]).strip()
        if "Seed Values: " in data_string:
            SeedValues(data_string)
        else:
            try:
                json_data = json.loads(data_string)
                if json_data["a"] == "volume":
                    ChangeVolume(json_data["e"], json_data["v"])
                elif json_data["a"] == "press":
                    ToggleMute(json_data["e"])
            except:
                pass
    time.sleep(TIME_INTERVAL)
    pass
