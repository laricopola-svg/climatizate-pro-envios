#!/bin/bash
# Uso: tools/make_reel.sh <carpeta con 9x16_NN.jpg> [segundos_por_lamina]
# Si existe <carpeta>/voz.txt se genera la voz en off (tools/voz.py) y el ritmo de láminas se ajusta a la locución.
d=$1; n=$(ls $d/9x16_*.jpg | wc -l); per=${2:-$([ $n = 1 ] && echo 8 || echo 3)}; i=0; T=$(mktemp -d)
VOZ=""; if [ -f $d/voz.txt ]; then python3 $(dirname $0)/voz.py "$(cat $d/voz.txt)" $d/voz.wav >/dev/null 2>&1 && VOZ=$d/voz.wav; fi
if [ -n "$VOZ" ]; then vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $VOZ); per=$(python3 -c "n=$n;print(round(max(2.2,($vd+1.5+0.4*(n-1))/n),2))"); fi
for f in $(ls $d/9x16_*.jpg); do i=$((i+1)); ffmpeg -y -loglevel error -loop 1 -i $f -t $per -vf "scale=1188:2112,zoompan=z='min(zoom+0.0009,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p" -r 30 -c:v libx264 -preset veryfast -crf 18 $T/s$i.mp4; done
if [ $n = 1 ]; then cp $T/s1.mp4 $T/v.mp4; else inputs=""; fc=""; prev="0"
 for j in $(seq 1 $n); do inputs="$inputs -i $T/s$j.mp4"; done
 for j in $(seq 1 $((n-1))); do off=$(python3 -c "print(round($j*($per-0.4),2))"); fc="$fc[$prev][$j]xfade=transition=slideleft:duration=0.4:offset=$off[x$j];"; prev=x$j; done
 ffmpeg -y -loglevel error $inputs -filter_complex "${fc%;}" -map "[$prev]" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p $T/v.mp4; fi
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/v.mp4)
if [ -n "$VOZ" ]; then ffmpeg -y -loglevel error -i $T/v.mp4 -i $VOZ -filter_complex "[1:a]adelay=300|300,apad[a]" -map 0:v -map "[a]" -t $dur -c:v copy -c:a aac -b:a 192k -movflags +faststart $d/reel.mp4
else ffmpeg -y -loglevel error -i $T/v.mp4 -f lavfi -t $dur -i anullsrc=r=44100:cl=stereo -c:v copy -c:a aac -shortest -movflags +faststart $d/reel.mp4; fi
cp $d/9x16_01.jpg $d/portada.jpg; rm -rf $T; echo "$d $dur s"
