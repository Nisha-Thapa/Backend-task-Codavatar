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
  // function to check if the virtual number already exists
  private async checkIfVirtualNumberExists(number: string) {
    const existingVirtualNumber = await VirtualNumberModel.exists({ number });
    return !!existingVirtualNumber;
  }

  async createVirtualNumber(virtualNumber: IVirtualNumber) {
    try {
      const virtualNumberExists = await this.checkIfVirtualNumberExists(
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
