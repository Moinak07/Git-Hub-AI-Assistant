import { getIssues, getFirstPullRequest, receiveTestCases} from "../controllers/githubController.js";
import express from "express"

const router = express.Router()

router.get("/issues",getIssues)
router.get("/pulls",getFirstPullRequest)
router.post("/test-cases",receiveTestCases)
export default router
