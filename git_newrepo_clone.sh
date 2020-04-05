#!/bin/bash
git clone git@github.com:$1/$2.git #$1: USERNAME, $2: NEW REPOSITORY NAME
cd tweet
git remote add kaggle_starter_kit git@github.com:$1/kaggle_starter_kit.git
git pull kaggle_starter_kit master # The contents of the existing directory you want is copied to the directory.
git add -A
git commit -m "first commit"
git remote rm kaggle_starter_kit
git push -u origin master