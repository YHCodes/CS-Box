

RabbitMQ 是部署最广泛的开源消息代理(message broker).


- lightweight and easy to deploy 
- supports multiple messaging protocols


Features:
- Asynchronous Messaging, 异步消息

### Tutorial

#### 1. Hello World
- **message broker** : it accepts, stores and forwards binary blobs of data - messages.
- **producer** ： sends message.
- **queue** : is a large message buffer that stores messages
- **consumer**: is a program that mostly waits to receive messages.

`send.py`

```python
import pika

# 建立连接
param = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(param)
channel = connection.channel()

# 在发送之前，创建队列
channel.queue_declare(queue='hello')

# 在 RabbitMQ 中，一个消息不能直接发送给队列，它总是需要通过交换(exchange)
# 下面使用 default exchange (用空字符串来标识） 
channel.basic_publish(exchange='', 
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!' ")

# 在退出程序之前，通过关闭连接来确保网络缓冲区(network buffers)被刷新和消息已经传递给 RabbitMQ
connection.close()
```

`receive.py`

```python
import pika

# 建立连接
param = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(param)
channel = connection.channel()

# 为什么要重复 declare 队列？确保队列存在
channel.queue_declare(queue='hello')

# 当接收到message时，callback函数被调用
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 告诉 RabbitMQ, 指定callback函数用来接收信息
channel.basic_consume(callback, queue='hello', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```



#### 2. Woke Queue
**Work Queue**

- 用于在多个`worker`之间分配耗时的任务。
- 避免**立即**执行资源密集型任务(resource-intensive task)，并且必须等待它完成。
- 安排任务在稍后完成，可将任务封装为消息并将其发送到队列中。运行在后台的`worker`会在队列中pop出这个任务，并执行这个作业。
- **Round-robin dispatching**，循环调度
  - 默认情况下，`RabbitMQ` 将按顺序将每条消息发送给下一个 `consumer`， 平均而言，每个 `consumer` 将获得相同数量的 `message`.
- **Message acknowledgment， ack**, 消息确认
  - `consumer` 发送 ack 告诉 `RabbitMQ` 消息已经接收和处理，可以删除了
  - 如果一个 `consumer` dies (channel is closed, connection is closed, or TCP connection is lost) 没有发送ack, `RabbitMQ`会将消息重新加入队列(re-queue)
- **Message durability**
  - 如果 `RabbitMQ` 服务器停止或宕机，队列和消息会丢失，除非:
    1. 在producer和consumer 创建队列时指定持久化选项，`channel.queue_declare(queue='hello', durable=True)`
    2. make message persistent: `properties=pika.BasicProperties(delivery_mode=2, ) `
- **Fair dispatch**
  - `basic.qos(prefetch_count=1)` 把消息分配到空闲的worker中处理



`new_task.py`

```python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Message durability
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()
```



`worker.py`

```python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Message durability
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

   
# Fair dispatch： tells RabbitMQ not to give more than one message to a worker at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()
```



#### 3.Publish/Subscribe

- **What?**

  - 在 work queue中，每个task都只传递给了一个worker，如果一个task要传递给多个worker要怎么办？
  - deliver a message to multiple consumers.
  -  eg. logging system, broadcast log messages to many receivers.

- **Exchanges**

  - `producer` 只能发送消息给一个`exchange`, 然后 `exchange` 接收到消息后再把消息发送给队列， `exchange` 必须准确地知道接收到消息后要如何做。
  -  **exchange types**： direct, topic, headers, fanout. 
  - create an  exchange:  `exchange_declare(exchange='logs', exchange_type='fanout')`
    - `fanout` : broadcasts all the messages it receives to all the queues it knows.
  - default exchange: `basic_publish(exchange='', routing_key='hello', body=message)`

- **Temporary queues**

  - 首先，需要一个空队列，可以在创建队列的时候不提供任何参数给 `queue_declare()`
    - `result = channel.queue_declare()`
    - 在这里，`result.method.queue` 包含一个随机队列名
  - 然后，一旦 `consumer` 连接关闭，这个队列应该被删除
    - `result = channel.queue_declare(exclusive=True)`

- **Bindings**

  - 告诉 `exchange` 发送消息给队列
  - `channel.queue_bind(exchange='logs', queue=result.method.queue)`

  ​

`emit_log.py`

```python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(" [x] Sent %r" % message)
connection.close()
```



`receive_logs.py`

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

    
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
```



#### 4.Routing - Direct exchange

- **What?**
  - how to listen for a subset of messages ? subscribe only to a subset of the messages
- **Bindings**
  - is a relationship between an exchange and a queue. 
  - the queue is interested in messages from this exchange.
  - `routing_key` : to avoid the confusion with a `basic_publish` parameter
  - `channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='black')`
- **Direct exchange**
  - a message goes to the queues whose `binding key` exactly matches the `routing key` of the message.
- **Multiple bindings**
- **Emitting logs**
- **Subscribing**



`emit_log_direct.py`

```python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()
```



`receive_logs_direct.py`

```python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
```



#### 5.Topic exchange

- **what?**
  - What are the limitations of the `direct` exchange type?
    - it can't do routing based on multiple criteria
- **Topic exchange**
  - a message sent with a particular routing key will be delivered to all the queues that are bound with a matching binding key.
    - *(star) can substitute for exactly one word.
    - \# (hash) can substitute for zero or more words.
  - Topic exchange is powerful and can behave like other exchanges.



`emit_log_topic.py`

```python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# exchange_type = 'topic'
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)

print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
```



`receive_logs_topic.py`

```python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# exchange_type = 'topic'
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
```





#### 6.RPC, Remote procedure call

- **what?**
  - what if we need to run a function on a remote computer and wait for the result? 
  - ​

### Reference
http://www.rabbitmq.com/
http://www.rabbitmq.com/tutorials/tutorial-one-python.html



[guide on queues](http://www.rabbitmq.com/queues.html)

[Documentation: Table of Contents](http://www.rabbitmq.com/documentation.html)