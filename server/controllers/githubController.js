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


export const getPullRequests = asyncHandler(async (req, res) => {
    try {
      const response = await axios.get(`${GITHUB_API_BASE}/pulls`, { headers: HEADERS });
      const processedPRs = response.data.map(pr => ({
        title: pr.title,
        body: pr.body,
        user: pr.user.login,
        state: pr.state,
        created_at: pr.created_at,
        updated_at: pr.updated_at,
        merged_at: pr.merged_at,
        html_url: pr.html_url,
        commits_url: pr.commits_url,
        files_url: `${GITHUB_API_BASE}/pulls/${pr.number}/files`
      }));
  
      return res.status(200).json(new ApiResponse(200, processedPRs));
    } catch (error) {
      throw new ApiError(500, error.message);
    }
  });
  

  export const getModifiedFiles = asyncHandler(async (req, res) => {
    try {
      const { prNumber } = req.params;
      const response = await axios.get(`${GITHUB_API_BASE}/pulls/${prNumber}/files`, { headers: HEADERS });
  
      const modifiedFiles = response.data.map(file => ({
        filename: file.filename,
        status: file.status,
        changes: file.changes,
        patch: file.patch || "No patch available"
      }));
  
      return res.status(200).json(new ApiResponse(200, modifiedFiles));
    } catch (error) {
      throw new ApiError(500, error.message);
    }
  });

  export const getPRCommits = asyncHandler(async (req, res) => {
    try {
      const { prNumber } = req.params;
      const response = await axios.get(`${GITHUB_API_BASE}/pulls/${prNumber}/commits`, { headers: HEADERS });
      const commits = response.data.map(commit => ({
        sha: commit.sha,
        message: commit.commit.message,
        author: commit.commit.author.name,
        date: commit.commit.author.date
      }));
      return res.status(200).json(new ApiResponse(200, commits));
    } catch (error) {
      throw new ApiError(500, error.message);
    }
  });
  

