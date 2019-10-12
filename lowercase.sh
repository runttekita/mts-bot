#!/bin/bash
for file in ./data/*
do
	newFileName="$(tr [A-Z] [a-z] <<< "$file")"
	mv $file $newFileName
done
