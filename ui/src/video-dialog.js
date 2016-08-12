import {DialogController} from 'aurelia-dialog';
import {inject} from 'aurelia-framework';
import {HttpClient} from 'aurelia-http-client';

@inject(DialogController)
export class VideoPrompt {

  constructor(controller) {
    this.controller = controller;
    this.httpClient = new HttpClient();
    this.answer = null;
    this.model = null;

    controller.settings.lock = false;
  }

  get youtube_video_url()
  {
    return 'https://www.youtube.com/embed/geGlkI9lVpk?wmode=transparent';//this.model.youtube_video_url;
  }

  activate(args) {
    this.httpClient.createRequest('api/brackets/'+args.bracketId+'/matches/'+args.matchId+'/games/'+args.gameId)
      .asGet()
      .send()
      .then((function(data)
      {
          this.model = JSON.parse(data.response);

      }).bind(this));
  }
}
