
export class Service {
    constructor(
        public id: string,
        public title: string,
        public publisher?: string,
        public description?: string,
        public type?: string,
        public url?: string,
        public quantity?: number,
        public similarity?: number
    ) { }
}

export class ServiceResponse {
    constructor(
        public service: Service,
        public similarity: number
    ) { }
}

export class FeatureType {
    constructor(
        public similarity?: number,
        public id?: string,
        public title?: string,
        public description?: string,
        public keywords?: string,
        public start_date?: Date,
        public end_date?: Date,
    ) { }
}

export enum CHOICE_LEVEL {
    SERVICE = 'SERVICE',
    FEATURE_TYPE = 'FEATURE_TYPE'
}

export enum RETRIEVE_TYPE {
    SERVICE = 'service',
    FEATURE_TYPE = 'feature-type'
}

export class Resource {
    constructor(
        public id?: string,
        public similarity?: number
    ) { }
}
