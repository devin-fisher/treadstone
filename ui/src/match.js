export class Match {
  constructor(modelVal) {
    this.model = modelVal;
  }

  get name() {
    return this.model.name;
  }

  get id() {
    return this.model.id;
  }

  get state() {
    return this.model.state;
  }

  get bracket_id() {
    return this.model.bracket_id;
  }

  get tournament_id() {
    return this.model.tournament_id;
  }

  get league_id() {
    return this.model.league_id;
  }

  get has_report() {
    return this.model.has_report;
  }

  get has_error() {
    return this.model.has_error;
  }

  get report_url() {
    return 'api/leagues/'+this.model.league_id+'/tournaments/'+ this.model.tournament_id + '/brackets/' + this.model.bracket_id + '/matches/' + this.model.id + '/report'
  }
}
