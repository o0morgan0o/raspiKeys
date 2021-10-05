#!/bin/bash
kill -9 $(ps aux | grep python3 |  awk '{print $2}')
