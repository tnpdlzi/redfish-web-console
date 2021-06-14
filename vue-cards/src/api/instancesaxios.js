import axios from 'axios'

let config = {
  baseURL: `http://localhost:8000/`
}

const instancesapi = axios.create(config)

const authInterceptor = config => {
  /** : Add auth token */
//   let token = localStorage.getItem('token')
//   config.headers.common['Content-Type'] = 'application/json'
//   config.headers.common['Authorization'] = `Bearer ${token}`

  return config
}

instancesapi.interceptors.request.use(authInterceptor)

export { instancesapi }
