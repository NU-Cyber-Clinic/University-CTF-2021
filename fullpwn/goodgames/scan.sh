for port in {1..65535}; do
  echo >/dev/tcp/172.19.0.1/$port &&
    echo "port $port is open"
done
