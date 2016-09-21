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
}
