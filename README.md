# xmppbot
XMPP sending bot with email gateway for monitoring and CI

# Принцип работы
* серверная часть - daemon.py открывает сокет, в который клиенты посылают json с сообщением
* клиентская часть
  * send.py <jid> <subject> <message> - если надо отправить сообщение из скрипта или коноли
  * sendmail.py <jid> - интегрируется в posfix

# Установка

* колнируем в /opt/xmppbot
* устанавливаем venv и зависимости
  * virtualenv /opt/xmppbot/venv
  * /opt/xmppbot/venv/bin/pip install -r requirements.txt
* создаём пользователя jabberbot
* вооружившись примером пишем конфиг xmppbot.conf
* устанавливаем файлы
  * cp contrib/xmppbot.tmpfiles.conf /etc/tmpdiles.d/xmppbot.conf; systemd-tmpfiles --create /etc/tmpdiles.d/xmppbot.conf
  * cp contrib/xmppbot.service /etc/systemd/system/xmppbot.service
  * install -u jabberbot -g jabberbot -d /var/log/xmppbot
* если selinux включен
  * cd contrib/selinux; ./postfixpipe.sh	
  * restorecon -R /run/jabberbot/
  * restorecon -R /var/log/xmppbot
  * restorecon -R /opt/xmppbot
* конфигурируем postfix по примеру в файле sendmail.py
* systemctl enable --now xmppbot
