import express from "express";
import { validateData } from "../../validators/base_validator";
import {
  createUser,
  getUser,
  updateUser,
  deleteUser,
  getUsers,
} from "./user.controller";
import { createUserSchema, updateUserSchema } from "./userSchema.validate";

const userRouter = express.Router();

userRouter.post("/new", validateData(createUserSchema), createUser);
userRouter.get("/:id", getUser);
userRouter.patch("/:id", validateData(updateUserSchema as any), updateUser);
userRouter.delete("/:id", deleteUser);
userRouter.get("/", getUsers);
export default userRouter;
