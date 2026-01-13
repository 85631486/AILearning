import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { taskAPI } from './api';
import './TaskList.css';

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskAPI.getAllTasks();
      setTasks(response.data);
      setError(null);
    } catch (err) {
      setError('获取任务列表失败');
      console.error('获取任务列表失败:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('确定要删除这个任务吗？')) {
      return;
    }

    try {
      await taskAPI.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      alert('删除任务失败');
      console.error('删除任务失败:', err);
    }
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await taskAPI.updateTask(taskId, { status: newStatus });
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, status: newStatus } : task
      ));
    } catch (err) {
      alert('更新任务状态失败');
      console.error('更新任务状态失败:', err);
    }
  };

  const getStatusBadgeClass = (status) => {
    const classes = {
      'pending': 'status-pending',
      'in_progress': 'status-in-progress',
      'completed': 'status-completed',
      'cancelled': 'status-cancelled'
    };
    return classes[status] || 'status-default';
  };

  const getPriorityBadgeClass = (priority) => {
    const classes = {
      'low': 'priority-low',
      'medium': 'priority-medium',
      'high': 'priority-high',
      'urgent': 'priority-urgent'
    };
    return classes[priority] || 'priority-default';
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="task-list-container">
      <div className="task-list-header">
        <h2>任务管理</h2>
        <div className="task-actions">
          <Link to="/tasks/new" className="btn btn-primary">新建任务</Link>
        </div>
      </div>

      <div className="task-filters">
        <label>状态筛选:</label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">全部</option>
          <option value="pending">待处理</option>
          <option value="in_progress">进行中</option>
          <option value="completed">已完成</option>
          <option value="cancelled">已取消</option>
        </select>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="no-tasks">
          {filter === 'all' ? '暂无任务' : `暂无${filter}状态的任务`}
        </div>
      ) : (
        <div className="task-grid">
          {filteredTasks.map(task => (
            <div key={task.id} className="task-card">
              <div className="task-header">
                <h3>{task.title}</h3>
                <div className="task-badges">
                  <span className={`badge status-badge ${getStatusBadgeClass(task.status)}`}>
                    {task.status}
                  </span>
                  <span className={`badge priority-badge ${getPriorityBadgeClass(task.priority)}`}>
                    {task.priority}
                  </span>
                </div>
              </div>

              <div className="task-body">
                {task.description && (
                  <p className="task-description">{task.description}</p>
                )}

                {task.due_date && (
                  <div className="task-due-date">
                    <strong>截止日期:</strong> {new Date(task.due_date).toLocaleDateString()}
                  </div>
                )}

                <div className="task-meta">
                  <small>
                    创建时间: {new Date(task.created_at).toLocaleString()}
                  </small>
                  {task.updated_at !== task.created_at && (
                    <small>
                      更新时间: {new Date(task.updated_at).toLocaleString()}
                    </small>
                  )}
                </div>
              </div>

              <div className="task-actions">
                <select
                  value={task.status}
                  onChange={(e) => handleStatusChange(task.id, e.target.value)}
                  className="status-select"
                >
                  <option value="pending">待处理</option>
                  <option value="in_progress">进行中</option>
                  <option value="completed">已完成</option>
                  <option value="cancelled">已取消</option>
                </select>

                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="btn btn-danger btn-small"
                >
                  删除
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TaskList;
