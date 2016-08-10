export class Bracket {
  constructor(modelVal) {
    this.model = modelVal;
  }

  get name() {
    return this.model.tournaments_name + " -- " +this.model.bracket_name;
  }

  get bracket_id() {
    return this.model.bracket_id;
  }
}
