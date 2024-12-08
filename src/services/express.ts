import { Application } from "express";
import userRouter from "../api/user/user.route";
import virtualNumberRouter from "../api/virtualphonenumber/virtualNumber.route";

export default class ExpressApp {
  constructor(private app: Application) {}

  public async configure(): Promise<void> {
    this.setupRoutes();
    // Add any other configuration methods here
  }

  private setupRoutes(): void {
    // Add other routes here
    this.app.use("/api/users", userRouter);
    this.app.use("/api/virtual-numbers", virtualNumberRouter);
  }
}
