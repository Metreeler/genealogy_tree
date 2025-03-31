export class Person {
    id: number = -1;
    surname: string = "";
    name: string = "";
    gender: string = "";
    birth: string = "";
    wedding: string = "";
    death: string = "";
    father: Person|undefined;
    mother: Person|undefined;
    generation: number = -1;
    birth_city: string = "";
    wedding_city: string = "";
    death_city: string = "";
    notes: string = "";
    job: string = "";
    address: string = "";
    show_parent: boolean = true;

    constructor() {}
}
