import { AppError } from "../../utils/errorHandler";
import { IVirtualNumber, VirtualNumberModel } from "./virtualNumber.model";
import { isValidObjectId } from "mongoose";

type GetVirtualNumbersParams = {
  page?: number;
  limit?: number;
  filter?: string;
};

const PAGE_SIZE = 10;

class VirtualNumberService {
  /**
   * Checks if a virtual number already exists
   * @private
   * @param {string} number - The phone number to check
   * @returns {Promise<boolean>} Returns true if number exists, false otherwise
   */
  private async checkIfNumberExists(number: string): Promise<boolean> {
    const existingNumber = await VirtualNumberModel.exists({ number });
    return !!existingNumber;
  }

  /**
   * Creates a new virtual phone number
   * @param {IVirtualNumber} virtualNumber - The virtual number data to create
   * @throws {AppError} Throws 409 if number already exists
   * @throws {AppError} Throws 400 if validation fails
   * @returns {Promise<IVirtualNumber>} The created virtual number
   */
  async createVirtualNumber(virtualNumber: IVirtualNumber) {
    try {
      const virtualNumberExists = await this.checkIfNumberExists(
        virtualNumber.number
      );
      if (virtualNumberExists) {
        throw new AppError("Virtual number already exists", 409);
      }
      if (!isValidObjectId(virtualNumber.userId)) {
        throw new AppError("Invalid user ID", 400);
      }
      const newVirtualNumber = await VirtualNumberModel.create(virtualNumber);
      return newVirtualNumber;
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }
      if (error.name === "ValidationError") {
        throw new AppError(error.message, 400);
      }
      throw error;
    }
  }

  /**
   * Retrieves a virtual number by its ID
   * @param {string} id - The virtual number ID to find
   * @throws {AppError} Throws 400 if ID is invalid
   * @throws {AppError} Throws 404 if number not found
   * @returns {Promise<IVirtualNumber>} The found virtual number
   */
  async getVirtualNumberById(id: string) {
    try {
      if (!isValidObjectId(id)) {
        throw new AppError("Invalid virtual number id", 400);
      }
      const virtualNumber = await VirtualNumberModel.findById(id);
      return virtualNumber;
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }
      throw new AppError("Failed to get virtual number", 500);
    }
  }

  /**
   * Retrieves a paginated list of virtual numbers with optional filtering
   * @param {GetVirtualNumbersParams} params - Pagination and filter parameters
   * @param {number} [params.page=1] - The page number
   * @param {number} [params.limit=10] - Items per page
   * @param {string} [params.filter] - Search filter for number
   * @returns {Promise<{items: IVirtualNumber[], stats: object}>} Paginated virtual numbers and stats
   */

  async getVirtualNumbers(params: GetVirtualNumbersParams) {
    const { page = 1, limit = PAGE_SIZE, ...rest } = params;

    try {
      const searchQuery = rest.filter
        ? {
            $or: [{ number: { $regex: rest.filter, $options: "i" } }],
          }
        : {};

      const totalCount = await VirtualNumberModel.countDocuments(searchQuery);
      const virtualNumbers = await VirtualNumberModel.find(searchQuery)
        .skip((page - 1) * limit)
        .limit(limit);

      const totalPages = Math.ceil(totalCount / limit);
      return {
        items: virtualNumbers,
        stats: {
          totalPages,
          totalCount,
          currentPage: Number(page),
          hasNextPage: page < totalPages,
          hasPreviousPage: page > 1,
        },
      };
    } catch (error) {}
  }
}

export default VirtualNumberService;
