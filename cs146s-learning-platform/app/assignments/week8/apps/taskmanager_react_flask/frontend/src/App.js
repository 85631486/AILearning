import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import TaskList from './TaskList';
import TaskForm from './TaskForm';
import UserList from './UserList';
import UserForm from './UserForm';

function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    // 检查API健康状态
    fetch('/api/health')
      .then(response => response.json())
      .then(data => setHealth(data))
      .catch(error => console.error('API健康检查失败:', error));
  }, []);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>TaskManager - 任务管理系统</h1>
          <p>使用React + Flask构建的任务管理应用</p>
          {health && (
            <div className="health-status">
              <span className="status-dot healthy"></span>
              API状态: {health.status}
            </div>
          )}
        </header>

        <nav className="App-nav">
          <ul>
            <li><Link to="/">首页</Link></li>
            <li><Link to="/tasks">任务管理</Link></li>
            <li><Link to="/users">用户管理</Link></li>
          </ul>
        </nav>

        <main className="App-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/tasks" element={<TaskList />} />
            <Route path="/tasks/new" element={<TaskForm />} />
            <Route path="/users" element={<UserList />} />
            <Route path="/users/new" element={<UserForm />} />
          </Routes>
        </main>

        <footer className="App-footer">
          <p>&copy; 2024 TaskManager - AI生成的应用示例</p>
        </footer>
      </div>
    </Router>
  );
}

function Home() {
  const [stats, setStats] = useState({ tasks: 0, users: 0 });

  useEffect(() => {
    // 获取统计信息
    Promise.all([
      fetch('/api/tasks').then(r => r.json()),
      fetch('/api/users').then(r => r.json())
    ]).then(([tasks, users]) => {
      setStats({
        tasks: tasks.length,
        users: users.length
      });
    }).catch(error => console.error('获取统计信息失败:', error));
  }, []);

  return (
    <div className="home">
      <h2>欢迎使用TaskManager</h2>
      <div className="stats">
        <div className="stat-card">
          <h3>任务数量</h3>
          <p className="stat-number">{stats.tasks}</p>
        </div>
        <div className="stat-card">
          <h3>用户数量</h3>
          <p className="stat-number">{stats.users}</p>
        </div>
      </div>
      <div className="features">
        <h3>功能特性</h3>
        <ul>
          <li>✅ 任务的增删改查</li>
          <li>✅ 用户管理</li>
          <li>✅ 任务状态跟踪</li>
          <li>✅ 优先级设置</li>
          <li>✅ 截止日期管理</li>
        </ul>
      </div>
    </div>
  );
}

export default App;
