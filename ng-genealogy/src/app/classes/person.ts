export class Person {
    id: number = 0;
    surname: string = "surname";
    name: string = "name";
    gender: string = "gender";
    birth: string = "birth";
    wedding: string = "wedding";
    death: string = "death";
    father: Person|undefined;
    mother: Person|undefined;
    generation: number = 0;
    birth_city: string = "birth_city";
    wedding_city: string = "wedding_city";
    death_city: string = "death_city";
    notes: string = "notes";

    constructor() {}
}
