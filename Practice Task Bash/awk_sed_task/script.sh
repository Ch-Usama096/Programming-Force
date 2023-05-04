#!/bin/bash

awk -F ',' '$3 > 30 { gsub(/Software/,"IT",$4); print $0}' employees.txt > updated_employees.txt

cat updated_employees.txt

echo -e "\nAverage Salary of each Department:"

awk -F ',' '{sum[$4] += $5; count[$4]++} END {for (dept in sum) {print dept, sum[dept]/count[dept]} }' employees.txt > average_employees.txt

cat average_employees.txt




