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

describe("Virtual Number API", () => {
  it("get all virtual numbers", async () => {
    const response = await request(app).get("/api/virtual-numbers");
    expect(response.statusCode).toBe(200);
    expect(response.body.result.items.length).toBeGreaterThan(0);
  });

  it("get virtual number by id", async () => {
    const response = await request(app).get(
      "/api/virtual-numbers/67548756657688772bbf11f"
    );
    if (response.statusCode === 200) {
      expect(response.body.result.items.length).toBeGreaterThan(0);
    } else if (response.statusCode === 400) {
      expect(response.body.message).toBe("Invalid virtual number id");
    } else {
      expect(response.statusCode).toBe(StatusCodes.NOT_FOUND);
    }
  });

  it("delete virtual number by id", async () => {
    const response = await request(app).delete(
      "/api/virtual-numbers/666666666666666666666666"
    );
    if (response.statusCode === 200) {
      expect(response.body.result.deletedCount).toBe(1);
    } else if (response.statusCode === 400) {
      expect(response.body.message).toBe("Invalid virtual number id");
    } else {
      expect(response.statusCode).toBe(StatusCodes.NOT_FOUND);
    }
  });
});

// describe("Virtual Number API for userId", () => {
//   it("get all virtual numbers for userId", async () => {
//     const response = await request(app).get(
//       "/api/users/user123/virtual-numbers"
//     );
//     if (response.statusCode === 200) {
//       expect(response.body.result.items.length).toBeGreaterThan(0);
//     } else if (response.statusCode === 400) {
//       expect(response.body.message).toBe("Invalid user ID");
//     } else {
//       expect(response.statusCode).toBe(StatusCodes.NOT_FOUND);
//     }
//   });
// });

describe("Virtual Number API for userId", () => {
  it("should return virtual numbers when user exists", async () => {
    const response = await request(app).get(
      "/api/users/6754761855944af90fee1691/virtual-numbers"
    );
    expect(response.statusCode).toBe(200);
    expect(response.body.result.items.length).toBeGreaterThan(0);
  });

  it("should return 400 when user ID is invalid", async () => {
    const response = await request(app).get(
      "/api/users/invalid@user/virtual-numbers"
    );
    expect(response.statusCode).toBe(400);
    expect(response.body.message).toBe("Invalid user ID");
  });

  it("should return 404 when user is not found", async () => {
    const response = await request(app).get(
      "/api/users/nonexistentuserId/virtual-numbers"
    );
    expect(response.statusCode).toBe(StatusCodes.NOT_FOUND);
  });
});
afterEach(async () => {
  await mongoose.connection.close();
});
