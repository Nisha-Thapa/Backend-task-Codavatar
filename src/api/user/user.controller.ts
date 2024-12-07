import UserService from "./user.service";
import { Request, Response, NextFunction } from "express";

const userService = new UserService();

const createUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const newUser = await userService.createUser(req.body);
    res.apiSuccess("User created successfully", newUser);
  } catch (error) {
    next(error);
  }
};

const getUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.getUserById(req.params.id);

    res.apiSuccess("User retrieved successfully", user);
  } catch (error) {
    next(error);
  }
};

const updateUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.updateUser(req.params.id, req.body);
    res.apiSuccess("User updated successfully", user);
  } catch (error) {
    next(error);
  }
};

const deleteUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await userService.deleteUser(req.params.id);
    res.apiSuccess("User deleted successfully", { user_id: user._id });
  } catch (error) {
    next(error);
  }
};

const getUsers = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const users = await userService.getUsers(req.query);
    res.apiSuccess("Users retrieved successfully", users);
  } catch (error) {
    next(error);
  }
};

export { createUser, getUser, updateUser, deleteUser, getUsers };
