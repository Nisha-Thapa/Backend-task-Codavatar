import { IUser, UserModel } from "./user.model";
import { AppError } from "../../utils/errorHandler";
import { isValidObjectId, Types } from "mongoose";
import { VirtualNumberModel } from "../virtualphonenumber/virtualNumber.model";
import { StatusCodes } from "http-status-codes";

const PAGE_SIZE = 10;

type GetUsersParams = {
  page?: number;
  limit?: number;
  filter?: string;
};
type IPaginationParams = GetUsersParams;

class UserService {
  /**
   * Checks if a user with the given email already exists
   * @private
   * @param {string} email - The email to check
   * @returns {Promise<boolean>} Returns true if user exists, false otherwise
   */
  private async checkIfUserExists(email: string): Promise<boolean> {
    const existingUser = await UserModel.exists({ email });
    return !!existingUser;
  }

  /**
   * Creates a new user
   * @param {IUser} user - The user data to create
   * @throws {AppError} Throws 409 if user already exists
   * @throws {AppError} Throws 400 if validation fails
   * @returns {Promise<IUser>} The created user
   */
  async createUser(user: IUser) {
    try {
      const userExists = await this.checkIfUserExists(user.email);
      if (userExists) {
        throw new AppError("User already exists", StatusCodes.CONFLICT);
      }
      const newUser = await UserModel.create(user);
      return newUser;
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }
      // Handle mongoose validation errors
      if (error.name === "ValidationError") {
        throw new AppError(error.message, StatusCodes.BAD_REQUEST);
      }
      // Handle other errors
      throw error;
    }
  }

  /**
   * Retrieves a user by their ID
   * @param {string} id - The user ID to find
   * @throws {AppError} Throws 400 if ID is invalid
   * @throws {AppError} Throws 404 if user not found
   * @returns {Promise<IUser>} The found user
   */
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

  /**
   * Updates a user's information
   * @param {string} id - The user ID to update
   * @param {IUser} user - The updated user data
   * @throws {AppError} Throws 400 if ID is invalid
   * @returns {Promise<IUser>} The updated user
   */
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

  /**
   * Deletes a user by their ID
   * @param {string} id - The user ID to delete
   * @throws {AppError} Throws 400 if ID is invalid
   * @throws {AppError} Throws 404 if user not found
   * @returns {Promise<IUser>} The deleted user
   */
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

  /**
   * Retrieves a paginated list of users with optional filtering
   * @param {GetUsersParams} params - Pagination and filter parameters
   * @param {number} [params.page=1] - The page number
   * @param {number} [params.limit=10] - Items per page
   * @param {string} [params.filter] - Search filter for name or email
   * @returns {Promise<{items: IUser[], stats: object}>} Paginated users and stats
   */
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

  /**
   * Gets virtual numbers associated with a user
   * @param {string} id - The user ID
   * @param {IPaginationParams} params - Pagination and filter parameters
   * @param {number} [params.page=1] - The page number
   * @param {number} [params.limit=10] - Items per page
   * @param {string} [params.filter] - Search filter for number
   * @throws {AppError} Throws 400 if user ID is invalid
   * @returns {Promise<{items: any[], stats: object}>} Paginated virtual numbers and stats
   */
  async getVirtualNumbersByUserId(id: string, params: IPaginationParams) {
    const { page = 1, limit = PAGE_SIZE, ...rest } = params;
    try {
      if (!isValidObjectId(id)) {
        throw new AppError("Invalid user ID", 400);
      }

      const searchQuery = rest.filter
        ? {
            $or: [{ number: { $regex: rest.filter, $options: "i" } }],
          }
        : {};

      const aggregationPipeline = [
        {
          $match: {
            userId: new Types.ObjectId(id),
            ...searchQuery,
          },
        },
        {
          $facet: {
            metadata: [{ $count: "totalCount" }],
            data: [
              { $skip: (page - 1) * limit },
              { $limit: limit },
              {
                $lookup: {
                  from: "users",
                  localField: "userId",
                  foreignField: "_id",
                  as: "userDetails",
                },
              },
              { $unwind: "$userDetails" },
            ],
          },
        },
      ];

      const [result] = await VirtualNumberModel.aggregate(aggregationPipeline);

      const totalCount = result.metadata[0]?.totalCount || 0;
      const totalPages = Math.ceil(totalCount / limit);

      return {
        items: result.data,
        stats: {
          totalPages,
          totalCount,
          currentPage: Number(page),
        },
      };
    } catch (error) {
      throw error;
    }
  }
}

export default UserService;
