import { Schema, model, Document } from "mongoose";
import { UserAccountStatus } from "./constant";

interface IUser extends Document {
  email: string;
  name: string;
  accountStatus: "active" | "suspended" | "inactive" | any;
  createdAt: Date;
  updatedAt: Date;
}

const userSchema = new Schema<IUser>(
  {
    email: {
      type: String,
      required: true,
      unique: true,
      trim: true,
    },
    name: {
      type: String,
      required: true,
    },
    accountStatus: {
      type: String,
      enum: [
        UserAccountStatus.ACTIVE,
        UserAccountStatus.SUSPENDED,
        UserAccountStatus.INACTIVE,
      ],
      default: UserAccountStatus.ACTIVE,
    },
  },
  {
    timestamps: true,
  }
);

// Ensure email is unique in the database
// make email search faster by creating index
userSchema.index({ email: 1 }, { unique: true });
// Export the model and interfaces
export { IUser };
export const UserModel = model<IUser>("User", userSchema);
