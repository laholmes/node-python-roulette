#!/usr/bin/env node

var express = require('express');
var app = express();
var amqp = require('amqplib/callback_api');

app.listen(3000, function () {
  console.log('server running on port 3000');
})

// 
// VERSION 1: calling python script from a node child process
// 
app.get('/dalembert', callD_alembert);

function callD_alembert(req, res) {
  // using spawn instead of exec, prefer a stream over a buffer
  // to avoid maxBuffer issue
  var spawn = require("child_process").spawn;
  var process = spawn('python', ["./d_alembert.py",
    req.query.funds, // starting funds
    req.query.size, // (initial) wager size
    req.query.count, // wager count - number of wagers per sim
    req.query.sims // number of simulations
  ]);

  process.stdout.on('data', function (data) {
    res.send(data.toString());
  });
}

// 
// VERSION 2: calling python script from a node child process, 
// using python-shell npm package (https://github.com/extrabacon/python-shell) 
// thin wrapper on childprocess
//
var PythonShell = require('python-shell');

app.get('/dalembert2', callD_alembert2);

function callD_alembert2(req, res) {
  var options = {
    args:
    [
      req.query.funds, // starting funds
      req.query.size, // (initial) wager size
      req.query.count, // wager count - number of wagers per sim
      req.query.sims // number of simulations
    ]
  }

  PythonShell.run('./d_alembert.py', options, function (err, data) {
    if (err) res.send(err);
    res.send(data.toString())
  });
}


// VERSION 3
// submit message, wait for response
app.get('/dalembert3', callD_alembert3);

function callD_alembert3(req, res) {
  var input = [
      req.query.funds, // starting funds
      req.query.size, // (initial) wager size
      req.query.count, // wager count - number of wagers per sim
      req.query.sims // number of simulations
  ]

  amqp.connect('amqp://localhost', function (err, conn) {
    conn.createChannel(function (err, ch) {
      var simulations = 'simulations';
      ch.assertQueue(simulations, { durable: false });
      var results = 'results';
      ch.assertQueue(results, { durable: false });

      ch.sendToQueue(simulations, new Buffer(JSON.stringify(input)));

      ch.consume(results, function (msg) {
        res.send(msg.content.toString())
      }, { noAck: true });
    });
    setTimeout(function () { conn.close(); }, 500);  
  });
}