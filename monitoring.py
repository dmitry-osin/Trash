#!/usr/bin/env python
#! -*- coding:utf-8 -*-
 
import sys,os,xmpp,time,re,socket
 
localtime = time.asctime( time.localtime(time.time()) )
print u"Текущее время :", localtime
 
FROM_GMAIL_ID = "from_example@gmail.com" # Ваш аккант google mail
GMAIL_PASS = "example_password" # Ваш пароль google mail
GTALK_SERVER = "talk.google.com" # Сервер по умолчанию
TO_GMAIL_ID = "to_example@gmail.com" # Адрес куда сообщать
GTALK_PORT = '5222' # Порт по умолчанию
 
def check_webserver(address, port, resource):
    # Создать строку запроса HTTP
    if not resource.startswith('/'):
        resource = '/' + resource
    request_string = "GET %s HTTP/1.1rnHost: %srnrn" % (resource, address)
 
    print u'Запрос HTTP'
    print '|||%s|||' % request_string
 
    # Создать сокет TCP
    s = socket.socket()
    print u"Соединяюсь с %s порт %s" % (address, port)
    try:
        s.connect((address, port))
        print u"Соединение с %s порт %s успешно" % (address, port)
        s.send(request_string)
        # Нам достаточно получить только первые 100 байтов
        rsp = s.recv(100)
        print u'Получены первые 100 байт HTTP ответа'
        print '|||%s|||' % rsp
    except socket.error, e:
        jid=xmpp.protocol.JID(FROM_GMAIL_ID)
        cl=xmpp.Client(jid.getDomain(),debug=[])
        if not cl.connect((GTALK_SERVER,GTALK_PORT)):
            raise IOError(u'Не могу соединиться с серверов.')
        if not cl.auth(jid.getNode(),GMAIL_PASS):
            raise IOError(u'Не могу авторизоваться на сервере.')
        cl.send( xmpp.Message( TO_GMAIL_ID ,"%s Сайт AcidNation.Ru недоступен" % localtime ) ) # Ваше сообщение
        cl.disconnect()
        print u'Не удалось соединиться с %s порт %s' % (address, port)
        return False
 
    finally:
        # Закроем соединение
        print u'Закрываем соединение'
        s.close()
    lines = rsp.splitlines()
    print u'Первая строка HTTP ответа: %s' % lines[0]
    try:
        version, status, message = re.split(r's+', lines[0], 2)
        print u'Версия: %s, Статус: %s, Сообщение: %s' % (version, status, message)
    except ValueError:
        print u'Не могу разделить строки'
        return False
    if status in ['200', '301']:
        print u'Успешно = статус выполнения %s' % status
        return True
    else:
        print u'Статус выполнения %s' % status
        return False
 
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a" , "--address", dest="address", default="localhost", help="ADDRESS for webserver", metavar="ADDRESS")
    parser.add_option("-p", "--port", dest="port", type="int", default="80", help="PORT for webserver", metavar="port")
    parser.add_option("-r", "--resource", dest="resource", default="index.html", help="RESOURCE to check", metavar="RESOURCE")
    (options, args) = parser.parse_args()
    print u'Опции: %s, Ключи: %s' % (options, args)
    check = check_webserver(options.address, options.port, options.resource)
    print u'Сервер check_webserver вернул результат %s' % check
    rez = check
    if rez == False:
        print u'Отчет отправлен на %s' % TO_GMAIL_ID
    else:
        print u'Успех'
    sys.exit(not check)