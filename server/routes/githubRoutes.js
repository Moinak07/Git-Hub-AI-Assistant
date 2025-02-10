import { getIssues, getModifiedFiles, getPullRequests,getPRCommits } from "../controllers/githubController.js";
import express from "express"

const router = express.Router()

router.get("/issues",getIssues)
router.get("/pulls",getPullRequests)
router.get("/pulls/:prNumber/files", getModifiedFiles);
router.get("/pulls/:prNumber/commits", getPRCommits);
export default router
