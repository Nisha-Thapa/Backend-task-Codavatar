import { Application } from "express";
import userRouter from "../api/user/user.route";

export default class ExpressApp {
  constructor(private app: Application) {}

  public async configure(): Promise<void> {
    this.setupRoutes();
    // Add any other configuration methods here
  }

  private setupRoutes(): void {
    // Add other routes here
    this.app.use("/api/users", userRouter);
  }
}
