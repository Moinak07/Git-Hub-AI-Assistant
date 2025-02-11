import { getIssues, getFirstPullRequest} from "../controllers/githubController.js";
import express from "express"

const router = express.Router()

router.get("/issues",getIssues)
router.get("/pulls",getFirstPullRequest)
export default router
