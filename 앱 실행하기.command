#!/bin/bash
cd "$(dirname "$0")"
PORT=8973
echo "설교 아카이브를 실행합니다... (이 창을 닫으면 서버가 꺼집니다)"
open "http://localhost:$PORT"
python3 -m http.server "$PORT"
