import {Component, OnInit} from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { ServerSocket } from './socet.server';
import swal from 'sweetalert';


@Component({
  selector: 'app-socket-user',
  template: `
    <table border="1" width="100%" cellpadding="5" class="table_class" id="table">
      <tr><th>Type of message</th><th>System name</th><th>Time</th></tr>
      <tr *ngFor="let mess of message_buffer">
        <td>{{mess.type}}</td><td>{{mess.name}}</td><td>{{mess.time}}</td>
      </tr>
    </table>
    <div class="main" *ngFor="let ch of class_channel">
      <nav>
        <a [routerLink]="['/module',ch]" (click)="onTap(ch)" routerLinkActive="active">{{ch}}</a>
     </nav>
    </div>
    <router-outlet></router-outlet>
    <div class="sub_class">
      <div class="main_channel" *ngFor="let s_ch of name_channel">
        {{s_ch}}
        <div class="sub_channel" *ngFor="let ch of  view_channel[s_ch]">
          <div class="channel" [id]="s_ch+'/'+ch" (click)="changeEleventStatus(s_ch, ch)">{{ch}}</div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .main {
      float: top;
    }
    .sub_class{
      width: 53%;
      float: left;
    }
    .main_channel {
      margin-top: 0.5%;
      width: 100%;
      background-color: #DDD;
      float: left;
      margin-right: 0.5%;
      border-radius: 7px;
      padding-left: 0.5%;
    }
    .channel {
      background: #F4F4F4;
      padding: 1%;
      padding-right: 1%;
      width: 10%;
      height: 15%;
      float: left;
      margin: 0.2%;
      border-radius: 4px 4px 4px 4px;
      color: #373737;
      font-family: Arial, Helvetica, sans-serif;
      text-align: center;
    }
    .table_class {
      margin-top: 0.5%;
      width: 46%;
      float: left;
      margin-right: 1%;
    }
  `]
})

export class SocketUserComponent {
  private socketSubscription: Subscription;
  message_buffer: any[] = [];
  name: string;
  name_channel: string[] = [];
  class_channel: string[] = [];
  view_channel: string[] = [];
  channel_buff: any[] = [];
  constructor(private socket: ServerSocket) {}

  ngOnInit() {
    //console.log(document.getElementById(''));

    this.socket.connect();

    // document.getElementById('VEPP/SOL/4S4').style.background = 'red';
    this.socketSubscription = this.socket.messages.subscribe((message: string) => {
       const json_message = JSON.parse(message);
       console.log(json_message);
       for (const ch in json_message) {
         //const ch = ch.slice(ch.indexOf('/') + 1);
         if (ch === 'channels') {
           this.channel_buff = json_message[ch];
           this.class_channel = Object.keys(this.channel_buff);
         } else {
           //console.log(ch)
           if (json_message[ch]['active'] === true) {
             const time = new Date();
             //let buff_str: any;
             //console.log(json_message[ch]['info']);
             switch (json_message[ch]['info']) {

               case 'error1':
                 if (typeof(document.getElementById(ch)) !== 'undefined' && document.getElementById(ch) !== null) {
                   document.getElementById(ch).style.background = 'red';
                   document.getElementById(ch).style.color = '#F4F4F4';
                   document.getElementById(ch).title = 'Set current = 0';
                 }
                 this.message_buffer.push({type: 'Set current = 0', name: ch, time: time});
                 break;
               case 'error2':
                 if (typeof(document.getElementById(ch)) !== 'undefined' && document.getElementById(ch) !== null) {
                   document.getElementById(ch).style.background = 'red';
                   document.getElementById(ch).style.color = '#F4F4F4';
                   document.getElementById(ch).title = 'Delta > 5A';
                 }
                 this.message_buffer.push({type: 'Delta > 5A', name: ch, time: time});
                 break;
               case 'error3':
                 if (typeof(document.getElementById(ch)) !== 'undefined' && document.getElementById(ch) !== null) {
                   document.getElementById(ch).style.background = 'red';
                   document.getElementById(ch).style.color = '#F4F4F4';
                   document.getElementById(ch).title = 'Sigma > 10^-3';
                 }
                 //console.log(ch)
                 this.message_buffer.push({type: 'Sigma > 10^-3', name: ch, time: time});
                 break;
               case 'correct':
                 if (typeof(document.getElementById(ch)) !== 'undefined' && document.getElementById(ch) !== null) {
                   document.getElementById(ch).style.background = 'forestgreen';
                   document.getElementById(ch).style.color = '#F4F4F4';
                 }
                 break;
             }
             if (this.message_buffer.length > 12) {
               this.message_buffer.shift();
             }
           } else {
             if (typeof(document.getElementById(ch)) !== 'undefined' && document.getElementById(ch) !== null) {
               document.getElementById(ch).style.background = '#F4F4F4';
               document.getElementById(ch).style.color = '#373737';
             }
           }
         }
       }
    });

  }
  onTap(ch: any) {
    this.view_channel = this.channel_buff[ch];
    //console.log(this.channel_buff)
    this.name_channel = Object.keys(this.view_channel);
  }

  changeEleventStatus(s_ch: string, ch: string) {
  }

  ngOnDestroy() {
    this.socketSubscription.unsubscribe();
  }
}
