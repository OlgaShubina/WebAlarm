import {Component, OnInit, Input} from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { ServerSocket } from './socet.server';
import swal from 'sweetalert';
import { Router, ActivatedRoute, Params, Data } from '@angular/router';

@Component({
  selector: 'app-module-component',
  template: `
    <div class="main" *ngFor="let s_ch of class_channel">
      {{s_ch}}
      <div class="sub_channel" *ngFor="let ch of  name_channel[s_ch]">
        <div class="channel" [id]="s_ch+'/'+ch">{{ch}}</div>
      </div>
    </div>
  `,
  styles: [`
    .main {
      margin-top: 0.5%;
      width: 33%;
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
      margin-left: 5%;
      width: 30%;
      float: top;
    }
  `]
})

export class ModuleComponent {
  @Input() name_channel: string[] = [];
  class_channel: string[] = [];
  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {
}
  ngOnInit() {
    this.name_channel = this.route.snapshot.data['name_cnannel'];
  }

  ngOnChanges() {
    this.name_channel = this.route.snapshot.data['name_cnannel'];

    this.class_channel = Object.keys(this.name_channel);
  }
}
