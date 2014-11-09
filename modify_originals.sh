#!/bin/bash

set -eu

original=static/audio/original
tmp=static/audio/tmp
mp3=static/audio/mp3

mkdir -p $tmp

#dry=echo
dry=""

function resample_and_add_reverb() {
    ls $original/*.wav | grep -v reverb- | while read f
    do
        $dry sox -r 44100 $f $tmp/$(basename $f) bass -10 1000 reverb
    done
}

function pitch_shift() {
    word=$1
    amount=$2

    $dry pushd $tmp
    $dry mv $word.wav $word-orig.wav
    $dry sox $word-orig.wav $word.wav pitch $amount
    $dry popd
}

function convert_to_mp3() {
    for f in $tmp/*.wav
    do
        $dry ffmpeg -y -i $f $mp3/$(basename $f | sed 's/\.wav/.mp3/')
    done
}

resample_and_add_reverb

pitch_shift of -100
pitch_shift to -100
pitch_shift much -100

convert_to_mp3
