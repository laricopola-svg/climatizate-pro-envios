#!/bin/bash
# uso: reel.sh carpeta segundos_por_lamina
set -e
D=$1; T=$2; X=0.4; FPS=30
files=($D/9x16_*.jpg); n=${#files[@]}
inputs=""; filt=""
for i in "${!files[@]}"; do
  inputs+=" -loop 1 -t $T -i ${files[$i]}"
  fr=$(python3 -c "print(int($T*$FPS))")
  filt+="[$i:v]scale=1188:2112,zoompan=z='min(zoom+0.0007,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$fr:s=1080x1920:fps=$FPS,setsar=1,format=yuv420p[v$i];"
done
if [ $n -eq 1 ]; then last="v0"; else
  prev="v0"; off=0
  for ((i=1;i<n;i++)); do
    off=$(python3 -c "print(round($T*$i-$X*$i,2))")
    filt+="[$prev][v$i]xfade=transition=fade:duration=$X:offset=$off[x$i];"; prev="x$i"
  done; last=$prev
fi
dur=$(python3 -c "print(round($T*$n-$X*($n-1),2))")
ffmpeg -y -loglevel error $inputs -f lavfi -t $dur -i anullsrc=r=44100:cl=stereo -filter_complex "${filt%;}" -map "[$last]" -map $n:a -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r $FPS -c:a aac -b:a 128k -shortest -movflags +faststart $D/reel.mp4
cp $D/9x16_01.jpg $D/portada.jpg
ffprobe -v error -show_entries format=duration,size -of csv=p=0 $D/reel.mp4
