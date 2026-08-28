import axios from 'axios'

const API_BASE_URL = 'https://recoverai-backend.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
})

export async function getDashboardSummary() {
  const response = await api.get('/dashboard/summary')
  return response.data
}

export async function getRecoveryCases() {
  const response = await api.get('/dashboard/cases')
  return response.data
}

export async function getCaseDetail(caseId) {
  const response = await api.get('/dashboard/cases/' + caseId)
  return response.data
}
