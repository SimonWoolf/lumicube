# unforuntately this doesn't work:  curl 'http://192.168.0.99/api/v1/debug/launch_python?name=main' -H 'Content-Type: application/x-python-code' --data-binary "@fire.py"
curl -v 'http://192.168.0.99/api/v1/debug/launch_python?name=main' -H 'Content-Type: application/json' --data "{\"body\":\"`awk '{printf "%s\\\n", $0}' fire.py `\"}"

curl 'http://192.168.0.99/api/v1/debug/python_log' | jq .
