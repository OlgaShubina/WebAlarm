import { Injectable } from '@angular/core';
import { QueueingSubject } from 'queueing-subject';
import { ReplaySubject } from 'rxjs/ReplaySubject';
import { Observable } from 'rxjs/Observable';
import websocketConnect from 'rxjs-websockets';
import 'rxjs/add/operator/share';
import 'rxjs/add/operator/retryWhen';
import 'rxjs/add/operator/delay';
import 'rxjs/add/operator/retry';

@Injectable()
export class ServerSocket {
  private inputStream: QueueingSubject<string>;
  public messages: Observable<string>;
  public ws: WebSocket;
  public connect() {
    if (this.messages) {
      return;
    }// Using share() causes a single websocket to be created when the first
    // observer subscribes. This socket is shared with subsequent observers
    // and closed when the observer count falls to zero.
    this.messages = websocketConnect(
      'ws://' + window.location.hostname + ':8080/ws',
      this.inputStream = new QueueingSubject<string>()
    ).messages.share();
  }
  public start() {
    this.ws = new WebSocket('ws://' + window.location.hostname + ':8080/ws');
    this.ws.onmessage = function(evt) { alert('message received'); };
    this.ws.onclose = function(){
        /// try to reconnect in 5 seconds
        setTimeout(function(){this.start('ws://' + window.location.hostname + ':8080/ws')}, 5000);
    };
}
   public send(message: string): void {
    // If the websocket is not connected then the QueueingSubject will ensure
    // that messages are queued and delivered when the websocket reconnects.
    // A regular Subject can be used to discard messages sent when the websocket
    // is disconnected
    this.inputStream.next(message);
  }
}
