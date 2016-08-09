import {Match} from './match';
import {HttpClient} from 'aurelia-http-client';


export class App
{
  constructor()
  {
    this.heading = 'Treadstone';
    this.matches = [];
    this.populateMatches('2a6a824d-3009-4d23-9c83-859b7a9c2629');
  }

  populateMatches(bracket_id)
  {
    this.clearMatches();
    let client = new HttpClient();
    client.createRequest('api/'+bracket_id+'/matches')
      .asGet()
      .withReviver()
      .send()
      .then((function(data)
      {
          var matches = JSON.parse(data.response);
          matches.forEach(this.addMatch.bind(this));
      }).bind(this));
  }

  addMatch(entry)
  {
    this.matches.push(new Match(entry.name, entry.state));
  }

  clearMatches()
  {
    this.matches = [];
  }
}
