// service:
// description: "Web services gerados da base de dados do i3Geo. Para chamar um tema especificamente, veja o sistema de ajuda, digitando no navegador web ogc.php?ajuda=, para uma lista compacta de todos os servicos, digite ogc.php?lista=temas"
// id: "0f2239bb-30e8-4090-af1b-cd3c31b0ef24"
// publisher: "Coordenação Geral de TI"
// title: "i3Geo - i3geo"
// type: "OGC:WMS"
// url: "ht

export class Service{
    constructor(
        public id: string,
        public title: string,
        public publisher?: string,
        public description?: string,
        public type?: string,
        public url?: string
    ){}
}

export class ServiceResponse{
    constructor(
        public service: Service,
        public similarity: number
    ){}
}