#!/bin/bash

# Get the Path of the Directory
read -p "Enter the Path of the Directory : " dir_path

#echo `ls $dir_path`

# Get the Regular Expression for Matching the File
read -p "Enter the Regular Expression for Matching File : " rex

# Define the File Name for Regular Expression Test
file_name="input_1.txt"

# Matching the File with the Regular Expression
if ! [[ "$file_name" =~ $rex ]]
then
	echo "Ivalid Regular Regress, Please Enter the Correct Regular Expression"
	exit
fi

# Create the Function for Further Wrok
file_changed() {
	local file="$1"
	if grep -q "specific string" "$file"
	then
		local value=$(awk '/specific string/ {print $3}' "$file")
		cp "$file" "backup/$file.bak"
		sed -i "s/specific string/new value/g" "$file"
		if [ $(wc -l < "$file") -gt 10 ]
		then
			head -n 5 "$file" > "$file.top"
			tail -n 5 "$file" > "$file.bottom"
		fi
		tar -czvf "backup_$(date +%Y%m%d_%H%M%S).tar.gz" "backup"
	fi
}

inotifywait -m -e create,modify,delete "$dir_path" | 
while read path action file
do
	if [[ "$file" =~ $rex ]]
	then
		file_changed "$path$file"
	fi
done

