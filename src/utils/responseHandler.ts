import { Request, Response, NextFunction } from "express";

interface ApiResponse {
  type: string;
  status_code: number;
  message: string;
  result: any;
}

const parseResponse = (
  statusCode: number,
  message: string,
  result: any
): ApiResponse => {
  const type = statusCode >= 200 && statusCode < 300 ? "success" : "error";
  const status_code = statusCode;

  return { type, status_code, message, result };
};

const responseHandler = (req: Request, res: Response, next: NextFunction) => {
  res.apiSuccess = (
    message: string,
    result: any = null,
    statusCode = 200
  ): void => {
    const successResponse = parseResponse(statusCode, message, result);
    res.status(statusCode).json(successResponse);
  };

  res.apiError = (
    message: string,
    statusCode = 500,
    result: any = null
  ): void => {
    const errorResponse = parseResponse(statusCode, message, result);
    res.status(statusCode).json(errorResponse);
  };

  next();
};

export default responseHandler;
