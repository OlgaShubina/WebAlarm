import {Component, OnInit} from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { ServerSocket } from './socet.server';
import swal from 'sweetalert';


@Component({
  selector: 'app-socket-user',
  template: `
    <div class="main" *ngFor="let ch of class_channel">
      <nav>
        <a [routerLink]="['/module',ch]" (click)="onTap(ch)" routerLinkActive="active">{{ch}}</a>
     </nav>
    </div>
    <router-outlet></router-outlet>
    <div class="sub_class">
      <div class="main_channel" *ngFor="let s_ch of name_channel">
        {{s_ch}}
        <div class="sub_channel" *ngFor="let ch of objectKeys(view_channel[s_ch])">
          <div *ngIf="objectKeys(view_channel[s_ch][ch]).length==0; else elseBlock">
            <div class="channel" [ngStyle]="{'width':'8.7%',
            'height':'8%', 'padding':'1%'}" [id]="active_route_link+'/'+s_ch+'/'+ch" (click)="changeEleventStatus(s_ch, ch)">
            {{ch}}
          </div>
          </div>
          <ng-template #elseBlock >
            <div class="block_channel">
            {{ch}}
            <div *ngFor="let ch_ of objectKeys(view_channel[s_ch][ch])">
              <div class="channel" [id]="active_route_link+'/'+s_ch+'/'+ch+'/'+ch_" (click)="changeEleventStatus(s_ch, ch)">
                {{ch_}}
              </div>
          </div></div></ng-template>
        </div>
      </div>
    </div>
     <table border="1" width="100%" cellpadding="5" class="table_class" id="table">
      <tr><th>Type of message</th><th>System name</th><th>Time</th></tr>
      <tr *ngFor="let mess of message_buffer">
        <td>{{mess.type}}</td><td>{{mess.name}}</td><td>{{mess.time}}</td>
      </tr>
    </table>
  `,
  styles: [`
    .main {
      float: top;
    }
    .sub_class{
      width: 100%;
      float: left;
    }
    .main_channel {
      margin-top: 0.5%;
      width: 49%;
      background-color: #DDD;
      float: right;
      margin-right: 0.5%;
      border-radius: 7px;
      padding-left: 0.5%;
    }
    .channel {
      background: #F4F4F4;
      padding: 2%;
      padding-right: 1%;
      padding-left: 1%;
      width: 22.5%;
      height: 30%;
      float: left;
      margin: 0.2%;
      border-radius: 4px 4px 4px 4px;
      color: #373737;
      font-family: Arial, Helvetica, sans-serif;
      text-align: center;
    }
    .block_channel {
      background-color: #DDD;
      border-color: darkgray;
      border-style: double;
      border-radius: 4px 4px 4px 4px;
      width: 45%;
      height: auto;
      float: left;
      padding: 1%;
      margin-top: 0.5%;
    }
    .table_class {
      margin-top: 0.5%;
      width: 100%;
      float: bottom;
      margin-right: 1%;
    }
  `]
})

export class SocketUserComponent {
  private socketSubscription: Subscription;
  message_buffer: any[] = [];
  name: string;
  active_route_link: string;
  objectKeys = Object.keys;
  name_channel: string[] = [];
  class_channel: string[] = [];
  view_channel: string[] = [];
  channel_buff: any[] = [];
  constructor(private socket: ServerSocket) {}

  ngOnInit() {
    this.socket.connect();

    this.socketSubscription = this.socket.messages.subscribe((message: string) => {
       const json_message = JSON.parse(message);
       //console.log(json_message);
       for (const ch in json_message) {
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
                 console.log(ch)
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
    this.active_route_link = ch
    this.view_channel = this.channel_buff[ch];
    this.name_channel = Object.keys(this.view_channel);
  }

  changeEleventStatus(s_ch: string, ch: string) {
  }

  ngOnDestroy() {
    this.socketSubscription.unsubscribe();
  }
}
