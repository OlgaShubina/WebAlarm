import { Component, OnInit, OnDestroy } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import {Message} from '@stomp/stompjs';

import { Subscription } from 'rxjs/Subscription';
import {StompService} from '@stomp/ng2-stompjs';
import 'rxjs/add/operator/map';
import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/observable/dom/WebSocketSubject';
import websocketConnect from 'rxjs-websockets';
import { QueueingSubject } from 'queueing-subject';
import 'rxjs/add/operator/share';
import { ServerSocket } from './socet.server';

@Component({
  selector: 'app-root',
  template: `
    <div class="head" id="head" style="width:100%;">
      <img src="{{src_image}}">
      <h1>VEPP-2000 Alarm System</h1>
    </div>
    <app-socket-user></app-socket-user>
  `
})
export class AppComponent {
    src_image: string;
    private socketSubscription: Subscription;
    constructor(private socket: ServerSocket) {
    this.src_image = '/assets/logo2.jpg';

    }

  OnInit() {
     document.getElementById('head').style.width = window.innerWidth * 0.99 + 'px';
     window.onresize = function(){
      document.getElementById('head').style.width = window.innerWidth * 0.99 + 'px';
    };
     /*const stomp_subscription = this._stompService.subscribe('/topic/ng-demo-sub');

    //stomp_subscription.map((message: Message) => {
      //console.log(message);
      //console.log('123');
     // return message.body;
   // }).subscribe((msg_body: string) => {
     // console.log(`Received: ${msg_body}`);
    //});*/

  }

}
