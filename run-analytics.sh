#!/bin/bash

echo "=== deptry ==="
deptry -v source/

echo "=== flake8 ==="
flake8 --max-line-length 120 source/

echo "=== pylint ==="
pylint --max-line-length 120 source/
