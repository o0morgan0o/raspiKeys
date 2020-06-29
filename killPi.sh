#!/bin/bash
kill -KILL $(ps aux | grep python3 | head -n 1| awk '{print $2}')
