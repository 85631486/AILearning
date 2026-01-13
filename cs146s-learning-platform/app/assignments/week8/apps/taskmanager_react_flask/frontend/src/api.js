import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token
    // config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// 任务API
export const taskAPI = {
  // 获取所有任务
  getAllTasks: () => api.get('/api/tasks'),

  // 获取单个任务
  getTask: (id) => api.get(`/api/tasks/${id}`),

  // 创建任务
  createTask: (taskData) => api.post('/api/tasks', taskData),

  // 更新任务
  updateTask: (id, taskData) => api.put(`/api/tasks/${id}`, taskData),

  // 删除任务
  deleteTask: (id) => api.delete(`/api/tasks/${id}`),
};

// 用户API
export const userAPI = {
  // 获取所有用户
  getAllUsers: () => api.get('/api/users'),

  // 获取单个用户
  getUser: (id) => api.get(`/api/users/${id}`),

  // 创建用户
  createUser: (userData) => api.post('/api/users', userData),

  // 获取用户的任务
  getUserTasks: (userId) => api.get(`/api/users/${userId}/tasks`),
};

// 健康检查API
export const healthAPI = {
  checkHealth: () => api.get('/api/health'),
};

export default api;
