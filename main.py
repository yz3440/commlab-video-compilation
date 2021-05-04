from moviepy.editor import *
import moviepy.video.fx.all as vfx
from os import path, listdir
import random

MEDIA_DIR = path.join(path.dirname(__file__),"media")

class StudentWork:
  def __init__(self,absolute_path):
    self.absolute_path = absolute_path
    self.basename = path.basename(absolute_path)
    self.filename = path.splitext(self.basename)[0]
    self.title, self.author = self.filename.split('_')

student_works = []

# loading the student works to list
for file in listdir(MEDIA_DIR):
    if file.endswith(".mp4"):
      student_work = StudentWork(path.join(MEDIA_DIR, file))
      student_works.append(student_work)

random.shuffle(student_works)


SCREEN_SIZE = (1920,1080)
TEXT_FADEIN_DURATION = 1
TEXT_FADEOUT_DURATION = 1
TEXT_DISPLAY_DURATION = 2
FONT = "Times-Roman"      # font must be present in your imagemagick installation, use "convert -list font" to check

clips = []

# iterating through student works
for student_work in student_works:
  print(student_work.title, student_work.author)

  title_clip = ( TextClip(student_work.title,font=FONT,fontsize=70,color='white')
              .set_duration(TEXT_FADEIN_DURATION+TEXT_DISPLAY_DURATION+TEXT_FADEOUT_DURATION)
              .fx(vfx.fadein,duration=TEXT_FADEIN_DURATION)
              .fx(vfx.fadeout,duration=TEXT_FADEOUT_DURATION )
              )

  title_clip = title_clip.set_position((1920/2-title_clip.w/2,1080/2-title_clip.h/2));

  author_clip = ( TextClip(student_work.author,font=FONT,fontsize=50,color='white')
              .set_duration(TEXT_FADEIN_DURATION+TEXT_DISPLAY_DURATION+TEXT_FADEOUT_DURATION)
              .fx(vfx.fadein,duration=TEXT_FADEIN_DURATION)
              .fx(vfx.fadeout,duration=TEXT_FADEOUT_DURATION )
              )

  author_clip = author_clip.set_position(
              (1920/2 - author_clip.w/2,
               1080/2 - author_clip.h/2 + title_clip.h + 10)
              );

  empty = (TextClip(' ',size=SCREEN_SIZE)
            .set_duration(TEXT_FADEIN_DURATION+TEXT_DISPLAY_DURATION+TEXT_FADEOUT_DURATION)
            )

  
  text_clip = CompositeVideoClip([empty,title_clip,author_clip]);
  video_clip = VideoFileClip(student_work.absolute_path)

  clips += [text_clip,video_clip]


result = concatenate_videoclips(clips) 
result.write_videofile("output.mp4") 