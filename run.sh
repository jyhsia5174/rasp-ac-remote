#!/bin/bash

for i in {1..20}
do
  echo ${i}
  ./38khz $1
  sleep 1s
done
