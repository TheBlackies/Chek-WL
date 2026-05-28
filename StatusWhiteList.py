from ping3 import ping
import time
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
hosts_path = os.path.join(script_dir, "hosts.json")

try:
  with open(hosts_path, "r", encoding="utf-8") as f:
    hosts_data = json.load(f)
    en_hosts = hosts_data["en_hosts"]
    ru_hosts = hosts_data["ru_hosts"]
    WhiteList_host = hosts_data["WhiteList_host"]
except FileNotFoundError:
    print("❌ Файл hosts.json не найден в папке скрипта.")
    exit(1)
except json.JSONDecodeError:
    print("❌ Ошибка чтения JSON. Проверьте формат hosts.json.")
    exit(1)


while True:
  host_check = input("Какие домены будем пинговать? 1 - EN. 2 - RU. Введите число: ")

  if host_check == "1":
    host_check = en_hosts
    print("Внимание, некоторые сайты могут попасть под блокировку РКН, тем самым список может быть не точен.")
    break
  elif host_check == "2":
    host_check = ru_hosts
    print("Внимание, некоторые сайты могут быть неактуальны и требовать проверку на актуальность со временем.")
    break
  else:
    print("Пожалуйста, введите либо 1 - EN, либо 2 - RU")

def check_hosts(host_dict):
  failed = 0
  total = len(host_dict)
  for name, address in host_dict.items():
    response = ping(address)
    if response is not None and response is not False:
      print(f'✅ {name:10} — {response:.3f} сек ({address})')
    else:
      print(f"❌ {name:10} — недоступен ({address})")
      failed += 1
  return failed, total

print("Пингую сайты...\n" + "-" * 40)
failed, total = check_hosts(host_check)
print("-" * 40)

if failed == 0:
  print("✅ Все основные хосты доступны. Вы вне зоне действий БС.")

elif failed < total / 2:
  print(f"⚠️ Часть основных хостов недоступна ({failed}/{total}). Возможны блокировки.")

else:
  print(f"\n❌ Большинство основных хостов недоступно ({failed}/{total})! Проверяю Белые Списки:")
  print("-" * 40)
  failed_w, total_w = check_hosts(WhiteList_host)
  print("-" * 40)
  
  if failed_w == 0:
    print("✅ Белые Списки работают! Вы находитесь в зоне БС.")
  elif failed_w < total_w / 2:
    print(f"⚠️ Часть Белых Списков доступна ({total_w - failed_w}/{total_w}). Проблемы с сетью или частичные блокировки.")
  else:
    print("⚠️ Интернет не работает. Проверьте интернет соединение.")

print("Скрипт завершен. Закрытие через 10 секунд...")
time.sleep(10)
