#!/bin/bash

set -e
set -x

model_name="AE_skipLSTM_AR"  # Options: AE_skipLSTM, AR
seed=0 
windows=6
train_percent=0.1 
dataset="std" # Options: occupancy, apple, bee_waggle_6 

unit=20
horizon=4
highway=6
skip_sizes="3 5 7"

python3 -W ignore ./code/main.py \
    --dataset_name $dataset \
    --seed $seed \
    --windows $windows \
    --train_percent $train_percent \
    --model_name $model_name \
    --epochs 10 \
    --unit $unit \
    --horizon $horizon \
    --highway $highway \
    --skip_sizes $skip_sizes
