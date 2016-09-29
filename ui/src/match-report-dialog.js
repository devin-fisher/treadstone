import {DialogController} from 'aurelia-dialog';
import {inject} from 'aurelia-framework';
import {HttpClient} from 'aurelia-http-client';

@inject(DialogController)
export class MatchReportPrompt {

  constructor(controller) {
    this.controller = controller;
    this.httpClient = new HttpClient();
    this.answer = null;
    this.match = controller.settings.model.match;
    this.games = controller.settings.model.games;

    controller.settings.lock = false;
  }

  get youtube_video_url()
  {
    return this.games.youtube_video_url;
  }

  activate(args) {
  }
}
