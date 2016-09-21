export class Tournament {
  constructor(modelVal) {
    this.model = modelVal;
    this.select = false
  }

  get name() {
    return this.model.name;
  }

  get id() {
    return this.model.id;
  }

  get league_id() {
    return this.model.league_id;
  }


  get selected()
  {
    return this.select
  }
  
  set selected(bool)
  {
    this.select = bool
  }
}
