import express, { Request, Response, NextFunction, Application } from "express";
import dotenv from "dotenv";
import cors from "cors";
import helmet from "helmet";

import ExpressApp from "./services/express";
import responseHandler from "./utils/responseHandler";
import setUpDatabase from "./config/db";
import { AppError } from "./utils/errorHandler";

dotenv.config();

class Server {
  private app: Application;
  private port: number;

  constructor() {
    this.app = express();
    this.port = parseInt(process.env.PORT || "5555", 10);
    this.configureMiddleware();
  }

  private configureMiddleware(): void {
    this.app.use(cors());
    this.app.use(
      helmet({
        contentSecurityPolicy: false,
        frameguard: true,
      })
    );
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
    this.app.use(responseHandler);
    this.app.use(this.logRequest);

    this.configureRoutes();

    this.app.use(this.errorHandler);
  }

  private logRequest(req: Request, res: Response, next: NextFunction): void {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
  }

  private errorHandler(
    err: AppError,
    req: Request,
    res: Response,
    next: NextFunction
  ): void {
    err.statusCode = err.statusCode || 500;
    err.status = err.status || "error";

    if (process.env.NODE_ENV === "development") {
      res.apiError(err.message, err.statusCode, {
        status: err.status,
        isOperational: err.isOperational,
        stack: err.stack,
      });
    } else {
      res.apiError(
        err.isOperational ? err.message : "Something went wrong!",
        err.statusCode,
        {
          status: err.status,
        }
      );
    }
  }

  private async setupDatabase(): Promise<void> {
    await setUpDatabase();
  }

  private async configureRoutes(): Promise<void> {
    await new ExpressApp(this.app).configure();
  }

  public async start(): Promise<void> {
    await this.setupDatabase();
    await this.configureRoutes();

    this.app.listen(this.port, () => {
      console.log(
        `Server is starting at port ${this.port}, http://localhost:${this.port}`
      );
    });
  }
}

const server = new Server();
server.start();
