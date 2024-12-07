import VirtualNumberService from "./virtualNumber.service";
import { Request, Response, NextFunction } from "express";

const virtualNumberService = new VirtualNumberService();

const createVirtualNumber = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const newVirtualNumber = await virtualNumberService.createVirtualNumber(
      req.body
    );
    res.apiSuccess("Virtual number created successfully", newVirtualNumber);
  } catch (error) {
    next(error);
  }
};

const getVirtualNumberById = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const virtualNumber = await virtualNumberService.getVirtualNumberById(
      req.params.id
    );
    res.apiSuccess("Virtual number retrieved successfully", virtualNumber);
  } catch (error) {
    next(error);
  }
};

const getVirtualNumbers = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    const virtualNumbers = await virtualNumberService.getVirtualNumbers(
      req.query
    );
    res.apiSuccess("Virtual numbers retrieved successfully", virtualNumbers);
  } catch (error) {
    next(error);
  }
};

export { createVirtualNumber, getVirtualNumberById, getVirtualNumbers };
