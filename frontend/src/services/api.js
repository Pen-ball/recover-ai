import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000'

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
