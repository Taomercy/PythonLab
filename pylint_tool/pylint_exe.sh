#!/bin/bash
pylint --list-msgs > pylint_messages_list.log
python pylint_message_to_excel.py
check_filename=$1
pylint $check_filename --disable=C0326,C0301,C0303 > res.log
