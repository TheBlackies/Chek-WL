from ping3 import ping
import time

en_hosts = {
  "Google": "google.com",
  "GitHub": "github.com",
  "Pinterest": "pinterest.com",
  "GitLab": "gitlab.com",
  "Docker": "docker.com",
  "Gitea": "about.gitea.com",
  "Oxk": "okx.com",
  "GitBook": "app.gitbook.com",
  "Dropbox": "dropbox.com",
  "Pixlr": "pixlr.com"
}

ru_hosts = {
  "Tproger": "tproger.ru",
  "Woordhunt": "wooordhunt.ru",
  "Mega": "mega.ru",
  "Shoko": "shoko.ru",
  "Zenden": "zenden.ru",
  "Tvoe": "tvoe.ru",
  "Cyberlenika": "cyberleninka.ru",
  "Businessmens": "businessmens.ru",
  "Health-Diet": "health-diet.ru",
  "secrets-tbank": "secrets.tbank.ru"
}

WhiteList_host = {
  "Max" : "web.max.ru",
  "Yandex" : "ya.ru",
  "Vk" : "vk.ru",
  "Avito" : "avito.ru",
  "Moex" : "moex.com",
  "RuStore" : "rustore.ru",
  "Gismeteo" : "gismeteo.ru",
  "Ozon" : "ozon.ru",
  "Wildberries" : "wildberries.ru",
  "2Gis" : "2gis.ru"
}

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
