import { z } from "zod";

const NumberStatus = {
  ACTIVE: "active",
  INACTIVE: "inactive",
};

export const virtualNumberSchema = z.object({
  number: z.string().min(10, { message: "At least 10 digits are required" }),
  userId: z.string().min(1, { message: "User ID is required" }),
  features: z.array(z.string()).optional(),
  status: z.enum([NumberStatus.ACTIVE, NumberStatus.INACTIVE]).optional(),
});
