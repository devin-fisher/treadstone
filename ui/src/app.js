import {Match} from './match';
import {Bracket} from './bracket';
import {HttpClient} from 'aurelia-http-client';


export class App
{
  constructor()
  {
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
    let client = new HttpClient();
    client.createRequest('api/brackets/'+bracket_id+'/matches')
      .asGet()
      .send()
      .then((function(data)
      {
          var matches = JSON.parse(data.response);
          matches.forEach(this.addMatch.bind(this));
      }).bind(this));
    localStorage.setItem('currentBracket',bracket_id);
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
