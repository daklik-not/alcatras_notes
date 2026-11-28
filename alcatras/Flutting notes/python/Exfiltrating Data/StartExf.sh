#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Пожалуйста, запусти скрипт через sudo: sudo ./StartExf.sh"
  exit 1
fi



echo "=== ЗАПУСК ДЕМОНСТРАЦИИ DNS EXFILTRATION ==="

cleanup() {
    echo -e "\n[!] Останавливаем сервер и детектор..."
    kill $SERVER_PID 2>/dev/null
    kill $DETECTOR_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
    wait $DETECTOR_PID 2>/dev/null
    echo "[+] Готово."
}
trap cleanup EXIT

# Обрати внимание на флаг -u
echo "[*] Запуск DNSExfiltrationServer.py..."
python3 -u DNSExfiltrationServer.py > server_output.log 2>&1 &
SERVER_PID=$!

sleep 2

echo "[*] Запуск DetectAlternativeProtocol.py..."
python3 -u DetectAlternativeProtocol.py > detector_output.log 2>&1 &
DETECTOR_PID=$!

sleep 2

echo "[*] Запуск DNSExfiltrationClient.py..."
python3 -u DNSExfiltrationClient.py | tee client_output.log

sleep 3 # Даем время на обработку последних пакетов

kill $SERVER_PID 2>/dev/null
kill $DETECTOR_PID 2>/dev/null
sleep 1

echo -e "\n============================================="
echo "=== ЛОГ КЛИЕНТА ==="
cat client_output.log

echo -e "\n=== ЛОГ СЕРВЕРА ==="
cat server_output.log

echo -e "\n=== ЛОГ ДЕТЕКТОРА ==="
cat detector_output.log
echo "============================================="