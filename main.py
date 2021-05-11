from moviepy.editor import *
import moviepy.video.fx.all as vfx
from os import path, listdir
import random
import csv
from time import gmtime, strftime

MEDIA_DIR = path.join(path.dirname(__file__),"media")
VIDEO_FORMATS = ('.mp4','.avi','.webm','.mov','m4v','mpeg')

class StudentWork:
  def __init__(self, absolute_path):
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
TEXT_DISPLAY_DURATION = 3
INTERMISSION_DURATION = 1

FONT = "Times-Roman"      # font must be present in your imagemagick installation, use "convert -list font" to check
TITLE_FONTSIZE = 70
AUTHOR_FONTSIZE = 50
FONT_COLOR= "white"

result_clips = []

with open('schedule.csv', 'w', newline='') as schedule_csv_file:
  fieldnames = ['#', "title", "author", "start_time", "end_time", "running_time"]
  writer = csv.DictWriter(schedule_csv_file,fieldnames=fieldnames)
  writer.writeheader()
  cumulated_time = 0

  # iterating through student works
  for i, student_work in enumerate(student_works):

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


    intermission_clip = (TextClip(' ',size=SCREEN_SIZE)
              .set_duration(INTERMISSION_DURATION)
              )


    video_clip = VideoFileClip(student_work.absolute_path)
    
    # if it's the first video, no intermission is needed
    if i == 0:
      work_clip = concatenate_videoclips([text_clip, video_clip]) 
    else:
      work_clip = concatenate_videoclips([intermission_clip, text_clip, video_clip]) 

    # log the video time info
    video_info = {
      "#": i,
      "title": student_work.title,
      "author":  student_work.author,
      "start_time": strftime("%H:%M:%S", gmtime(cumulated_time)),
      "end_time": strftime("%H:%M:%S", gmtime(cumulated_time+video_clip.duration)),
      "running_time":strftime("%H:%M:%S", gmtime(video_clip.duration))
    }
    print(video_info)
    writer.writerow(video_info)

    cumulated_time += work_clip.duration 

    result_clips += [work_clip]


# rendering the result
result = concatenate_videoclips(result_clips) 
result.write_videofile("video_compilation.mp4"), 