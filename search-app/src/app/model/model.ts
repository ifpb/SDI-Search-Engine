
export class Service {
    constructor(
        public id: string,
        public wfs_url: string,
        public wms_url?: string,
        public service_processed?: string,
        public title?: string,
        public description?: string,
        public publisher?: string,
        public start_date?: string,
        public end_date?: string,
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
