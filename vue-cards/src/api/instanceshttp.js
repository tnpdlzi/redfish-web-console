import axios from 'axios'

let config = {
  baseURL: `http://tars.toastoven.net:7072/`
}

const tarshttp = axios.create(config)

const authInterceptor = config => {
  /** : Add auth token */
  let token = localStorage.getItem('token')
  config.headers.common['Content-Type'] = 'application/json'
  config.headers.common['Authorization'] = `Bearer ${token}`

  return config
}

tarshttp.interceptors.request.use(authInterceptor)

export { tarshttp }
