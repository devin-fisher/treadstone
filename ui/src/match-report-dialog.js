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
    var foundGames = this.games;

    controller.settings.lock = false;

    // var url = 'http://localhost:9000/api/leagues/na-lcs/tournaments/6090e92b-d565-41c4-8548-06570ab26fb7/brackets/141069e4-bce3-4d29-be15-9c733cbb7d75/matches/9ac829ec-d231-45ba-ba24-0adde0f6cc6f/games'
    // this.httpClient.createRequest(url)
    //   .asGet()
    //   .send()
    //   .then((function(data)
    //   {
    //       var matches = JSON.parse(data.response);
    //       matches.forEach(function(entry)
    //         {
    //           foundGames.push(entry)
    //         });
    //   }));
  }

  get youtube_video_url()
  {
    return 'https://www.youtube.com/embed/geGlkI9lVpk?wmode=transparent';//this.model.youtube_video_url;
  }

  activate(args) {
    // this.httpClient.createRequest('api/brackets/'+args.bracketId+'/matches/'+args.matchId+'/games/'+args.gameId)
    //   .asGet()
    //   .send()
    //   .then((function(data)
    //   {
    //       this.model = JSON.parse(data.response);
    //
    //   }).bind(this));
  }
}
