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

  get games() {
    return this.model.games;
  }

  get bracket_id() {
    return this.model.bracket_id;
  }

  get scheduledTime() {
    var date = new Date(this.model.scheduledTime);
    return date.toDateString() + ", " + date.toLocaleTimeString();
  }
}
