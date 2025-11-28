/**
 * API helper for AutoResearcher AI backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Run a research query
 * @param {string} query - URL or topic to research
 * @returns {Promise<Object>} Research results
 */
export async function runResearch(query) {
    const response = await fetch(`${API_BASE_URL}/research`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query }),
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export async function ping() {
    const response = await fetch(`${API_BASE_URL}/ping`);
    return response.json();
}
