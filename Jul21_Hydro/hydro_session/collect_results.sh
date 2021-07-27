#!/usr/bin/env bash

folder=$1

echo "collect results into " $folder " ..."

mkdir -p $folder

mv eccentricities_evo_eta_-0.5_0.5.dat $folder/
mv evolution_all_xyeta_MUSIC.dat $folder/
mv momentum_anisotropy_eta_-0.5_0.5.dat $folder/
