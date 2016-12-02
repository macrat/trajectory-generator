tail -n +2 $1 | awk -F',' '$1 != "" { print "ffmpeg -ss " $4 " -i GOPR" $1 ".MP4 -t " $6 " -an original/" NR ".mp4" }'
