from moviepy.editor import *
import moviepy.video.fx.all as vfx
from os import path, listdir
import random

MEDIA_DIR = path.join(path.dirname(__file__),"media")
VIDEO_FORMATS = ('.mp4','.avi','.webm','.mov')

class StudentWork:
  def __init__(self,absolute_path):
    self.absolute_path = absolute_path
    self.basename = path.basename(absolute_path)
    self.filename = path.splitext(self.basename)[0]
    self.title, self.author = self.filename.split('_')

student_works = []

# loading the student works to list
for file in listdir(MEDIA_DIR):
    if file.endswith(VIDEO_FORMATS):
      student_work = StudentWork(path.join(MEDIA_DIR, file))
      student_works.append(student_work)

random.shuffle(student_works)

# modify these to change the visuals
SCREEN_SIZE = (1920,1080)
TEXT_FADEIN_DURATION = 1
TEXT_FADEOUT_DURATION = 1
TEXT_DISPLAY_DURATION = 0

FONT = "Times-Roman"      # font must be present in your imagemagick installation, use "convert -list font" to check
TITLE_FONTSIZE = 70
AUTHOR_FONTSIZE = 50
FONT_COLOR= "white"

clips = []

# iterating through student works
for student_work in student_works:
  print(student_work.title, "-", student_work.author)

  # making the title clip
  title_clip = (TextClip(student_work.title,font=FONT, fontsize=TITLE_FONTSIZE, color=FONT_COLOR)
              .set_duration(TEXT_FADEIN_DURATION+TEXT_DISPLAY_DURATION+TEXT_FADEOUT_DURATION)
              )

  title_clip = title_clip.set_position((1920/2-title_clip.w/2,1080/2-title_clip.h/2));


  # making the author clip
  author_clip = (TextClip(student_work.author, font=FONT, fontsize=AUTHOR_FONTSIZE, color=FONT_COLOR)
              .set_duration(TEXT_FADEIN_DURATION+TEXT_DISPLAY_DURATION+TEXT_FADEOUT_DURATION)
              )

  author_clip = author_clip.set_position(
              (1920/2 - author_clip.w/2,
               1080/2 - author_clip.h/2 + title_clip.h + 10)
              );


  # a place holder empty clip just to make the size correct
  empty_clip = (TextClip(' ',size=SCREEN_SIZE)
            .set_duration(TEXT_FADEIN_DURATION+TEXT_DISPLAY_DURATION+TEXT_FADEOUT_DURATION)
            )

  # layer the tile and author clip on top of the empty clip and add transition
  text_clip = (CompositeVideoClip([empty_clip,title_clip,author_clip])
                .fx(vfx.fadein,duration=TEXT_FADEIN_DURATION)
                .fx(vfx.fadeout,duration=TEXT_FADEOUT_DURATION
                )
              )

  video_clip = VideoFileClip(student_work.absolute_path)

  clips += [text_clip,video_clip]


result = concatenate_videoclips(clips) 
result.write_videofile("video_compilation.mp4"), 