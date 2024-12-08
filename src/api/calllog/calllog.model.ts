import mongoose, { Schema, Document, Types } from "mongoose";

// Define enum for call status
enum CallStatus {
  COMPLETED = "completed",
  MISSED = "missed",
  FAILED = "failed",
  BUSY = "busy",
  NO_ANSWER = "no-answer",
}

// Define interface for the document
interface ICallLog extends Document {
  callerId: Types.ObjectId;
  calleeId: Types.ObjectId;
  duration: number; // in seconds
  startTime: Date;
  endTime: Date;
  status: CallStatus;
  createdAt: Date;
  updatedAt: Date;
}

// Define the schema
const callLogSchema = new Schema<ICallLog>(
  {
    callerId: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    calleeId: {
      type: Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },

    startTime: {
      type: Date,
      required: true,
    },
    endTime: {
      type: Date,
      required: true,
    },
    status: {
      type: String,
      enum: Object.values(CallStatus),
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

// Indexes for better query performance
callLogSchema.index({ callerId: 1, calleeId: 1 });
callLogSchema.index({ startTime: 1 });

// write pre save hook to calculate duration
callLogSchema.pre("save", function (this: ICallLog, next) {
  this.duration = this.endTime.getTime() - this.startTime.getTime(); // save time in milliseconds
  next();
});

// Export enums and interface
export { ICallLog, CallStatus };

// Export model
export default mongoose.model<ICallLog>("CallLog", callLogSchema);
