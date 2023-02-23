#!/bin/bash

#set permissions

path=$1
cd $path

for file in *.sh; do
	chmod u+rwx $file
	chmod g+rwx $file
	sed -i -e 's/\r$//' $file
done