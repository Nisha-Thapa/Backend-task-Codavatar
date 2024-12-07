import { z } from "zod";
import { UserAccountStatus } from "./constant";

export const createUserSchema = z.object({
  name: z.string().min(5, {
    message: "Name is required and must be at least 5 characters long",
  }),
  email: z.string().email({ message: "Invalid email address" }),
  accountStatus: z
    .enum([
      UserAccountStatus.ACTIVE,
      UserAccountStatus.SUSPENDED,
      UserAccountStatus.INACTIVE,
    ])
    .optional(),
});

// Base schema with all possible update fields
const userUpdateFields = {
  name: z
    .string()
    .min(5, {
      message: "Name must be at least 5 characters long",
    })
    .optional(),
  email: z
    .string()
    .email({
      message: "Invalid email format",
    })
    .optional(),
  accountStatus: z
    .enum([
      UserAccountStatus.ACTIVE,
      UserAccountStatus.SUSPENDED,
      UserAccountStatus.INACTIVE,
    ])
    .optional(),
};
// how to add validation for at least one field is required

export const updateUserSchema = z
  .object(userUpdateFields)
  .refine((data) => Object.keys(data).length > 0, {
    message: "At least one field must be provided for update",
  });
