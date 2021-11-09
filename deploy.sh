#!/bin/bash
SCRIPT="pwd; ls"
ssh -l pi 192.168.88.20 "${SCRIPT}"
