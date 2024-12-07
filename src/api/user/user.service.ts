import { IUser, UserModel } from "./user.model";
import { AppError } from "../../utils/errorHandler";
import { isValidObjectId } from "mongoose";

const PAGE_SIZE = 10;

type GetUsersParams = {
  page?: number;
  limit?: number;
  filter?: string;
};

class UserService {
  // A function that check if the user already exists by email
  private async checkIfUserExists(email: string): Promise<boolean> {
    const existingUser = await UserModel.exists({ email });
    // Convert to boolean - will be true if user exists, false if null
    return !!existingUser;
  }

  async createUser(user: IUser) {
    try {
      const userExists = await this.checkIfUserExists(user.email);
      // here userExists is a object with the user id if the user exists
      if (userExists) {
        throw new AppError("User already exists", 409);
      }
      const newUser = await UserModel.create(user);
      return newUser;
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }
      // Handle mongoose validation errors
      if (error.name === "ValidationError") {
        throw new AppError(error.message, 400);
      }
      // Handle other errors
      throw error;
    }
  }

  async getUserById(id: string) {
    try {
      if (!isValidObjectId(id)) {
        throw new AppError("Invalid user ID", 400);
      }
      const user = await UserModel.findById(id);
      if (!user) {
        throw new AppError("User not found", 404);
      }
      return user;
    } catch (error) {
      throw error;
    }
  }

  async updateUser(id: string, user: IUser) {
    try {
      if (!isValidObjectId(id)) {
        throw new AppError("Invalid user ID", 400);
      }
      return await UserModel.findByIdAndUpdate(id, user, { new: true });
    } catch (error) {
      throw error;
    }
  }

  async deleteUser(id: string) {
    try {
      if (!isValidObjectId(id)) {
        throw new AppError("Invalid user ID", 400);
      }
      const user = await UserModel.findByIdAndDelete(id);
      if (!user) {
        throw new AppError("User not found", 404);
      }
      return user;
    } catch (error) {
      throw error;
    }
  }

  async getUsers(params: GetUsersParams) {
    const { page = 1, limit = PAGE_SIZE, ...rest } = params;

    try {
      // searchquery is also passed as filter="searchkey"
      const searchQuery = rest.filter
        ? {
            $or: [
              { name: { $regex: rest.filter, $options: "i" } },
              { email: { $regex: rest.filter, $options: "i" } },
            ],
          }
        : {};

      const totalCount = await UserModel.countDocuments(searchQuery);
      const users = await UserModel.find(searchQuery)
        .skip((page - 1) * limit)
        .limit(limit);
      // keep track of current page, total page, total count, hasNextPage,hasPreviousPage
      const totalPages = Math.ceil(totalCount / limit);
      return {
        items: users,
        stats: {
          totalPages,
          totalCount,
          currentPage: Number(page),
          hasNextPage: page < totalPages,
          hasPreviousPage: page > 1,
        },
      };
    } catch (error) {
      throw error;
    }
  }
}

export default UserService;
