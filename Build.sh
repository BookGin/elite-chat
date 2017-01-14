#!/usr/bin/env bash

python3 --version
if [ $? -ne 0 ]; then
  echo "You donen't have Python3. I'll install with apt for you."
  sudo apt install python3.5
fi

pip3 --version
if [ $? -ne 0 ]; then
  echo "You donen't have pip3. I'll install with apt for you."
  sudo apt install python3-pip
fi

echo "Install and upgrade Django via pip3..."
sudo pip3 install --upgrade django

echo "Migrate database...."
cd src
./manage.py migrate

echo "Run server......"
./manage.py runserver '0.0.0.0:8000'
