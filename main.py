import time

from PIL import Image
from cv2.cv2 import VideoCapture
from ffpyplayer.player import MediaPlayer

# set up the video player and the audio player
video_cap = VideoCapture("faces_evil.mp4") #your video you want to play
audio_player = MediaPlayer("faces_evil.mp4") #audio of video (should be same video but you can use seperate mp3)

# "Standard" character ramp for grey scale pictures
# http://paulbourke.net/dataformats/asciiart/
g_scale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^` . '
g_scale = [character for character in g_scale][::-1]

WIDTH_INPUT = 140  # the size of the frame, and therefore the size of the resulting ASCII image
FRAME_RATE = 30  # speed at which the frames will be displayed
BRIGHTNESS = 18  # the higher the value, the darker the frame is


# resize a frame to make it readable by the program
def resize_frame(frame):
    width, height = frame.size
    ratio = height / width
    new_height = int(WIDTH_INPUT * ratio)
    resized_frame = frame.resize((WIDTH_INPUT, new_height))
    return resized_frame


# convert a frame into a greyscale image to make it usable
def greyscale(frame):
    greyscale_frame = frame.convert("L")
    return greyscale_frame


# convert each pixel of a frame into an ASCII character
def pixels_to_ascii(frame):
    pixels = frame.getdata()
    characters = "".join([g_scale[pixel // BRIGHTNESS] for pixel in pixels])
    return characters


# render the current frame
def render_frame():
    try:
        ret, frame = video_cap.read()
        frame = Image.fromarray(frame)
        new_image_data = pixels_to_ascii(greyscale(resize_frame(frame)))

        pixel_count = len(new_image_data)
        ascii_frame = "\n".join(new_image_data[i:(i + WIDTH_INPUT)] for i in range(0, pixel_count, WIDTH_INPUT))

        print(ascii_frame)
    except AttributeError:
        exit()


# output the ASCII video
def output_video():
    while video_cap.isOpened():
        audio_frame = audio_player.get_frame()  # update the audio for each frame
        current_time = time.time()
        render_frame()
        time_interval = time.time() - current_time
        time.sleep(max(1 / FRAME_RATE - time_interval, 0))


# if the file is run, output the video
if __name__ == "__main__":
    output_video()


# compatible with Python 3.9.2
# P.S. the audio may be out of sync, this program is not the most efficient
# xoxoxoxo
