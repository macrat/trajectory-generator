mkdir original image trajectory tmp

sh cropgen.sh $1 > cropper
sh cropper
rm cropper

python trajectory.py

ls tmp/ | xargs -I{} ffmpeg -i tmp/{} -c:v libx264 trajectory/{} && rm -r tmp
