import {Match} from './match';
import {Bracket} from './bracket';
import {VideoPrompt} from './video-dialog';
import {HttpClient} from 'aurelia-http-client';
import {DialogService} from 'aurelia-dialog';
import {inject} from 'aurelia-framework';

@inject(DialogService)
export class App
{
  constructor(dialogService, httpClient)
  {
    this.dialogService = dialogService;
    this.httpClient = new HttpClient();
    this.heading = 'Treadstone';
    this.matches = [];
    this.brackets = [];

    this.populateBracket();

    var currentBracket = localStorage.getItem('currentBracket');
    if(currentBracket)
    {
      this.populateMatches('2a6a824d-3009-4d23-9c83-859b7a9c2629');
    }
  }

  populateMatches(bracket_id)
  {
    this.clearMatches();
    this.httpClient.createRequest('api/brackets/'+bracket_id+'/matches')
      .asGet()
      .send()
      .then((function(data)
      {
          var matches = JSON.parse(data.response);
          matches.forEach(this.addMatch.bind(this));
      }).bind(this));
    localStorage.setItem('currentBracket',bracket_id);
  }

  openVideoDialog(bracketId, matchId, gameId)
  {
    this.dialogService.open({ viewModel: VideoPrompt, model: {"bracketId":bracketId, "matchId":matchId, "gameId":gameId}}).then(response => {
          if (!response.wasCancelled) {
            console.log('good');
          } else {
            console.log('bad');
          }
          console.log(response.output);
        });
  }

  populateBracket()
  {
    this.clearMatches();
    let client = new HttpClient();
    client.createRequest('api/brackets')
      .asGet()
      .send()
      .then((function(data)
      {
          var matches = JSON.parse(data.response);
          matches.forEach(this.addBracket.bind(this));
      }).bind(this));
  }

  addMatch(entry)
  {
    this.matches.push(new Match(entry));
  }

  addBracket(entry)
  {
    this.brackets.push(new Bracket(entry));
  }

  clearMatches()
  {
    this.matches = [];
  }
}
