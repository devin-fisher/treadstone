export class League {
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

  get selected()
  {
    return this.select
  }

  set selected(bool)
  {
    this.select = bool
  }
}
