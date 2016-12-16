#!/usr/bin/env python
import pika
import d_alembert
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='simulations')
channel.queue_declare(queue='results')

def callback(ch, method, properties, body):
    requestParams = json.loads(body.decode('utf-8'))
    funds = int(requestParams[0])
    size = int(requestParams[1])
    count = int(requestParams[2])
    sims = int(requestParams[3])

    results = d_alembert.simulate(funds, size, count, sims)
    print(results)

    # send a message back
    channel.basic_publish(exchange='',
                          routing_key='results',
                          body=json.dumps(results, ensure_ascii=False))

    # connection.close()

#  receive message and complete simulation
channel.basic_consume(callback,
                  queue='simulations',
                  no_ack=True)

channel.start_consuming()