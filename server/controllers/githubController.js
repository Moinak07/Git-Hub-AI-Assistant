import { asyncHandler } from "../utils/asyncHandler.js";
import { ApiResponse } from "../utils/ApiResponse.js";
import { ApiError } from "../utils/ApiError.js";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const GITHUB_OWNER = "apu52";
const GITHUB_REPO = "Travel_Website";
const GITHUB_API_BASE = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}`;
const HEADERS = { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` };

export const getIssues = asyncHandler(async (req, res) => {
  try {
    const response = await axios.get(`${GITHUB_API_BASE}/issues`, { headers: HEADERS });

    if (response.data.length === 0) {
      throw new ApiError(404, "No issues found");
    }
    const issue = response.data[0];
    const processedIssue = {
      title: issue.title,
      body: issue.body,
      user: issue.user.login,
      state: issue.state,
      created_at: issue.created_at,
      updated_at: issue.updated_at,
      labels: issue.labels.map(label => label.name),
      assignee: issue.assignee ? issue.assignee.login : null,
      comments_url: issue.comments_url,
      html_url: issue.html_url
    };

    return res.status(200).json(new ApiResponse(200, processedIssue));
  } catch (error) {
    throw new ApiError(500, error.message);
  }
});


export const getFirstPullRequest = asyncHandler(async(req,res)=>{
  try {
    const response = await axios.get(`${GITHUB_API_BASE}/pulls`,{headers:HEADERS});
    if(response.data.length === 0){
      throw new ApiError(404,"No pull requests found")
    }
    const firstPR = response.data[0]
    const fileResponse = await axios.get(`${GITHUB_API_BASE}/pulls/${firstPR.number}/files`,{headers:HEADERS});
    const files = fileResponse.data.map(file=>({
      filename:file.filename,
      status:file.status,
      additions:file.additions,
      deletions:file.deletions,
      changes:file.changes,
      patch:file.patch || null
    }))
    const processedPR = {
      title: firstPR.title,
      body: firstPR.body,
      user: firstPR.user.login,
      state: firstPR.state,
      created_at: firstPR.created_at,
      updated_at: firstPR.updated_at,
      merged_at: firstPR.merged_at,
      html_url: firstPR.html_url,
      commits_url: firstPR.commits_url,
      files
    };
    return res.status(200).json(new ApiResponse(200, processedPR));
  } catch (error) {
    throw new ApiError(500, error.message);
  }
})


