import {Match} from './match';
import {League} from './league';
import {Bracket} from './bracket';
import {Tournament} from './tournament';
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
    this.leagues = [];
    this.tournaments = [];
    this.brackets = [];
    this.matches = [];

    this.populateLeague();

    // var currentBracket = localStorage.getItem('currentBracket');
    // if(currentBracket)
    // {
    //   this.populateMatches('2a6a824d-3009-4d23-9c83-859b7a9c2629');
    // }
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

  _populate(obj, objList, clearArrays, url, subObjList, createSubObj)
  {
    if(obj && obj.selected)
    {
      return;
    }

    var i = 0;
    for(i in clearArrays)
    {
      var a = clearArrays[i];
      while(a.length > 0) {
          a.pop();
      }
    }

    if(obj && objList)
    {
      this.select(objList, obj);
    }

    this.httpClient.createRequest(url)
      .asGet()
      .send()
      .then((function(data)
      {
          var matches = JSON.parse(data.response);
          matches.forEach(function(entry)
            {
              subObjList.push(createSubObj(entry));
            });
      }).bind(this));
  }

  populateLeague()
  {
    this._populate(null
      , null
      , [this.leagues, this.tournaments, this.brackets, this.matches]
      , 'api/leagues'
      , this.leagues
      , function(entry){return new League(entry)}
    );
  }

  populateTournaments(league)
  {
    this._populate(league
      , this.leagues
      , [this.tournaments, this.brackets, this.matches]
      , 'api/leagues/'+league.id+'/tournaments/'
      , this.tournaments
      , function(entry){return new Tournament(entry)}
    );
  }

  populateBrackets(tournament)
  {
    this._populate(tournament
      , this.tournaments
      , [this.brackets, this.matches]
      , 'api/leagues/'+tournament.league_id+'/tournaments/'+ tournament.id + '/brackets'
      , this.brackets
      , function(entry){return new Bracket(entry)}
    );
  }

  populateMatches(bracket)
  {
    this._populate(bracket
      , this.brackets
      , [this.matches]
      , 'api/leagues/'+bracket.league_id+'/tournaments/'+ bracket.tournament_id + '/brackets/' + bracket.id + '/matches'
      , this.matches
      , function(entry){return new Match(entry)}
    );
  }

  select(set, value)
  {
    set.forEach(function(entry){entry.selected = false});
    value.selected = true;
  }
}
