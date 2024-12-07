import { Response as ExpressResponse } from "express";

declare module "express" {
  export interface Response extends ExpressResponse {
    apiSuccess: (message: string, result: any, statusCode?: number) => void;
    apiError: (message: string, statusCode?: number, result?: any) => void;
  }
}

declare namespace Express {
  interface Response {
    apiSuccess(message: string, result?: any, statusCode?: number): void;
    apiError(message: string, statusCode?: number, result?: any): void;
  }
}
