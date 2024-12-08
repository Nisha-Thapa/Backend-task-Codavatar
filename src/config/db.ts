import dotenv from "dotenv";
import mongoose from "mongoose";
import colors from "colors";

dotenv.config();

export default async function setUpDatabase() {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URL as string);
    console.log(colors.green(`MongoDB Connected: ${conn.connection.host}`));
  } catch (error) {
    console.log(colors.red("Error connecting to MongoDB:"), error);
    process.exit(1);
  }
}
