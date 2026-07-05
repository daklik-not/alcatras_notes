## The five layers reference model[¶](https://beta.computer-networking.info/syllabus/default/principles/referencemodels.html#the-five-layers-reference-model "Permalink to this headline")
Application, Transport, Network, Datalink, Physical
## TCP/IP Reference model
#### The Physical layer[¶](https://beta.computer-networking.info/syllabus/default/principles/referencemodels.html#the-physical-layer "Permalink to this headline")
2 устройства соединены через физического посредника - кабель/радиоволны. Данные в виде электрических или световых сигналов. На этом уровне почти всегда протоколы ненадежного уровня, потому что физический канал может менять из-за электромагнитной интерференции + может доставляться больше или меньше бит.
#### The Datalink layer[¶](https://beta.computer-networking.info/syllabus/default/principles/referencemodels.html#the-datalink-layer "Permalink to this headline")
На уровень выше. Обмениваются кадрами. Кадры - фиксированного размера/нефиксированного. Тип соединения - connectionless/connection-oriented. Reliable доставка кадров и не reliable доставка. Чтобы передать кадр, сущность канального уровня вызывает столько Data.request к физическому уровню., сколько бит надо передать.
#### The Network layer[](https://beta.computer-networking.info/syllabus/default/principles/referencemodels.html#the-network-layer "Permalink to this headline")
Нужен, чтобы передавать информацию между сущностями, не соединенными напрямую каналом. Обменивается пакетами. Пакет содержит информацию о своем адресе назначения и передается через роутеры до следующего хоста.
#### The Transport layer[¶](https://beta.computer-networking.info/syllabus/default/principles/referencemodels.html#the-transport-layer "Permalink to this headline")
Между 2 хостами может быть сразу несколько потоков взаимодействия. Обмениваются сегментами. Вводится понятие порта. TCP - connection-oriented сервис, в то время, как UDP - connectionless сервис.
#### The Application Layer
Этот слой включает в себя все механизмы и структуры данных, которые необходимы для приложения. ADU/SDU - юнит обмена на этом уровне.

### OSI model
Здесь только отличия от TCP/IP.
1. The session layer.  Содержит протоколы и механизмы, которые нужны, чтобы организовать и синхронизировать диалог и управлять обменом данных сущностей *presentation* слоя. Этот уровень прячет ошибки транспортного уровня. Он дает сервис, который позволяет устанавливать сессионное соединение, поддерживать упорядоченный обмен данными(включая механизмы восстановления от abrupt освобождения) и освобождение поочереди
2. The presentation layer. Работает с информацией. Его задача стандартизировать представление информации. ASN.1.
3. Application layer. Механизмы, которые не содержатся ни в presentation ни в session.