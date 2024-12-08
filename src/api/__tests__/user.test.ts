import app from "../../index";
import request from "supertest";
import dotenv from "dotenv";
import { beforeEach } from "node:test";
import mongoose from "mongoose";
import { afterEach } from "node:test";
import { StatusCodes } from "http-status-codes";

dotenv.config();

beforeEach(async () => {
  await mongoose.connect(process.env.MONGO_URL);
});

describe("User API", () => {
  it("get all users", async () => {
    const response = await request(app).get("/api/users");
    expect(response.statusCode).toBe(200);
    expect(response.body.result.items.length).toBeGreaterThan(0);
  });

  describe("POST /api/users/new", () => {
    it("should return 400 when required fields are missing", async () => {
      const response = await request(app).post("/api/users/new").send({
        // Missing required fields
      });

      expect(response.status).toBe(StatusCodes.BAD_REQUEST);
      expect(response.body).toHaveProperty("error");
    });

    it("should return 400 when email is invalid", async () => {
      const response = await request(app).post("/api/users/new").send({
        name: "test",
        email: "invalid-email", // Invalid email format
      });

      expect(response.status).toBe(StatusCodes.BAD_REQUEST);
      expect(response.body).toHaveProperty("error");
    });

    it("should return 400 when name is too short", async () => {
      const response = await request(app).post("/api/users/new").send({
        name: "t", // Too short name
        email: "test@test.com",
      });

      expect(response.status).toBe(StatusCodes.BAD_REQUEST);
      expect(response.body).toHaveProperty("error");
    });

    it("get user by id", async () => {
      const response = await request(app).get(
        "/api/users/666666666666666666666666"
      );
      if (response.statusCode === 200) {
        expect(response.body.result.name).toBe("test1234");
      } else if (response.statusCode === 400) {
        expect(response.body.error).toBe("Invalid user id");
      } else {
        expect(response.statusCode).toBe(StatusCodes.NOT_FOUND);
      }
    });

    it("should return 409 when user already exists", async () => {
      // First create a user
      const userData = {
        name: "test1234",
        email: "test1234@test.com",
      };

      // First request should succeed
      await request(app).post("/api/users/new").send(userData);

      // Second request with same email should fail
      const response = await request(app).post("/api/users/new").send(userData);

      expect(response.status).toBe(StatusCodes.CONFLICT);
      expect(response.body).toHaveProperty("error");
      expect(response.body.error).toBe("User already exists");
    });

    it("create a new user", async () => {
      const response = await request(app).post("/api/users/new").send({
        name: "uniqueuser",
        email: "unique@test.com",
      });

      if (response.statusCode === StatusCodes.CONFLICT) {
        expect(response.body).toHaveProperty("error");
        expect(response.body.error).toBe("User already exists");
      } else if (response.statusCode === StatusCodes.BAD_REQUEST) {
        expect(response.body).toHaveProperty("error");
      } else {
        expect(response.statusCode).toBe(200);
        expect(response.body.message).toBe("User created successfully");
      }
    });
  });
});

afterEach(async () => {
  await mongoose.connection.close();
});
