import { Router } from "express";
import {
  createVirtualNumber,
  getVirtualNumberById,
  getVirtualNumbers,
} from "./virtualNumber.controller";
import { validateData } from "../../validators/base_validator";
import { virtualNumberSchema } from "./virtualNumberSchema.validate";

const virtualNumberRouter = Router();

virtualNumberRouter.post(
  "/new",
  validateData(virtualNumberSchema),
  createVirtualNumber
);
virtualNumberRouter.get("/:id", getVirtualNumberById);
virtualNumberRouter.get("/", getVirtualNumbers);

export default virtualNumberRouter;
