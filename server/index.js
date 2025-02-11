import express from "express";
import dotenv from "dotenv";
import githubRoutes from "./routes/githubRoutes.js";

const app = express()
app.use(express.json())
app.use("/api/github",githubRoutes)
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));