#!/bin/bash

find . | awk -F'-' '{ print $1 }' | sort | uniq -c | sort -h
